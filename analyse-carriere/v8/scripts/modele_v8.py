# -*- coding: utf-8 -*-
"""Version 8 : 339 metiers FAP-2021 (DARES), France et Suisse, methode v6 inchangee.

Regles (declarees avant calcul, etape 1 validee le 29 octobre 2026) :
- metiers : FAP-2021 au niveau le plus fin (341), domaine X exclu ;
- variantes : salarie si au moins 20 % de salaries (DARES), independant si au moins 20 % de non-salaries,
  dans les deux pays ; Suisse salarie en resident et en frontalier (sauf postes reserves aux nationaux) ;
  Suisse independant seulement si une cellule revenu existe (medecins, dentistes) ; on garde la
  meilleure variante par metier (regle v7.1) ;
- 7 dimensions Eurofound a poids egaux ; revenu net avant impot (definition v6), EQTP, PPA ;
- Monte Carlo variante A de la v6 : 10 000 tirages, graine 20261029, notes estimees +-1.
Usage : python -I modele_v8.py <dossier dl> <sortie json>
"""
import csv
import json
import math
import os
import sys
from statistics import NormalDist

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import encodage_v8 as E  # noqa: E402
import lirexlsx  # noqa: E402

DL = sys.argv[1]
SORTIE = sys.argv[2]
Z = NormalDist()

# --- Nomenclature ------------------------------------------------------------------------------------
NOM, PARENT228, NOM228 = {}, {}, {}
for r in csv.DictReader(open(os.path.join(DL, "fap", "fap2021.csv"), encoding="utf-8-sig"), delimiter=";"):
    if r["Code FAP 22"] == "X":
        continue
    NOM[r["Code FAP 341"]] = r["Intitulé FAP 341"]
    PARENT228[r["Code FAP 341"]] = r["Code FAP 228"]
    NOM228[r["Code FAP 228"]] = r["Intitulé FAP 228"]
METIERS = sorted(NOM)
assert len(METIERS) == 339, len(METIERS)


def chaine(c):
    """Niveaux du plus fin au plus large : (code, rang) ; rang 0 = le metier lui-meme."""
    p = PARENT228[c]
    out = [(c, 0)]
    if p != c:
        out.append((p, 1))
    out += [(c[:3], 2), (c[0], 3)]
    return out


# --- DARES, portraits 2023-2025 ----------------------------------------------------------------------
def _liste(s):
    return [int(x) / 1000 if x not in ("",) else None for x in s.split(",")] if s else None


DARES = {}
for ligne in open(os.path.join(DL, "dares", "portraits_2023_2025.psv"), encoding="utf-8"):
    if ligne.startswith("#") or not ligne.strip():
        continue
    f = ligne.rstrip("\n").split("|")
    f += [""] * (10 - len(f))
    DARES[f[0]] = dict(med=float(f[1]) if f[1] else None, net=_liste(f[2]), ind=_liste(f[3]), statut=_liste(f[4]),
                       emp=_liste(f[5]), atyp=_liste(f[6]), partiel=_liste(f[7]), N=f[8])


def dares(c, champ):
    for code, rang in chaine(c):
        v = DARES.get(code, {}).get(champ)
        if v is not None and (not isinstance(v, list) or any(x is not None for x in v)):
            return v, code, rang
    return None, None, None


# --- DARES - France Travail, tensions 2024 (FAP 228) -------------------------------------------------
TENS = {}
for ligne in open(os.path.join(DL, "dares", "tensions_2024_fap228.psv"), encoding="utf-8"):
    if ligne.startswith("#") or not ligne.strip():
        continue
    f = ligne.split("|")
    disc = [x for x in f[2].split(",")]
    TENS[f[0]] = int(float(disc[0])) if disc[0] not in ("", "n.d.") else None

# --- OFS, ESS 2024, T17 (mediane du salaire mensuel brut standardise, CITP a 2 chiffres) -------------
ESS = {}
for r in lirexlsx.lire(os.path.join(DL, "ofs", "ofs_36355238.bin"))["2024"]:
    if r and str(r[0]).strip().isdigit() and len(str(r[0]).strip()) == 2:
        ESS[str(r[0]).strip()] = (float(r[3]), r[1].strip())

