# -*- coding: utf-8 -*-
"""Version 7 (29 octobre 2026) : classement 2, triplets dans les 10 pays retenus par le tri (pays_v7).

Regles declarees en section 1.15 du rapport (avant ce calcul) :
- postes : ceux dont un triplet est dans les 30 premiers du classement 1, plus les fonctionnaires
  internationaux ; controle : un poste exclu dont le score maximal possible (RE = 5, sans penalite de
  langue) atteint le 10e score du classement 2 est ajoute et le calcul refait ;
- la Suisse entre avec tous ses triplets du classement 1 ; les autres pays avec les postes retenus, au
  statut francais ou suisse du poste (specialites liberales seulement en DE, AT, LU, NL) ;
- notes : celles du meilleur triplet du poste au classement 1, ES moins 1 hors pays francophones (1.10) ;
- revenu : donnee lue (REVENUS_LUS) ou regle de structure (rapport au salaire moyen en France et en
  Suisse, x salaire moyen OCDE du pays ; plafond 5 pour une specialite), puis impot du pays.
"""
import math

import fiscalite_v7 as F
import modele as M6
import modele_v7 as M7
import pays_v7 as PV
import postes_v7 as P
from revenus import LAMAL, P80_LIB

PAYS2 = list(PV.RETENUS)
NOMS = PV.NOMS
FRANCOPHONES = {"CH", "LU"}
EWCTS_ABSENT = {"IS", "GB"}  # pays non couverts par l'enquete europeenne 2021 (EWCTS)

# Salaire moyen 2025 de l'OCDE (Taxing Wages 2026, monnaie locale) : valeur, provenance.
AW = {"FR": (45964, "relayé (OCDE via Euronews, S167)"), "CH": (100700, "imputé : 107 487 € (OCDE via Euronews) × 0,937"),
      "DE": (66700, "lu (S167)"), "LU": (77844, "lu (S167)"), "NL": (69028, "relayé (S167)"), "AT": (63054, "lu (S167)"),
      "DK": (537071, "lu (S167)"), "IS": (12433527, "lu (S167)"), "GB": (55983, "lu (S167)"),
      "NO": (801695, "relayé (S167)"), "SI": (31000, "imputé : 53 697 USD PPA (S167), parité estimée")}
CUR = {"NL": "EUR", "NO": "NOK", "DE": "EUR", "LU": "EUR", "IS": "ISK", "DK": "DKK", "GB": "GBP", "SI": "EUR",
       "AT": "EUR", "CH": "CHF", "FR": "EUR"}
PLI = {"FR": 111, "DE": 109, "LU": 133, "AT": 111.7, "DK": 143, "IS": 162, "NO": 124, "NL": 118, "SI": 90, "GB": 115,
       "CH": 174}
PLI_PROV = {"NL": "connu", "SI": "connu", "GB": "connu", "DE": "v6 (Eurostat 2024) ; 108,3 relayé (S190)", "FR": "v6 (Eurostat 2024)",
            "LU": "lu (S190)", "CH": "lu (S190)", "AT": "lu (S190)", "DK": "lu (S190)", "IS": "lu (S190)", "NO": "lu (S190)"}
XR24 = {"EUR": 1.0, "NOK": 11.6290, "DKK": 7.4589, "GBP": 0.84662, "ISK": 149.31, "CHF": 0.9526}
XR25 = {"EUR": 1.0, "NOK": 11.7182, "DKK": 7.4634, "GBP": 0.85687, "ISK": 144.66, "CHF": 0.933}


def ppa(pays, resid):
    if resid == "FR-LO":
        return 1.0 / (1 + M6.PRIME_REGION["FR-LO"])
    return PLI["FR"] / (PLI[pays] * XR24[CUR[pays]])


def nominal(pays):
    return 1.0 / XR25[CUR[pays]]


# ---------------------------------------------------------------------------
# Postes retenus
# ---------------------------------------------------------------------------
SPECIALITES = {"Radiologue", "Ophtalmologue", "Anesthésiste-réanimateur", "Anatomopathologiste",
               "Cancérologue (oncologie médicale et radiothérapie)", "Médecin nucléaire", "Gastro-entérologue",
               "Cardiologue", "Dermatologue", "Gynécologue-obstétricien", "Rhumatologue", "Psychiatre", "Pédiatre"}
PAYS_LIBERAL_SPE = {"DE", "AT", "LU", "NL"}
NOTAIRE_PAYS = {"DE", "AT", "NL", "LU", "SI"}  # notariat de type latin
FONCTIONNAIRE_PROTEGE = {"DE", "AT", "LU"}
canon, type_statut, cle = P.canon, P.type_statut, P.cle


