# -*- coding: utf-8 -*-
"""Version 7 (29 octobre 2026) : tri des pays (OCDE + Singapour + Emirats), regle declaree en 1.15.

Piliers a poids egaux : (1) revenu net apres impot, celibataire sans enfant au salaire moyen, USD PPA
(OCDE, Taxing Wages 2026, donnees 2025) ; (2) heures annuelles effectivement travaillees par travailleur
(OCDE), moins c'est mieux ; (3) part des travailleurs en tension au travail (job strain, 2021, OCDE a partir
de l'enquete europeenne EWCTS), moins c'est mieux. Min-max sur les pays disponibles ; pilier sans donnee
comparable = mediane des pays disponibles (valeur neutre), pays signale. Score = moyenne ; 10 premiers.
Provenance de chaque valeur : "lu" (lu dans une source pendant l'analyse), "imputé" (calcule ou borne a
partir de chiffres lus), "connu" (chiffre OCDE connu avant l'analyse, non reverifie), None (sans donnee).
"""
import numpy as np

NOMS = {
    "CH": "Suisse", "NL": "Pays-Bas", "LU": "Luxembourg", "GB": "Royaume-Uni", "NO": "Norvège", "IS": "Islande",
    "CA": "Canada", "AU": "Australie", "IE": "Irlande", "DK": "Danemark", "US": "États-Unis", "DE": "Allemagne",
    "AT": "Autriche", "BE": "Belgique", "SE": "Suède", "FI": "Finlande", "FR": "France", "KR": "Corée",
    "JP": "Japon", "IL": "Israël", "NZ": "Nouvelle-Zélande", "ES": "Espagne", "IT": "Italie", "PT": "Portugal",
    "GR": "Grèce", "PL": "Pologne", "CZ": "Tchéquie", "SK": "Slovaquie", "HU": "Hongrie", "SI": "Slovénie",
    "EE": "Estonie", "LV": "Lettonie", "LT": "Lituanie", "TR": "Türkiye", "MX": "Mexique", "CL": "Chili",
    "CO": "Colombie", "CR": "Costa Rica", "SG": "Singapour", "AE": "Émirats arabes unis",
}
EUROPE = {"CH", "NL", "LU", "GB", "NO", "IS", "IE", "DK", "DE", "AT", "BE", "SE", "FI", "FR", "ES", "IT", "PT",
          "GR", "PL", "CZ", "SK", "HU", "SI", "EE", "LV", "LT", "TR"}

