# -*- coding: utf-8 -*-
"""Version 7.1 : classement monde, ajout des Etats-Unis, du Canada (Quebec), de l'Australie, de Singapour et des
Emirats pour les 10 premiers codes du classement 2 recalcule (codes_v7_1).

Regles (consigne du 29 octobre) :
- revenu lu dans une source nommee (donnees deja collectees ou au plus 20 recherches) ; sinon cellule vide,
  variante non classee et signalee ; une source modelisee, non attribuee ou contredite par une autre est refusee ;
- notes : triplet v6 du meme code dans le pays quand il existe (T93, T90, T92, T32), sinon meilleure variante du
  code au classement 1 de meme type de statut (salarie ou fonctionnaire / independant), sinon meilleure variante
  du code ; 2266 salarie : orthophoniste salarie T93 (le salarie francais du code est un audioprothesiste) ;
  aucune regle de langue ;
- impot : baremes 2025 simplifies ci-dessous ; prix : niveaux des prix declares ci-dessous.
"""
import copy
import math

import eurofound as EU
import fiscalite_v7 as F
import modele as M6
import codes_v7_1 as K
from revenus import p80_interp, p80_ln

_b = F._bareme


# --- Impot et cotisations, celibataire, 2025 (simplifie) --------------------------------------------------
def us_fed(imposable):
    return _b(max(0.0, imposable), [(0, .10), (11925, .12), (48475, .22), (103350, .24), (197300, .32),
                                    (250525, .35), (626350, .37)])


def us_net(g):
    """Salarie : FICA, impot federal (deduction forfaitaire 15 750 USD), Etat et local 5 % (hypothese),
    part salariale d'assurance sante 1,5 % (regle v4)."""
    fica = 0.062 * min(g, 176100) + 0.0145 * g + 0.009 * max(0.0, g - 200000)
    imp = max(0.0, g - 15750)
    return g - fica - us_fed(imp) - 0.05 * imp - 0.015 * g


def us_net_indep(g):
    """Proprietaire : cotisation des independants, assurance sante 7 000 USD (regle v4), impots comme us_net."""
    b = 0.9235 * g
    se = 0.124 * min(b, 176100) + 0.029 * b + 0.009 * max(0.0, b - 200000)
    imp = max(0.0, g - se / 2 - 15750)
    return g - se - 7000 - us_fed(imp) - 0.05 * imp


def _ca_fed(x):
    t = _b(x, [(0, .145), (57375, .205), (114750, .26), (177882, .29), (253414, .33)])
    return max(0.0, t - 0.145 * 16129) * (1 - 0.165)  # abattement du Quebec


def _qc(x):
    return max(0.0, _b(x, [(0, .14), (53255, .19), (106495, .24), (129590, .2575)]) - 0.14 * 18571)


def ca_net(g):
    """Quebec, salarie : RRQ, assurance emploi, RQAP, impots federal et quebecois."""
    cot = (0.064 * max(0.0, min(g, 71300) - 3500) + 0.04 * max(0.0, min(g, 81200) - 71300)
           + 0.0131 * min(g, 65700) + 0.00494 * min(g, 98000))
    return g - cot - max(0.0, _ca_fed(g) - 0.145 * cot * 0.835) - max(0.0, _qc(g) - 0.14 * cot)


def ca_net_indep(g):
    """Quebec, medecin remunere par la RAMQ : g = revenu apres frais ; RRQ et RQAP des autonomes 9 900 CAD (v6)."""
    cot = 9900
    imp = g - cot / 2
    return g - cot - _ca_fed(imp) - _qc(imp)


def au_net(g):
    return g - _b(g, [(0, 0), (18200, .16), (45000, .30), (135000, .37), (190000, .45)]) - 0.02 * g


def sg_net(g):
    """Etranger titulaire d'un permis de travail : pas de CPF ; bareme des residents fiscaux."""
    return g - _b(g, [(0, 0), (20000, .02), (30000, .035), (40000, .07), (80000, .115), (120000, .15),
                      (160000, .18), (200000, .19), (240000, .195), (280000, .20), (320000, .22), (500000, .23),
                      (1000000, .24)])