def selection(classement, rang_max=30):
    cles = []
    for t in classement:
        if t["rang"] <= rang_max and cle(t) not in cles:
            cles.append(cle(t))
    return cles


# Rapports au salaire moyen en France et en Suisse, par poste (structure).
def rapports(cle_poste):
    fr, ch, p80r = [], [], []
    for t in M7.R1:
        if cle(t) != cle_poste:
            continue
        if t["pays"] == "FR":
            fr.append(t["med"] / 0.78 / AW["FR"][0])
        else:
            ch.append(t["med"] / 0.80 / AW["CH"][0])
        p80r.append(t["p80"] / t["med"])
    vals = []
    if fr:
        vals.append(sum(fr) / len(fr))
    if ch:
        vals.append(sum(ch) / len(ch))
    r = math.exp(sum(math.log(v) for v in vals) / len(vals))
    q = math.exp(sum(math.log(v) for v in p80r) / len(p80r))
    pays_src = "+".join(p for p, v in (("FR", fr), ("CH", ch)) if v)
    return r, q, pays_src


def meilleur(cle_poste):
    return min((t for t in M7.R1 if cle(t) == cle_poste), key=lambda t: (t["rang"], t["id"]))


# Donnees lues (remplacent la structure) : (poste canonique, pays) -> brut median, brut P80 (ou None : rapport
# P80 / median du poste), source, fiabilite, fonction de passage au net.
REVENUS_LUS = {
    ("Médecin généraliste (médecin de famille)", "indépendant", "DE"): (
        218000, None, "Destatis 2023 relayé (S188) : médecine générale, revenu net de cabinet (Reinertrag) médian 218 000 € par cabinet",
        "relayée (par cabinet, site secondaire)", "de_indep"),
    ("Médecin généraliste (médecin de famille)", "indépendant", "GB"): (
        140200 * 0.85, None, "NHS Digital 2022/23 relayé (S187) : généralistes associés (contractors), revenu moyen avant impôt 140 200 £ ; "
        "médiane = moyenne × 0,85 (règle 1.4)", "relayée (moyenne, 2022/23)", "salarie"),
    ("Médecin spécialiste hospitalier (grille commune aux spécialités)", "salarié", "NO"): (
        122980 * 12, None, "SSB, tableau 13848, 4e trimestre 2025 (S184) : médecins spécialistes à temps plein, 122 980 NOK par mois",
        "officielle (moyenne)", "salarie"),
    ("Médecin spécialiste hospitalier (grille commune aux spécialités)", "salarié", "DK"): (
        101900 * 12 * 0.90, 122500 * 12 * 0.90,
        "Danmarks Statistik 2024 relayé (S185) : overlæger, quartiles 87 932 et 118 110 DKK par mois, retraite comprise ; "
        "médiane log 101 900 ; × 0,90 (part patronale de retraite, estimée)", "relayée", "salarie"),
    ("Médecin spécialiste hospitalier (grille commune aux spécialités)", "salarié", "GB"): (
        127600, 145478, "NHS, barème des consultants 2025/26 (connu, hausse de 4 % confirmée, S187) : 109 725 à 145 478 £ ; milieu",
        "connue (grille)", "salarie"),
    ("Développeur logiciel", "salarié", "NO"): (
        77420 * 12, None, "SSB 2025 relayé (S184) : développeurs de logiciels, médiane 77 420 NOK par mois (moyenne 81 050)",
        "relayée (site secondaire)", "salarie"),
    ("Développeur logiciel", "salarié", "GB"): (
        56914, None, "ONS, ASHE 2025 relayé (S187) : programmeurs et développeurs, médiane 56 914 £ à temps plein",
        "relayée (site secondaire)", "salarie"),
    ("Développeur logiciel", "salarié", "NL"): (
        6032 * 12 * 1.08, None, "CBS 2024 relayé (S186) : développeur de logiciels, médiane 6 032 € par mois à 40 h ; × 12 × 1,08 (pécule de vacances)",
        "relayée (site secondaire)", "salarie"),
    ("Développeur logiciel", "salarié", "DE"): (
        6114 * 12, None, "Bundesagentur für Arbeit (S33) : informatique, médiane 6 114 € brut par mois à temps plein",
        "relayée", "salarie"),
}
HOSP = "Médecin spécialiste hospitalier (grille commune aux spécialités)"
PAYS_HOSP = ("NO", "DK", "GB", "IS", "SI")


def net_fonction(pays, mode):
    if mode == "de_indep":
        return F.net_de_indep
    return F.NET_PAYS[pays]