# (1) Revenu net au salaire moyen, USD PPA 2025 : valeur, provenance, source.
NET = {
    "CH": (87303, "lu", "S167"), "NL": (67017, "lu", "S167"), "LU": (63385, "lu", "S167"),
    "GB": (63277, "lu", "S167"), "NO": (63052, "lu", "S167"), "IS": (60863, "lu", "S167"),
    "CA": (60811, "lu", "S167"), "AU": (60275, "lu", "S167"), "DK": (57205, "lu", "S167"),
    "IE": (60500, "imputé", "S167 : parmi les 9 pays au-dessus de 60 000, sous le Canada (60 811)"),
    "US": (55580, "imputé", "S167 : salaire moyen 73 520 USD et coin fiscal 30,0 % lus ; part patronale estimée"),
    "DE": (57600, "imputé", "S167 : salaire moyen 93 985 USD PPA (tableau 1.3) x (1 - 38,7 %, taux déduit du coin fiscal de 49,3 %)"),
    "KR": (55000, "imputé", "S167 : absente de la liste lue des 9 pays au-dessus de 60 000"),
    "AT": (57600, "imputé", "S167 : salaire moyen 86 370 USD PPA (tableau 1.3) x (1 - 33,3 %, taux lu, colonne incertaine)"),
    "BE": (49000, "connu", "taux moyen de 39,5 % lu (S167)"),
    "SE": (48500, "connu", ""), "FI": (46000, "connu", ""), "FR": (46000, "connu", ""), "JP": (43000, "connu", ""),
    "NZ": (44000, "connu", ""), "IL": (40000, "connu", ""), "ES": (38000, "connu", ""), "IT": (36000, "connu", ""),
    "PT": (30000, "connu", ""), "GR": (26000, "connu", ""), "PL": (32000, "connu", ""), "CZ": (32000, "connu", ""),
    "SK": (27000, "connu", ""), "HU": (26000, "connu", ""), "EE": (33000, "connu", ""),
    "SI": (34100, "imputé", "S167 : salaire moyen 53 697 USD PPA (tableau 1.3) x (1 - 36,5 %, taux déduit du coin fiscal de 45,3 %)"),
    "LV": (26000, "connu", ""), "LT": (32000, "connu", ""), "TR": (29000, "connu", ""), "MX": (15000, "connu", ""),
    "CL": (22000, "connu", ""), "CO": (13000, "connu", ""), "CR": (19000, "connu", ""),
    "SG": (57300, "imputé", "S168 : revenu médian des résidents à temps plein hors part patronale (5 000 SGD/mois), "
                            "cotisation CPF de 20 %, barème IRAS, PPA connue ; médiane, pas moyenne"),
    "AE": (83500, "imputé", "S169 : salaire moyen de 16 000 AED/mois attribué au FCSC par un site secondaire, "
                            "sans impôt sur le revenu ; PPA connue"),
}
# (2) Heures annuelles effectivement travaillees par travailleur.
HEURES = {
    "DE": (1331, "lu", "S170 (2024)"), "DK": (1379, "lu", "S170 (2024)"), "NO": (1407, "lu", "S170 (2024)"),
    "US": (1796, "lu", "S170 (2024)"), "NL": (1417, "lu", "S171 (2023)"), "IS": (1433, "lu", "S171 (2023)"),
    "AT": (1442, "lu", "S171 (2023)"), "SE": (1444, "lu", "S171 (2023)"), "FR": (1490, "lu", "S171 (2023)"),
    "BE": (1493, "lu", "S171 (2023)"), "FI": (1518, "lu", "S171 (2023)"), "CH": (1533, "lu", "S171 (2023)"),
    "JP": (1607, "lu", "S171 (2023)"), "CA": (1685, "lu", "S171 (2023)"), "AU": (1694, "lu", "S171 (2023)"),
    "NZ": (1730, "lu", "S171 (2023)"), "IE": (1775, "lu", "S171 (2023), valeur d'un site secondaire à vérifier"),
    "KR": (1910, "lu", "S171 (2023), valeur d'un site secondaire à vérifier"),
    "LU": (1450, "imputé", "S172 : moins de 1 500 h"), "GB": (1524, "connu", ""), "IL": (1880, "connu", ""),
    "ES": (1632, "connu", ""), "IT": (1734, "connu", ""), "PT": (1696, "connu", ""), "GR": (1897, "connu", ""),
    "PL": (1803, "connu", ""), "CZ": (1754, "connu", ""), "SK": (1589, "connu", ""), "HU": (1680, "connu", ""),
    "SI": (1593, "connu", ""), "EE": (1742, "connu", ""), "LV": (1547, "connu", ""), "LT": (1597, "connu", ""),
    "TR": (1732, "connu", ""), "MX": (2207, "connu", ""), "CL": (1953, "connu", ""), "CO": (2297, "connu", ""),
    "CR": (2149, "connu", ""),
    "SG": (2298, "imputé", "S168 : 44,2 h payées par semaine pour les temps plein × 52 ; définition différente"),
    "AE": (2496, "imputé", "S169 : durée légale de 48 h × 52 ; aucune mesure des heures réelles trouvée"),
}
# (3) Tension au travail 2021 (OCDE, EWCTS), pays europeens de l'OCDE couverts.
_TREIZE = "S173 : moyenne de 13 %, les trois quarts des pays entre 11 et 15 %"
STRAIN = {"NL": (9, "imputé", "S173 : moins de 10 %"), "EE": (9, "imputé", "S173 : moins de 10 %"),
          "PT": (9, "imputé", "S173 : moins de 10 %"), "SI": (9, "imputé", "S173 : moins de 10 %"),
          "CZ": (17, "lu", "S173"), "FI": (17, "lu", "S173"), "FR": (18, "lu", "S173")}
for _c in ("AT", "BE", "DK", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "PL", "SK", "ES", "SE", "CH", "NO"):
    STRAIN[_c] = (13, "imputé", _TREIZE)

PAYS = list(NOMS)


def _minmax(vals, mieux_haut):
    lo, hi = min(vals.values()), max(vals.values())
    return {c: ((v - lo) / (hi - lo) if mieux_haut else (hi - v) / (hi - lo)) for c, v in vals.items()}


def scores(net, heures, strain):
    p1 = _minmax(net, True)
    p2 = _minmax(heures, False)
    p3 = _minmax(strain, False)
    med3 = float(np.median(list(p3.values())))
    out = {}
    for c in PAYS:
        s3 = p3.get(c, med3)
        out[c] = {"p1": p1[c], "p2": p2[c], "p3": s3, "p3_nc": c not in p3, "score": (p1[c] + p2[c] + s3) / 3}
    return out


def _valeurs(d):
    return {c: v[0] for c, v in d.items()}


BASE = scores(_valeurs(NET), _valeurs(HEURES), _valeurs(STRAIN))
RANG = sorted(PAYS, key=lambda c: -BASE[c]["score"])
RETENUS = RANG[:10]


def robustesse(n=10_000, graine=20261029):
    rng = np.random.default_rng(graine)
    compte = {c: 0 for c in PAYS}

    def bruit(d):
        return {c: v * (1 + rng.uniform(-0.03, 0.03) if p == "lu" else 1 + rng.uniform(-0.10, 0.10))
                for c, (v, p, _) in d.items()}
    for _ in range(n):
        s = scores(bruit(NET), bruit(HEURES), bruit(STRAIN))
        for c in sorted(PAYS, key=lambda c: -s[c]["score"])[:10]:
            compte[c] += 1
    return {c: compte[c] / n for c in PAYS}


P_TOP10 = robustesse()

if __name__ == "__main__":
    for i, c in enumerate(RANG, 1):
        b = BASE[c]
        print(f"{i:2d} {c} {NOMS[c]:22s} score {b['score']:.3f}  net {b['p1']:.2f} h {b['p2']:.2f} strain {b['p3']:.2f}{' nc' if b['p3_nc'] else ''}  P(top10) {P_TOP10[c]:.2f}")
