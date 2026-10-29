# -*- coding: utf-8 -*-
"""Version 7 (29 octobre 2026) : calcul des deux classements (regles de la section 1.15 du rapport).

Classement 1 : triplets France et Suisse de postes_v7.R1. Classement 2 : triplets des 10 pays retenus par
le tri de pays_v7, construits dans classement2_v7.py. Methode commune :
- notes hors revenu : notes_v7.ancrer (methode v6) ;
- revenu : cellule nette de cotisations, moins l'impot sur le revenu (fiscalite_v7), en equivalent temps
  plein, en PPA au niveau des prix francais (facteurs de modele.py) ; RE = moyenne de deux notes
  logarithmiques (mediane et P80) bornees par le minimum et le maximum du classement ;
- score = moyenne des 7 dimensions (poids egaux) ; paliers S, A, B, C ; rangs partages a 0,03 ;
- robustesse : 8 ponderations et 10 000 tirages (variantes A, B, C de la v6, D sur le revenu).
"""
import math

import numpy as np

import eurofound as EU
import fiscalite_v7 as F
import modele as M6
import notes_v7 as N

DIMS = EU.DIMS
DIMS6 = N.DIMS6
POIDS = {d: 1 for d in DIMS}
VARIANTES_POIDS = {"Poids égaux": POIDS}
for _d in DIMS:
    VARIANTES_POIDS[f"{EU.NOMS_DIMS[_d]} doublé"] = {d: (2 if d == _d else 1) for d in DIMS}
TOP = 10
N_TIRAGES = 10_000
GRAINE = 20261029
IA_FORT = M6.IA_FORT

# Mots qui designent une cellule revenu incertaine (variante D : +/- 20 % au lieu de +/- 5 %).
INCERTAIN = ("non officielle", "non re-sourcée", "proxy", "estim", "ancienne", "année", "site secondaire",
             "champ plus large", "structure", "groupe", "2024")


def incertaine(t):
    return any(m in t["fiab"] for m in INCERTAIN)


def apres_impot(t, x):
    """Revenu net d'impot sur le revenu, en devise locale, pour une cellule nette de cotisations x."""
    f = t["fiscal"]
    if f == "exonere":
        return x
    if f == "salarie_fr":
        return F.apres_impot_fr(x, False)
    if f == "liberal_fr":
        return F.apres_impot_fr(x, True)
    if f == "salarie_ch":
        return F.apres_impot_ch(x, False)
    if f == "independant_ch":
        return F.apres_impot_ch(x, True)
    if f.startswith("brut_"):  # classement 2 : x est un brut, fonction du pays
        return t["net_de_brut"](x)
    raise ValueError(f)


def facteur_ppa(t):
    if "ppa" in t:
        return t["ppa"]
    return M6.facteur_ppa(t["cur"], t["resid"])


def facteur_nominal(t):
    if "nominal" in t:
        return t["nominal"]
    return M6.facteur_nominal(t["cur"])


def preparer(T):
    """Notes ancrees et revenus apres impot, ETP, PPA."""
    for t in T:
        d, t["prov"], t["modifs"] = N.ancrer(t)
        t.update(d)
        fp, fn = facteur_ppa(t), facteur_nominal(t)
        for cle, src in (("med", "med"), ("p80", "p80")):
            ai = apres_impot(t, t[src])
            t[f"{cle}_ai"] = ai
            t[f"{cle}_ai_nom"] = ai * fn / t["q"]
            t[f"{cle}_ai_ppa"] = ai * fp / t["q"]
            t[f"{cle}_av_ppa"] = t[src] * fp / t["q"]
        t["taux_impot"] = 1 - t["med_ai"] / t["med"] if t["med"] else 0.0


def bornes(T):
    return {k: (min(t[k] for t in T), max(t[k] for t in T)) for k in ("med_ai_ppa", "p80_ai_ppa")}


def note_log(x, lo, hi):
    return max(1.0, min(5.0, 1 + 4 * (math.log(x) - math.log(lo)) / (math.log(hi) - math.log(lo))))