def ae_net(g):
    return g


NET = {"US": us_net, "CA": ca_net, "AU": au_net, "SG": sg_net, "AE": ae_net}
CUR = {"US": "USD", "CA": "CAD", "AU": "AUD", "SG": "SGD", "AE": "AED"}
# Niveaux des prix (UE = 100) : Etats-Unis et Canada comme en v6 (estimes a partir des niveaux de prix de l'OCDE) ;
# Australie, Singapour, Emirats = niveau des Etats-Unis x niveau relatif de la consommation des menages (Banque
# mondiale, Etats-Unis = 100) : 96 (relaye, en conflit avec une autre source), 78 (relaye) ; Emirats : parite de la
# consommation privee 2,66 AED par dollar international (2020, relaye, S200) / 3,6725 AED par USD = 72,4.
PLI = {"US": M6.PLI["US"], "CA": M6.PLI["CA"], "AU": M6.PLI["US"] * 0.96, "SG": M6.PLI["US"] * 0.78,
       "AE": M6.PLI["US"] * 2.66 / 3.6725}
XR24 = {"USD": 1.0824, "CAD": 1.4821, "AUD": 1.6397, "SGD": 1.4458, "AED": 1.0824 * 3.6725}
XR25 = {"USD": 1.13, "CAD": 1.619, "AUD": 1.6397, "SGD": 1.4458, "AED": 1.13 * 3.6725}

PAYS_NOUVEAUX = ("US", "CA", "AU", "SG", "AE")
NOMS = {"US": "États-Unis", "CA": "Canada (Québec)", "AU": "Australie", "SG": "Singapour", "AE": "Émirats arabes unis"}


def depuis_v6(src):
    """Triplet v6 hors France et Suisse, sous la forme des variantes v7 (relations sans la malus de langue)."""
    t = next(x for x in M6.T if x["id"] == src)
    groupe, ep, it = EU.groupe_de(src)
    return dict(src=src, citp=EU.CITP[src][0], niveau=EU.CITP[src][1], C=t["C"],
                R=t["R"] + (1 if src in EU.LANGUE else 0), Se=t["Se"], fx=set(EU.FACTEURS[src].split()) - {"F5"},
                EP=ep, IT=it, groupe=groupe, ia=t["ia"], L=t["L"], anc_extra=[], anc_exclus=[], anc_partiel=[],
                just="", poste_rep=t["metier"].replace("Ingenieur cybersecurite (hors SOC)", "analyste en sécurité de l'information")
                .replace("Chirurgien-dentiste", "dentiste propriétaire").replace("Medecin de famille", "médecin de famille")
                .replace("Orthophoniste", "orthophoniste"))


def base_r1(code, salarie):
    vs = [t for t in K.V1 if t["code"] == code]
    meme = [t for t in vs if (K.P.type_statut(t) in ("salarié", "fonctionnaire")) == salarie]
    return max(meme or vs, key=lambda t: (t["W"], t["id"]))