CELL = json.load(open(os.path.join(DL, "cellules_v7.json"), encoding="utf-8"))

# --- Prix et change (v6, modele.py) ------------------------------------------------------------------
PLI_FR, PLI_CH, XR24, XR25, PRIME_GE = 111, 174, 0.9526, 0.933, 0.10
PPA = {"FR": 1.0, "CH": PLI_FR / (PLI_CH * XR24), "FR-GE": 1 / XR25 / (1 + PRIME_GE)}
NET_CH = 0.80          # v6 : Suisse x 0,80 (AVS, AC, LPP, AANP, LAMal)
INSEE_NET = 0.874      # v6 : revenus Insee des non-salaries, CSG et CRDS non deduites
LVL = {4: 5.0, 3: 11 / 3, 2: 7 / 3, 1: 1.0}


# --- Quantiles a partir des tranches publiees --------------------------------------------------------
def quantile(bornes, parts, q, med=None):
    """bornes : limites superieures des tranches finies ; parts : parts de chaque tranche (la derniere
    ouverte). Interpolation lineaire dans une tranche finie ; loi log-normale dans la tranche ouverte,
    ajustee sur la mediane publiee (ou sur les deux dernieres limites)."""
    parts = [p or 0.0 for p in parts]
    tot = sum(parts)
    parts = [p / tot for p in parts]
    cum, bas = 0.0, 0.0
    for i, b in enumerate(bornes):
        if cum + parts[i] >= q and parts[i] > 0:
            return bas + (b - bas) * (q - cum) / parts[i], "interpolée"
        cum += parts[i]
        bas = b
    F_haut = cum  # part sous la derniere limite finie
    b_haut = bornes[-1]
    if med is not None and abs(math.log(b_haut / med)) > 1e-9 and 0 < F_haut < 1:
        zb = Z.inv_cdf(F_haut)
        if zb != 0 and (math.log(b_haut / med) / zb) > 0:
            s = math.log(b_haut / med) / zb
            return med * math.exp(Z.inv_cdf(q) * s), "log-normale (médiane et part au-dessus de la tranche)"
    F_bas = F_haut - parts[len(bornes) - 1]
    b_bas = bornes[-2]
    if 0 < F_bas < F_haut < 1:
        z1, z2 = Z.inv_cdf(F_bas), Z.inv_cdf(F_haut)
        s = (math.log(b_haut) - math.log(b_bas)) / (z2 - z1)
        mu = math.log(b_haut) - z2 * s
        return math.exp(mu + Z.inv_cdf(q) * s), "log-normale (deux dernières limites)"
    return None, "non calculable"


B_SAL = [1500, 2000, 2500, 3000]
B_IND = [0.0001, 10000, 20000, 30000, 50000, 100000]


def lib_niveau(code, rang):
    return {0: f"métier {code}", 1: f"famille FAP 228 {code}", 2: f"famille FAP 86 {code}",
            3: f"domaine {code}"}[rang]


def revenu_fr_sal(c):
    m, cm, rm = dares(c, "med")
    dist, cd, rd = dares(c, "net")
    if m is None:
        return None
    med = 12 * m
    p80, meth = (None, "")
    if dist is not None:
        dd = DARES[cm]["net"] if DARES.get(cm, {}).get("net") else dist
        p80m, meth = quantile(B_SAL, dd, 0.8, med=m)
        p80 = 12 * p80m if p80m else None
    if not p80:
        p80, meth = 1.25 * med, "estimé (× 1,25)"
    fiab = "officielle" if rm == 0 else "officielle, groupe"
    src = (f"DARES, portraits statistiques des métiers 2023-2025, salaire mensuel net médian, "
           f"{lib_niveau(cm, rm)} : {m:,.0f} € × 12").replace(",", " ")
    return dict(med=med, p80=p80, cur="EUR", src=src, src_p80=f"DARES, tranches de salaire ({meth})", fiab=fiab,
                rang=rm, etp=False)