def note_re(t, B, mult=1.0):
    return sum(note_log(t[k] * mult, *B[k]) for k in ("med_ai_ppa", "p80_ai_ppa")) / 2


def score(v, P=POIDS):
    return sum(P[d] * v[d] for d in P) / sum(P.values())


def classer(T, B):
    for t in T:
        t["RE"] = note_re(t, B)
        t["W"] = score(t)
        t["palier"] = M6.classer(t["W"])
        t["proche"] = M6.proche_frontiere(t["W"])
        # Scenario IA fort (informatif) : perspectives moins 1 ou 2 et revenu brut x 0,9 ou x 0,8.
        d_se, mult = IA_FORT[t["ia"]]
        if "fonctionnaire" in t["statut"]:
            d_se = max(0, d_se - 1)
        med_ia = apres_impot(t, t["med"] * mult) * facteur_ppa(t) / t["q"]
        p80_ia = apres_impot(t, t["p80"] * mult) * facteur_ppa(t) / t["q"]
        re_ia = (note_log(med_ia, *B["med_ai_ppa"]) + note_log(p80_ia, *B["p80_ai_ppa"])) / 2
        t["W_ia"] = score(dict(t, PS=max(1, t["PS"] - d_se), RE=re_ia))
        t["palier_ia"] = M6.classer(t["W_ia"])
        t["W_tension"] = score(dict(N.variante_tensions(t, {d: t[d] for d in DIMS6}), RE=t["RE"]))
    rg = M6.rangs_partages(T)
    for t in T:
        t["rang"], t["groupe_eg"] = rg[t["id"]]
    for nom, P in VARIANTES_POIDS.items():
        for t in T:
            t["_w"] = score(t, P)
        r = M6.rangs_partages(T, cle="_w")
        for t in T:
            t.setdefault("rangs_var", {})[nom] = r[t["id"]][0]
    for t in T:
        t.pop("_w", None)
        t["nb_top"] = sum(1 for r in t["rangs_var"].values() if r <= TOP)
        t["rang_min"], t["rang_max"] = min(t["rangs_var"].values()), max(t["rangs_var"].values())
    rt = M6.rangs_partages(T, cle="W_tension")
    for t in T:
        t["rang_tension"] = rt[t["id"]][0]
    return sorted(T, key=lambda t: (-t["W"], t["id"]))


VARIANTES_MC = {"A": "notes estimées, tirages indépendants (consigne)",
                "B": "notes estimées, EP et IT communs au groupe de postes",
                "C": "notes estimées et mixtes, CA à ± 0,5",
                "D": "notes estimées comme en A et revenu à ± 20 % (cellule incertaine) ou ± 5 %",
                "E": "notes estimées, écart commun à toutes les occurrences d'un même poste (informatif)"}