def triplet(base, pays, resid, poste=None, statut=None, cellule=None, ident=None):
    """Transpose le triplet de base (classement 1) dans un pays du classement 2."""
    t = {k: v for k, v in base.items() if k in (
        "src", "citp", "niveau", "C", "R", "Se", "EP", "IT", "groupe", "ia", "L", "anc_extra", "anc_exclus",
        "anc_partiel", "just")}
    t["fx"] = set(base["fx"]) - {"F5"} | ({"F5"} if resid == "FR-LO" else set())
    t["poste"] = poste or canon(base)
    t["statut"] = statut or type_statut(base)
    t["pays"], t["resid"], t["cur"] = pays, resid, CUR[pays]
    t["langue"] = 0 if pays in FRANCOPHONES else 1
    t["base"] = base["id"]
    t["cle_mc"] = "|".join(cle(base)) if poste is None else poste
    if t["statut"] == "fonctionnaire":
        t["statut"] = "fonctionnaire" if pays in FONCTIONNAIRE_PROTEGE else "salarié du secteur public"
        if pays not in FONCTIONNAIRE_PROTEGE:
            t["Se"] = max(1, t["Se"] - 1)
    t.update(cellule)
    t["ppa"], t["nominal"] = ppa(pays, resid), nominal(pays)
    t["id"] = ident
    t["exonere"] = False
    return t


def cellule_structure(cle_poste, pays, specialite):
    r, q, src = rapports(cle_poste)
    plafond = specialite and r > 5
    r_eff = min(r, 5.0) if specialite else r
    brut = r_eff * AW[pays][0]
    return dict(med=round(brut, -2), p80=round(brut * q, -2), fiscal="brut_" + pays, net_de_brut=F.NET_PAYS[pays],
                src_med=f"estimé (structure) : rapport au salaire moyen {r:.2f} ({src})" + (", plafonné à 5" if plafond else "")
                        + f" × salaire moyen OCDE 2025 ({AW[pays][0]:,} {CUR[pays]}, {AW[pays][1]})".replace(",", " "),
                src_p80=f"estimé : rapport P80 / médiane du poste ({q:.2f})", fiab="estimé (structure)",
                h="non trouvé", q=1.0, etp="règle de structure (temps plein)", etp_ok=False, rapport=r_eff)


def cellule_lue(cle_poste, pays):
    med, p80, src, fiab, mode = REVENUS_LUS[(cle_poste[0], cle_poste[1], pays)]
    if p80 is None:
        q = P80_LIB if mode == "de_indep" or "contractors" in src else rapports(cle_poste)[1] if cle_poste[0] != HOSP else 1.2
        p80 = med * q
        src_p80 = f"estimé : rapport P80 / médiane ({q:.2f})"
    else:
        src_p80 = "même source"
    return dict(med=round(med, -2), p80=round(p80, -2), fiscal="brut_" + pays, net_de_brut=net_fonction(pays, mode),
                src_med=src, src_p80=src_p80, fiab=fiab, h="non trouvé", q=1.0, etp="source à temps plein", etp_ok=True,
                rapport=med / AW[pays][0])