def revenu_fr_ind(c):
    dist, cd, rd = dares(c, "ind")
    cell = E.CELLULES_FR_IND.get(c)
    if cell and (dist is None or rd > 0):
        x = CELL[cell]
        return dict(med=x["med"], p80=x["p80"], cur="EUR", src=x["src_med"] + f" (cellule v7 {cell})",
                    src_p80=x["src_p80"], fiab=x["fiab"], rang=0, etp=bool(x.get("etp_ok")))
    if dist is None:
        return None
    med, m1 = quantile(B_IND, dist, 0.5)
    p80, m2 = quantile(B_IND, dist, 0.8, med=med)
    if not med or not p80:
        return None
    fiab = "officielle" if rd == 0 else "officielle, groupe"
    src = (f"DARES, portraits 2023-2025, revenus annuels d'activité des indépendants, {lib_niveau(cd, rd)} : "
           f"médiane {med:,.0f} € ({m1}) × 0,874").replace(",", " ")
    return dict(med=med * INSEE_NET, p80=p80 * INSEE_NET, cur="EUR", src=src,
                src_p80=f"DARES, tranches de revenu ({m2}) × 0,874", fiab=fiab, rang=rd, etp=False)


def revenu_ch_sal(c, isco, ratio):
    cell = E.CELLULES_CH_SAL.get(c)
    if cell:
        x = CELL[cell]
        return dict(med=x["med"], p80=x["p80"], cur="CHF", src=x["src_med"] + f" (cellule v7 {cell})",
                    src_p80=x["src_p80"], fiab=x["fiab"], rang=0, etp=True)
    m, nom = ESS[isco]
    med = m * 12 * NET_CH
    return dict(med=med, p80=med * ratio, cur="CHF",
                src=f"OFS, ESS 2024, T17 : groupe CITP {isco} « {nom} », médiane {m:,.0f} CHF/mois (EQTP 40 h) × 12 × 0,80".replace(",", " "),
                src_p80=f"estimé : rapport P80 / médiane du métier en France (× {ratio:.2f})", fiab="officielle, groupe CITP",
                rang=2, etp=True)


def revenu_ch_ind(c):
    cell = E.CELLULES_CH_IND.get(c)
    if not cell:
        return None
    x = CELL[cell]
    return dict(med=x["med"], p80=x["p80"], cur="CHF", src=x["src_med"] + f" (cellule v7 {cell})",
                src_p80=x["src_p80"], fiab=x["fiab"], rang=0, etp=bool(x.get("etp_ok")))


# --- Encodage ------------------------------------------------------------------------------------------
ENC = {}
for ligne in E.TABLE.strip().splitlines():
    f = ligne.split("|")
    ENC[f[0]] = dict(isco=f[1], lvl=int(f[2]), EP=int(f[3]), IT=int(f[4]), C=int(f[5]), R=int(f[6]),
                     F1=int(f[7]), flags=f[8], ind=[int(x) for x in f[9].split(",")] if f[9] else None)
manque = [c for c in METIERS if c not in ENC and PARENT228[c] not in ENC]
assert not manque, manque


def enc(c):
    return ENC.get(c) or ENC[PARENT228[c]]


def niveau_statut(rang):
    return "sourcée" if rang == 0 else "mixte"