def tirages(T, B, variante, n=N_TIRAGES, graine=GRAINE, top=TOP):
    rng = np.random.default_rng(graine)
    k = len(T)
    base = np.array([[t[d] for d in DIMS6] for t in T], dtype=float)
    statut = np.array([[t["prov"][d][0] for d in DIMS6] for t in T])
    variable = (statut == "estimée") if variante in ("A", "B", "D", "E") else (statut != "sourcée")
    if variante != "C":
        variable[:, DIMS6.index("CA")] = False
    pas = np.ones((k, len(DIMS6)))
    if variante == "C":
        pas[:, DIMS6.index("CA")] = 0.5
    ecarts = rng.integers(-1, 2, size=(n, k, len(DIMS6))).astype(float)
    if variante == "B":
        groupes = sorted({t["groupe"] for t in T})
        idx = np.array([groupes.index(t["groupe"]) for t in T])
        commun = rng.integers(-1, 2, size=(n, len(groupes), 2)).astype(float)
        ecarts[:, :, 0] = commun[:, idx, 0]
        ecarts[:, :, 1] = commun[:, idx, 1]
    if variante == "E":
        cles = sorted({t["cle_mc"] for t in T})
        idx = np.array([cles.index(t["cle_mc"]) for t in T])
        ecarts = rng.integers(-1, 2, size=(n, len(cles), len(DIMS6))).astype(float)[:, idx, :]
    notes = np.clip(base[None, :, :] + ecarts * pas[None, :, :] * variable[None, :, :], 1, 5)
    if variante == "D":
        amp = np.array([0.20 if incertaine(t) else 0.05 for t in T])
        mult = 1 + rng.uniform(-1, 1, size=(n, k)) * amp[None, :]
        med = np.array([t["med_ai_ppa"] for t in T])[None, :] * mult
        p80 = np.array([t["p80_ai_ppa"] for t in T])[None, :] * mult

        def nl(x, lo, hi):
            return np.clip(1 + 4 * (np.log(x) - math.log(lo)) / (math.log(hi) - math.log(lo)), 1, 5)
        re_ = (nl(med, *B["med_ai_ppa"]) + nl(p80, *B["p80_ai_ppa"])) / 2
    else:
        re_ = np.array([t["RE"] for t in T], dtype=float)[None, :]
    scores = (notes.sum(axis=2) + re_) / 7
    p_top = np.zeros(k)
    p_1 = np.zeros(k)
    rangs = np.zeros((n, k), dtype=np.int32)
    for i in range(0, n, 500):
        s = scores[i:i + 500]
        r = (s[:, None, :] > s[:, :, None]).sum(axis=2) + 1
        rangs[i:i + 500] = r
        p_top += (r <= top).sum(axis=0)
        en_tete = np.isclose(s, s.max(axis=1, keepdims=True), rtol=0, atol=1e-12)
        p_1 += (en_tete / en_tete.sum(axis=1, keepdims=True)).sum(axis=0)
    out = {}
    for j, t in enumerate(T):
        out[t["id"]] = {"p_top": p_top[j] / n, "p_1": p_1[j] / n, "r_med": int(np.median(rangs[:, j])),
                        "r_p5": int(np.percentile(rangs[:, j], 5)), "r_p95": int(np.percentile(rangs[:, j], 95)),
                        "n_var": int(variable[j].sum())}
    return out


def robustesse(T, B):
    mc = {v: tirages(T, B, v) for v in VARIANTES_MC}
    for t in T:
        t["mc"] = {v: mc[v][t["id"]] for v in mc}
    return mc


def premier(T):
    """Regle 1.15 : un 1er n'est designe que si un triplet est premier dans plus de 50 % des tirages (A)."""
    best = max(T, key=lambda t: t["mc"]["A"]["p_1"])
    return best if best["mc"]["A"]["p_1"] > 0.5 else None


# ---------------------------------------------------------------------------
# Classement 1
# ---------------------------------------------------------------------------
import postes_v7 as P  # noqa: E402

R1 = P.R1
preparer(R1)
B1 = bornes(R1)
CLASSEMENT1 = classer(R1, B1)
MC1 = robustesse(R1, B1)
PREMIER1 = premier(R1)

if __name__ == "__main__":
    print("Bornes classement 1 :", {k: (round(a), round(b)) for k, (a, b) in B1.items()})
    for i, t in enumerate(CLASSEMENT1[:40], 1):
        mc = t["mc"]
        print(f"{i:3d} {t['id']:5s} {t['poste'][:44]:44s} {t['statut'][:14]:14s} {t['pays']}/{t['resid']:5s} "
              f"W {t['W']:.3f} {t['palier']} RE {t['RE']:.2f} ai {t['med_ai_ppa'] / 1000:.0f}/{t['p80_ai_ppa'] / 1000:.0f}k "
              f"impôt {100 * t['taux_impot']:.0f}% | A {mc['A']['p_top']:.2f}/{mc['A']['p_1']:.3f} B {mc['B']['p_top']:.2f} "
              f"C {mc['C']['p_top']:.2f} D {mc['D']['p_top']:.2f}/{mc['D']['p_1']:.3f} top8 {t['nb_top']}")
    print("Premier désigné :", PREMIER1["id"] if PREMIER1 else "aucun")