def construire(cles):
    T = []
    for t in M7.R1:  # Suisse : tous ses triplets du classement 1
        if t["pays"] == "CH":
            c = {k: v for k, v in t.items() if k not in ("mc", "rangs_var", "prov", "modifs")}
            c["base"] = t["id"]
            c["langue"] = 0
            c["cle_mc"] = t["cle_mc"]
            T.append(c)
    n = 0
    for cp in cles:
        base = meilleur(cp)
        spe = cp[0] in SPECIALITES
        for pays in PAYS2:
            if pays == "CH":
                continue
            if spe and pays not in PAYS_LIBERAL_SPE:
                continue
            if cp[0] == "Notaire" and pays not in NOTAIRE_PAYS:
                continue
            residences = [pays] + (["FR-LO"] if pays == "LU" and cp[1] in ("salarié",) else [])
            for resid in residences:
                cel = cellule_lue(cp, pays) if (cp[0], cp[1], pays) in REVENUS_LUS else cellule_structure(cp, pays, spe)
                n += 1
                T.append(triplet(base, pays, resid, cellule=cel, ident=f"M{n:03d}"))
    # Specialistes hospitaliers la ou l'exercice liberal des specialistes n'est pas courant.
    t04 = next(t for t in M7.R1 if t["id"] == "T04")
    for pays in PAYS_HOSP:
        cp = (HOSP, "salarié")
        if (HOSP, "salarié", pays) in REVENUS_LUS:
            cel = cellule_lue(cp, pays)
        else:
            r = math.exp((math.log(83100 / 0.78 / AW["FR"][0]) + math.log(163600 / 0.80 / AW["CH"][0])) / 2)
            brut = r * AW[pays][0]
            cel = dict(med=round(brut, -2), p80=round(brut * 1.2, -2), fiscal="brut_" + pays, net_de_brut=F.NET_PAYS[pays],
                       src_med=f"estimé (structure) : rapport au salaire moyen {r:.2f} (FR praticien hospitalier, CH médecin hospitalier)"
                               f" × salaire moyen OCDE 2025 ({AW[pays][0]:,} {CUR[pays]})".replace(",", " "),
                       src_p80="estimé : amplitude de grille (× 1,2)", fiab="estimé (structure)", h="non trouvé", q=1.0,
                       etp="règle de structure (temps plein)", etp_ok=False, rapport=r)
        n += 1
        T.append(triplet(t04, pays, pays, poste=HOSP, statut="salarié (hôpital)", cellule=cel, ident=f"M{n:03d}"))
    # Fonctionnaire europeen a Luxembourg (T64 de la v6) : impot de l'UE estime a 18 %.
    t64 = M6.T[[t["id"] for t in M6.T].index("T64")]
    import eurofound as EU
    from revenus import REV
    r64 = REV["T64"]
    base64 = dict(src="T64", citp="2422", niveau=4, C=t64["C"], R=t64["R"], Se=t64["Se"], EP=5, IT=3,
                  groupe="bureau_cadre", ia=t64["ia"], L=t64["L"], anc_extra=[], anc_exclus=[], anc_partiel=[], just="",
                  fx=set(EU.FACTEURS["T64"].split()), poste="Administrateur (AD), institutions de l'Union européenne",
                  statut="fonctionnaire européen", id="T64")
    cel = dict(med=r64["med"], p80=r64["p80"], fiscal="brut_UE", net_de_brut=lambda x: F.impot_ue(x, 0.18),
               src_med=r64["src_med"] + " ; impôt de l'UE et prélèvement de solidarité : 18 % (estimé)",
               src_p80=r64["src_p80"], fiab="relayée (grille), impôt estimé", h=r64["h"], q=1.0, etp="grille à temps plein",
               etp_ok=True, rapport=r64["med"] / AW["LU"][0])
    n += 1
    T.append(triplet(base64, "LU", "LU", poste=base64["poste"], statut="fonctionnaire européen", cellule=cel,
                     ident=f"M{n:03d}"))
    return T


def max_possible(cp):
    t = meilleur(cp)
    return (sum(t[d] for d in ("EP", "IT", "QT", "ES", "CA", "PS")) + 5) / 7


def calculer():
    cles = selection(M7.CLASSEMENT1)
    ajoutes = []
    while True:
        T = construire(cles)
        M7.preparer(T)
        B = M7.bornes(T)
        cl = M7.classer(T, B)
        seuil = cl[TOP - 1]["W"]
        tous = []
        for t in M7.R1:
            if cle(t) not in tous:
                tous.append(cle(t))
        nouveaux = [cp for cp in tous if cp not in cles and max_possible(cp) >= seuil]
        if not nouveaux:
            return T, B, cl, cles, ajoutes, seuil
        ajoutes += nouveaux
        cles += nouveaux


TOP = M7.TOP
R2, B2, CLASSEMENT2, CLES2, AJOUTES2, SEUIL2 = calculer()
MC2 = M7.robustesse(R2, B2)
PREMIER2 = M7.premier(R2)
# Sensibilite (informatif) : sans la regle de langue.
for _t in R2:
    _t["W_sans_langue"] = M7.score(dict(_t, ES=_t["ES"] + _t["langue"]))
RANG_SANS_LANGUE = M6.rangs_partages(R2, cle="W_sans_langue")

if __name__ == "__main__":
    print("Postes retenus :", len(CLES2), "dont ajoutés par le contrôle :", len(AJOUTES2), AJOUTES2)
    print("Triplets :", len(R2), "seuil du 10e :", round(SEUIL2, 3))
    print("Bornes :", {k: (round(a), round(b)) for k, (a, b) in B2.items()})
    for i, t in enumerate(CLASSEMENT2[:40], 1):
        mc = t["mc"]
        print(f"{i:3d} {t['id']:5s} {t['poste'][:40]:40s} {t['statut'][:12]:12s} {t['pays']}/{t['resid']:5s} W {t['W']:.3f} "
              f"RE {t['RE']:.2f} ai {t['med_ai_ppa'] / 1000:.0f}/{t['p80_ai_ppa'] / 1000:.0f}k ES {t['ES']} "
              f"| A {mc['A']['p_top']:.2f}/{mc['A']['p_1']:.3f} D {mc['D']['p_top']:.2f} sans langue {RANG_SANS_LANGUE[t['id']][0]} [{t['fiab'][:22]}]")
    print("Premier :", PREMIER2["id"] if PREMIER2 else "aucun")