# Cellules des pays ajoutes : (code, pays) -> (statut, base, brut median, brut P80 ou None, source, fiabilite, fonction)
# Brut annuel en monnaie locale ; P80 None = rapport P80 / mediane de la base.
H = 1950
CELLULES = {
    ("2266", "US"): ("salarié", "T93", 95410, p80_interp(112510, 132850), "BLS OEWS mai 2024 (S113) : orthophonistes, médiane 95 410 USD", "officielle", "us"),
    ("2222", "US"): ("salarié", None, 128790, None, "BLS OEWS mai 2024 relayé (S194) : infirmières sages-femmes, médiane 128 790 USD", "relayée (site secondaire)", "us"),
    ("2211", "US"): ("salarié", None, 238380, None, "BLS OEWS mai 2024 relayé (S194) : médecins de famille, médiane 238 380 USD (plafond de publication 239 200 USD)", "relayée (site secondaire)", "us"),
    ("2120", "US"): ("salarié", None, 125770, None, "BLS OEWS mai 2024 relayé (S194) : actuaires, médiane 125 770 USD", "relayée (site secondaire)", "us"),
    ("2529", "US"): ("salarié", "T90", 124910, p80_interp(159600, 186420), "BLS OEWS mai 2024 (S113) : analystes en sécurité de l'information, médiane 124 910 USD", "officielle", "us"),
    ("2267", "US"): ("salarié", None, 131860, None, "BLS mai 2023 relayé (S194) : optométristes, médiane 131 860 USD (aucun chiffre de mai 2024 trouvé)", "relayée (2023, site secondaire)", "us"),
    ("2212", "US"): ("salarié", None, 404000 * 0.85, None, "Medscape 2025 relayé (S195) : spécialistes, rémunération moyenne 404 000 USD en 2024, tous statuts ; × 0,85 (moyenne vers médiane, règle 1.4)", "non officielle (moyenne)", "us"),
    ("2264", "US"): ("salarié", None, 101020, None, "BLS OEWS mai 2024 relayé (S194) : kinésithérapeutes, médiane 101 020 USD", "relayée (site secondaire)", "us"),
    ("2261", "US"): ("indépendant", "T92", 185360, p80_ln(185360, 218710 / 185360), "ADA 2023 (S114) : dentistes généralistes propriétaires, médiane 185 360 USD", "officielle (ordre professionnel)", "us_indep"),
    ("2211", "CA"): ("libéral (RAMQ)", "T32", 268808 * 0.70, math.exp(math.log(268808) + 0.6567 * math.log(505024 / 268808)) * 0.70,
                     "Guichet-Emplois 2023-2024 (S122) : médecins de famille, médiane 268 808 CAD avant frais ; moins 30 % de frais", "officielle", "ca_indep"),
    ("2264", "CA"): ("salarié", None, 48.08 * H, 48.08 * (54.91 / 48.08) ** 0.6567 * H, "Guichet-Emplois relayé (S196) : physiothérapeutes, Québec, médiane 48,08 CAD/h, haut 54,91 (année non affichée) ; × 1 950 h", "officielle (année non affichée)", "ca"),
    ("2266", "CA"): ("salarié", "T93", 42.74 * H, None, "Guichet-Emplois relayé (S196) : orthophonistes, région de Montréal, médiane 42,74 CAD/h (aucun chiffre provincial) ; × 1 950 h", "officielle (région de Montréal)", "ca"),
    ("2120", "CA"): ("salarié", None, 51.98 * H, 51.98 * (84.13 / 51.98) ** 0.6567 * H, "Guichet-Emplois relayé (S196), novembre 2025 : mathématiciens, statisticiens et actuaires, Québec, médiane 51,98 CAD/h ; × 1 950 h", "relayée, groupe plus large", "ca"),
    ("2211", "AU"): ("salarié", None, 2446 * 52, None, "Jobs and Skills Australia (S197) : généralistes et médecins résidents (ANZSCO 2531), médiane 2 446 AUD par semaine, salariés (proxy : internes compris)", "officielle, proxy", "au"),
    ("2212", "AU"): ("salarié", None, 3620 * 52, None, "Jobs and Skills Australia (S197) : médecins spécialistes (ANZSCO 2533), médiane 3 620 AUD par semaine (une autre page donne 4 657)", "officielle, sources en conflit", "au"),
    ("2266", "AU"): ("salarié", "T93", 2003 * 52, None, "Jobs and Skills Australia (S197) : audiologistes et orthophonistes (ANZSCO 2527), médiane 2 003 AUD par semaine", "officielle", "au"),
    ("2264", "AU"): ("salarié", None, 1710 * 52, None, "Jobs and Skills Australia (S197) : kinésithérapeutes (ANZSCO 2525), médiane 1 710 AUD par semaine (novembre 2024)", "officielle", "au"),
    ("2261", "AU"): ("salarié", None, 3232 * 52, None, "Jobs and Skills Australia (S197) : dentistes (groupe des praticiens dentaires), médiane 3 232 AUD par semaine, salariés", "officielle", "au"),
    ("2211", "SG"): ("salarié", None, 7165 * 12, None, "MOM, enquête sur les salaires par profession, juin 2025, relayée (S198) : médecin généraliste, médiane 7 165 SGD par mois", "relayée", "sg"),
    ("2529", "AE"): ("salarié", None, 30000 * 12, 40000 * 12, "Michael Page 2025 relayé (S199) : pentesteurs et consultants en sécurité, 20 000 à 40 000 AED par mois ; milieu", "non officielle (cabinet de recrutement)", "ae"),
    ("2211", "AE"): ("salarié", None, 14434 * 12, None, "Indeed relayé (S199) : médecin, moyenne 14 434 AED par mois", "non officielle (offres d'emploi)", "ae"),
    ("2261", "AE"): ("salarié", None, math.sqrt(12666 * 30948) * 12, math.sqrt(12666 * 30948) * (30948 / math.sqrt(12666 * 30948)) ** 0.6567 * 12,
                     "Paylab relayé (S199) : dentiste, 12 666 à 30 948 AED par mois ; milieu géométrique", "non officielle (fourchette déclarative)", "ae"),
    ("2222", "AE"): ("salarié", None, math.sqrt(7484 * 21963) * 12, math.sqrt(7484 * 21963) * (21963 / math.sqrt(7484 * 21963)) ** 0.6567 * 12,
                     "Paylab relayé (S199) : sage-femme, 7 484 à 21 963 AED par mois ; milieu géométrique", "non officielle (fourchette déclarative)", "ae"),
}
SANS_EQUIVALENT = {"2619": "notariat de type latin absent (le notary public n'est pas un juriste)"}
REFUSES = {
    ("2120", "SG"): "article sans source ni année (10 416 SGD par mois) : refusé",
    ("2261", "SG"): "site de salaires à estimations modélisées (61 956 SGD par an) : refusé",
    ("2264", "SG"): "estimation modélisée (85 524 SGD par an) : refusée",
    ("2212", "SG"): "fourchette de tous médecins, pas de spécialistes : refusée",
    ("2212", "AE"): "fourchettes non attribuées (35 000 à 80 000 AED par mois) : refusées",
    ("2264", "AE"): "sources contradictoires (247 000 AED par an ou 6 200 AED par mois) : refusées",
    ("2120", "AE"): "site de coût de la vie, revenu net : refusé",
}