def variantes(c):
    e = enc(c)
    st, cs, rs = dares(c, "statut")
    nonsal = (st[4] or 0.0) if st else 0.0
    sal_parts = [x or 0.0 for x in st[:4]] if st else [1, 0, 0, 0]
    prec = (sal_parts[1] + sal_parts[3]) / max(1e-9, sum(sal_parts))
    emp, ce, re_ = dares(c, "emp")
    public = (emp[0] or 0.0) if emp else 0.0
    at, ca_, ra = dares(c, "atyp")
    f3 = int(bool(at) and ((at[0] or 0) >= 0.40 or (at[1] or 0) >= 0.40))
    f3_stat = niveau_statut(ra) if at else "estimée"
    t228 = TENS.get(PARENT228[c])
    t_stat = "sourcée" if PARENT228[c] == c else "mixte"
    S, P, T, G, g = (x in e["flags"] for x in "SPTGg")
    out = []

    def notes(kind, EP, IT, C, R, F1):
        F3 = f3
        if (kind == "FR-ind" and G) or (kind == "CH-ind" and (G or g)):
            F3 = 1
        H = int(C <= 3)
        QT = max(1, 5 - F1 - F3 - H)
        CA = (C + LVL[e["lvl"]]) / 2
        # PS
        if S:
            PS, ps_st = 5, "estimée"
        elif kind == "FR-sal" and public >= 0.5 and prec < 0.30:
            PS, ps_st = 5, "mixte"
        elif kind in ("FR-sal", "CH-sal") and prec >= 0.30:
            PS, ps_st = 2, "mixte"
        elif kind == "CH-sal" and T:
            PS, ps_st = 5, "estimée"
        elif kind == "CH-sal" and public >= 0.5:
            PS, ps_st = 4, "estimée"
        elif t228 is None:
            PS, ps_st = 3, "estimée"
        elif kind in ("FR-ind", "CH-ind"):
            PS, ps_st = (3 if t228 >= 3 else 2), t_stat
        else:
            PS, ps_st = (4 if t228 >= 4 else 3), t_stat
        v = dict(EP=EP, IT=IT, QT=QT, ES=R, CA=CA, PS=PS, C=C, F1=F1, F3=F3, H=H)
        prov = dict(EP="estimée", IT="estimée", ES="estimée", CA="mixte", PS=ps_st,
                    QT="mixte" if f3_stat != "estimée" else "estimée")
        for d, x in E.ANCRAGES.get((c, kind), {}).items():
            v[d] = x
            prov[d] = "mixte"
        return v, prov

    base = (e["EP"], e["IT"], e["C"], e["R"], e["F1"])
    ind = e["ind"] or [e["EP"], e["IT"], 4, e["R"], e["F1"]]
    fr_sal = revenu_fr_sal(c) if (1 - nonsal) >= E.SEUIL_STATUT else None
    ratio = (fr_sal["p80"] / fr_sal["med"]) if fr_sal else 1.25
    if fr_sal:
        out.append(("FR-sal", "salarié", "France", "FR", fr_sal, *notes("FR-sal", *base)))
    if nonsal >= E.SEUIL_STATUT:
        r = revenu_fr_ind(c)
        if r:
            out.append(("FR-ind", "indépendant", "France", "FR", r, *notes("FR-ind", *ind)))
    if not P and (1 - nonsal) >= E.SEUIL_STATUT:
        r = revenu_ch_sal(c, e["isco"], ratio)
        out.append(("CH-sal", "salarié", "Suisse (résident)", "CH", r, *notes("CH-sal", *base)))
        out.append(("CH-sal", "salarié", "Suisse (frontalier, Genève)", "FR-GE", r, *notes("CH-sal", *base)))
    if not P and nonsal >= E.SEUIL_STATUT:
        r = revenu_ch_ind(c)
        if r:
            ib = list(ind)
            if c == "V2X90":
                ib[4] = 0  # medecins independants suisses : 43 h par semaine (v6 T30, S131)
            out.append(("CH-ind", "indépendant", "Suisse (résident)", "CH", r, *notes("CH-ind", *ib)))
    res = []
    for kind, statut, pays, resid, rev, v, prov in out:
        f = PPA[resid]
        rev = dict(rev)
        rev["med_ppa"], rev["p80_ppa"] = rev["med"] * f, rev["p80"] * f
        res.append(dict(metier=c, nom=NOM[c], kind=kind, statut=statut, pays=pays, resid=resid, rev=rev,
                        notes=v, prov=prov, nonsal=nonsal, public=public, prec=prec, tension=t228,
                        atyp=at, atyp_code=ca_))
    return res