def nouvelles_variantes(codes):
    V, vides = [], []
    for code in codes:
        for pays in PAYS_NOUVEAUX:
            if code in SANS_EQUIVALENT and not (code == "2619" and pays == "CA"):
                vides.append((code, pays, "sans équivalent : " + SANS_EQUIVALENT[code]))
                continue
            if (code, pays) not in CELLULES:
                vides.append((code, pays, REFUSES.get((code, pays), "revenu non trouvé")))
                continue
            statut, src6, med, p80, source, fiab, mode = CELLULES[(code, pays)]
            salarie = statut in ("salarié",)
            if src6:
                base = depuis_v6(src6)
            else:
                b = base_r1(code, salarie)
                base = {k: v for k, v in b.items() if k in ("src", "citp", "niveau", "C", "R", "Se", "EP", "IT", "groupe",
                                                            "ia", "L", "anc_extra", "anc_exclus", "anc_partiel", "just", "poste_rep")}
                base["fx"] = set(b["fx"]) - {"F5"}
            if p80 is None:
                ref = base_r1(code, salarie)
                p80 = med * ref["p80"] / ref["med"]
            fn = {"us": us_net, "us_indep": us_net_indep, "ca": ca_net, "ca_indep": ca_net_indep, "au": au_net,
                  "sg": sg_net, "ae": ae_net}[mode]
            cur = CUR[pays]
            t = copy.deepcopy(base)
            t.update(code=code, citp=code, poste=f"{code} {K.NOMS_CITP[code]}", statut=statut, pays=pays, resid=pays, cur=cur,
                     langue=0, cle_mc=code, id=f"{code}-{pays}-{statut[:3]}", med=round(med, -2), p80=round(p80, -2),
                     src_med=source, src_p80="même source" if CELLULES[(code, pays)][3] is not None else "estimé : rapport P80 / médiane de la base",
                     fiab=fiab, h="non trouvé", q=1.0, etp="source à temps plein", etp_ok=True, fiscal="brut_" + pays,
                     net_de_brut=fn, ppa=M6.PLI["FR"] / (PLI[pays] * XR24[cur]), nominal=1 / XR25[cur], exonere=False)
            V.append(t)
    return V, vides


TOP10_CODES = [t["code"] for t in K.CL2[:10]]
NOUV, VIDES = nouvelles_variantes(TOP10_CODES)
SEL3, CL3, B3 = K.calculer(K.V2 + NOUV)

if __name__ == "__main__":
    print("10 premiers codes du classement 2 :", TOP10_CODES)
    print("Variantes ajoutées :", len(NOUV), "; cellules vides :", len(VIDES))
    for t in K.calculer(NOUV + K.V2)[1][:15]:
        mc = t["mc"]
        print(f"{t['rang']:3d}{'=' if t['groupe_eg'] > 1 else ' '} {t['id']:16s} {t['poste'][:40]:40s} ({t['poste_rep'][:28]}) {t['statut'][:14]:14s} {t['pays']}/{t['resid']:5s} "
              f"{t['palier']}{'*' if t['proche'] else ' '} RE {t['RE']:.2f} {t['med_ai_ppa'] / 1000:.0f}k P10 A {mc['A']['p_top']:.2f} [{mc[min('ABCD', key=lambda v: mc[v]['p_top'])]['p_top']:.2f}-{max(mc[v]['p_top'] for v in 'ABCD'):.2f}] P1 {mc['A']['p_1']:.3f} [{t['fiab'][:26]}]")
    print("Nouveaux pays, rang de chaque variante dans l'ensemble des variantes :")
    for t in NOUV:
        print(f"  {t['id']:16s} W {t['W']:.3f} RE {t['RE']:.2f} {t['med_ai_ppa'] / 1000:.0f}k impôt {100 * t['taux_impot']:.0f}%")


# ---------------------------------------------------------------------------
# Sorties : 15 premiers de chaque classement, cellules non sourcees
# ---------------------------------------------------------------------------
NON_SOURCE = ("non re-sourcée", "estimé (structure)")


def non_sourcees(sel):
    return [t for t in sel if any(m in t["fiab"] for m in NON_SOURCE)]


def resume(cl, n=15):
    out = []
    for t in cl[:n]:
        mc = t["mc"]
        out.append(dict(rang=f"{t['rang']}{'=' if t['groupe_eg'] > 1 else ''}", id=t["id"], code=t["code"], poste=t["poste"],
                        poste_rep=t["poste_rep"], statut=t["statut"], pays=t["pays"], resid=t["resid"],
                        palier=t["palier"] + ("*" if t["proche"] else ""), p10=mc["A"]["p_top"],
                        p10_min=min(mc[v]["p_top"] for v in "ABCD"), p10_max=max(mc[v]["p_top"] for v in "ABCD"),
                        p1=mc["A"]["p_1"], net_nom=t["med_ai_nom"], net_ppa=t["med_ai_ppa"], fiab=t["fiab"], src=t["src_med"]))
    return out


def ecrire():
    import json
    import os
    res = {"classement1": resume(K.CL1), "classement_monde": resume(CL3),
           "non_sourcees_1": [(t["code"], t["id"], t["fiab"], t["src_med"]) for t in non_sourcees(K.CL1)],
           "non_sourcees_monde": [(t["code"], t["id"], t["fiab"], t["src_med"]) for t in non_sourcees(CL3)],
           "cellules_vides": VIDES, "top10_codes": TOP10_CODES,
           "p1_max": {"classement1": max(t["mc"]["A"]["p_1"] for t in K.CL1), "monde": max(t["mc"]["A"]["p_1"] for t in CL3)}}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats_v7_1.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1, default=float)
    return res


RESULTATS = ecrire()