V = [v for c in METIERS for v in variantes(c)]


def echelle(vals):
    lo, hi = min(vals), max(vals)
    return lo, hi, (lambda x: max(1.0, min(5.0, 1 + 4 * (math.log(x) - math.log(lo)) / (math.log(hi) - math.log(lo)))))


BM = echelle([v["rev"]["med_ppa"] for v in V])
BP = echelle([v["rev"]["p80_ppa"] for v in V])
DIMS6 = ("EP", "IT", "QT", "ES", "CA", "PS")
for v in V:
    v["RE"] = (BM[2](v["rev"]["med_ppa"]) + BP[2](v["rev"]["p80_ppa"])) / 2
    v["W"] = (sum(v["notes"][d] for d in DIMS6) + v["RE"]) / 7

MEILLEUR = {}
for v in V:
    b = MEILLEUR.get(v["metier"])
    if b is None or v["W"] > b["W"] + 1e-12:
        MEILLEUR[v["metier"]] = v
R = sorted(MEILLEUR.values(), key=lambda v: -v["W"])
for i, v in enumerate(R):
    v["rang_base"] = 1 + sum(1 for w in R if w["W"] > v["W"] + 1e-12)

# --- Monte Carlo, variante A de la v6 ------------------------------------------------------------------
N, GRAINE, TOP = 10_000, 20261029, 10
rng = np.random.default_rng(GRAINE)
k = len(R)
base = np.array([[v["notes"][d] for d in DIMS6] for v in R], dtype=float)
re_ = np.array([v["RE"] for v in R])
var = np.array([[v["prov"][d] == "estimée" for d in DIMS6] for v in R])
var[:, DIMS6.index("CA")] = False
p_top, p_1 = np.zeros(k), np.zeros(k)
rangs = np.zeros((N, k), dtype=np.int32)
for i in range(0, N, 500):
    n = min(500, N - i)
    ec = rng.integers(-1, 2, size=(n, k, len(DIMS6))).astype(float)
    notes = np.clip(base[None] + ec * var[None], 1, 5)
    s = (notes.sum(axis=2) + re_[None]) / 7
    r = np.empty((n, k), dtype=np.int32)
    for j in range(n):
        srt = np.sort(s[j])[::-1]
        r[j] = 1 + np.searchsorted(-srt, -s[j], side="left")
    rangs[i:i + n] = r
    p_top += (r <= TOP).sum(axis=0)
    tete = np.isclose(s, s.max(axis=1, keepdims=True), rtol=0, atol=1e-12)
    p_1 += (tete / tete.sum(axis=1, keepdims=True)).sum(axis=0)
for j, v in enumerate(R):
    v["p_top"], v["p_1"] = p_top[j] / N, p_1[j] / N
    v["r_med"] = int(np.median(rangs[:, j]))
    v["r_p5"], v["r_p95"] = int(np.percentile(rangs[:, j], 5)), int(np.percentile(rangs[:, j], 95))
    v["n_var"] = int(var[j].sum())

json.dump(dict(bornes=dict(med=BM[:2], p80=BP[:2]), n_variantes=len(V), classement=R), open(SORTIE, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1, default=float)
print("variantes", len(V), "metiers", len(R), "bornes med", [round(x) for x in BM[:2]], "p80", [round(x) for x in BP[:2]])
for v in sorted(R, key=lambda v: (-v["p_top"], -v["W"]))[:30]:
    n = v["notes"]
    print(f"{v['metier']:7} {v['nom'][:55]:55} {v['kind']:6} {v['resid']:5} W={v['W']:.3f} rang={v['rang_base']:3} "
          f"P10={v['p_top']:.3f} P1={v['p_1']:.3f} | EP{n['EP']} IT{n['IT']} QT{n['QT']} ES{n['ES']} CA{n['CA']:.2f} PS{n['PS']} RE{v['RE']:.2f} "
          f"| med {v['rev']['med_ppa']:,.0f}".replace(",", " "))
