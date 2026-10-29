# -*- coding: utf-8 -*-
"""Version 7 : impot sur le revenu et cotisations salariales, celibataire sans enfant, baremes 2025
simplifies (section 1.15). Chaque fonction prend le salaire brut annuel en monnaie locale et rend le net
apres cotisations salariales et impot sur le revenu. Les independants sont traites avec le meme bareme,
applique a leur revenu avant impot (approximation declaree).

Verification : au salaire moyen (AW) de l'OCDE, le taux calcule est compare au taux moyen publie ou
deduit du coin fiscal publie (CALIBRAGE) ; ecart signale dans le rapport.
"""


def _bareme(x, tranches):
    """Impot progressif : tranches = [(seuil_bas, taux), ...] triees."""
    impot = 0.0
    for i, (bas, taux) in enumerate(tranches):
        haut = tranches[i + 1][0] if i + 1 < len(tranches) else float("inf")
        if x > bas:
            impot += (min(x, haut) - bas) * taux
    return impot


# --- France (bareme 2025, revenus 2024) : sur le net deja calcule dans les cellules --------------------
def impot_fr(imposable):
    ir = _bareme(imposable, [(0, 0), (11497, 0.11), (29315, 0.30), (83823, 0.41), (180294, 0.45)])
    if ir < 1965:  # decote d'un celibataire
        ir = max(0.0, ir - (889 - 0.4525 * ir))
    cehr = 0.03 * max(0.0, min(imposable, 500000) - 250000) + 0.04 * max(0.0, imposable - 500000)
    return ir + cehr


def apres_impot_fr(net, liberal):
    """net = revenu net de cotisations, CSG et CRDS (cellules v4 a v6). Imposable : salarie = net plus
    CSG non deductible et CRDS (environ 3,5 %), moins 10 % de frais (plafond 14 171 €) ; liberal =
    benefice avant CSG non deductible (net / 0,96)."""
    if liberal:
        imposable = net / 0.96
    else:
        brut_fiscal = net * 1.035
        imposable = brut_fiscal - min(0.10 * brut_fiscal, 14171)
    return net - impot_fr(imposable)


# --- Suisse, Geneve : impot a la source, bareme A0 2026, en % du brut (S179) ----------------------------
# Points lus : 100 000 -> 16,5 % ; 200 000 -> 22,5 % ; 300 000 -> 25 %. Autres points estimes.
_GE = [(0, 0.0), (30000, 0.02), (50000, 0.075), (75000, 0.12), (100000, 0.165), (200000, 0.225),
       (300000, 0.25), (500000, 0.275), (1000000, 0.30)]


def taux_ge(brut):
    for (x0, t0), (x1, t1) in zip(_GE, _GE[1:]):
        if brut <= x1:
            return t0 + (t1 - t0) * (brut - x0) / (x1 - x0)
    return _GE[-1][1]


def apres_impot_ch(cellule, independant, lamal=449.20 * 12):
    """cellule = revenu net de cotisations sociales (et de la prime LAMal) des versions 4 a 6.
    Salarie : brut = cellule / 0,80. Independant : base = cellule + prime LAMal."""
    base = cellule + lamal if independant else cellule / 0.80
    return cellule - taux_ge(base) * base


# --- Pays du classement 2 : brut -> net apres cotisations salariales et impot --------------------------
def net_lu(brut):
    ssc = min(brut, 155000) * (0.08 + 0.028) + max(0.0, brut - 12 * 2704 / 4) * 0.014
    imposable = max(0.0, brut - ssc - 540 - 396)
    t = [(0, 0), (13230, 0.08), (15435, 0.09), (17640, 0.10), (19845, 0.11), (22050, 0.12), (24255, 0.14),
         (26550, 0.16), (28845, 0.18), (31140, 0.20), (33435, 0.22), (35730, 0.24), (38025, 0.26),
         (40320, 0.28), (42615, 0.30), (44910, 0.32), (47205, 0.34), (49500, 0.36), (51795, 0.38),
         (54090, 0.39), (117450, 0.40), (176160, 0.41), (234870, 0.42)]
    ir = _bareme(imposable, t)
    ir *= 1.07 if imposable <= 150000 else 1.09  # contribution au fonds pour l'emploi
    return brut - ssc - ir


def net_nl(brut):
    impot = _bareme(brut, [(0, 0.3582), (38441, 0.3748), (76817, 0.4950)])
    ahk = max(0.0, 3068 - 0.06337 * max(0.0, brut - 28406))
    if brut <= 12169:
        ak = 0.08053 * brut
    elif brut <= 26288:
        ak = 980 + 0.30030 * (brut - 12169)
    elif brut <= 43071:
        ak = 5220 + 0.02258 * (brut - 26288)
    else:
        ak = max(0.0, 5599 - 0.0651 * (brut - 43071))
    return brut - max(0.0, impot - ahk - ak)


def net_no(brut):
    trygd = 0.077 * brut if brut > 99650 else 0.0
    alminnelig = max(0.0, brut - min(0.46 * brut, 92000) - 108550)
    trinn = _bareme(brut, [(0, 0), (217400, 0.017), (306050, 0.040), (697150, 0.137), (942400, 0.167),
                           (1410750, 0.177)])
    return brut - trygd - 0.22 * alminnelig - trinn


def _est_de(zve):
    if zve <= 12096:
        return 0.0
    if zve <= 17443:
        y = (zve - 12096) / 10000
        return (932.30 * y + 1400) * y
    if zve <= 68480:
        z = (zve - 17443) / 10000
        return (176.64 * z + 2397) * z + 1015.13
    if zve <= 277825:
        return 0.42 * zve - 10911.92
    return 0.45 * zve - 19246.67


def net_de(brut):
    rv_av = min(brut, 96600) * (0.093 + 0.013)
    kv_pv = min(brut, 66150) * (0.0855 + 0.024)
    zve = max(0.0, brut - 1230 - 36 - min(brut, 96600) * 0.093 - min(brut, 66150) * (0.073 + 0.024) * 0.96)
    est = _est_de(zve)
    soli = min(0.055 * est, 0.119 * max(0.0, est - 19950)) if est > 19950 else 0.0
    return brut - rv_av - kv_pv - est - soli


def net_at(brut):
    ssc = min(brut, 90300) * 0.1807
    courant, special = brut * 12 / 14, brut * 2 / 14
    imposable = max(0.0, (courant - ssc * 12 / 14) - 132)
    ir = _bareme(imposable, [(0, 0), (13308, 0.20), (21617, 0.30), (35836, 0.40), (69166, 0.48),
                             (103072, 0.50), (1000000, 0.55)])
    ir_special = max(0.0, special - ssc * 2 / 14 - 620) * 0.06
    return brut - ssc - ir - ir_special


def net_dk(brut):
    am = 0.08 * brut
    apres_am = brut - am
    fradrag = min(0.1275 * apres_am, 63300)
    personfradrag = 51600
    commune = 0.250 * max(0.0, apres_am - fradrag - personfradrag)
    bund = 0.1201 * max(0.0, apres_am - personfradrag)
    top = 0.15 * max(0.0, apres_am - 611800)
    return brut - am - commune - bund - top


def net_is(brut):
    pension = 0.04 * brut
    mensuel = (brut - pension) / 12
    impot = _bareme(mensuel, [(0, 0.3149), (472005, 0.3799), (1325127, 0.4629)]) - 68691
    return brut - pension - 12 * max(0.0, impot)


def net_gb(brut):
    pa = max(0.0, 12570 - max(0.0, brut - 100000) / 2)
    ir = 0.20 * max(0.0, min(brut, 50270) - pa) + 0.40 * max(0.0, min(brut, 125140) - max(50270, pa)) \
        + 0.45 * max(0.0, brut - 125140)
    ni = 0.08 * max(0.0, min(brut, 50270) - 12570) + 0.02 * max(0.0, brut - 50270)
    return brut - ir - ni


def net_de_indep(benefice):
    """Medecin ou dentiste liberal allemand : Versorgungswerk 18,6 % jusqu'a 96 600 EUR, assurance maladie
    privee 9 000 EUR (estime), deductibles ; impot sur le reste."""
    social = 0.186 * min(benefice, 96600) + 9000
    zve = max(0.0, benefice - social - 36)
    est = _est_de(zve)
    soli = min(0.055 * est, 0.119 * max(0.0, est - 19950)) if est > 19950 else 0.0
    return benefice - social - est - soli


def impot_ue(brut, taux):
    """Fonctionnaires et agents de l'UE : impot communautaire et prelevement de solidarite, taux moyen estime."""
    return brut * (1 - taux)


def net_si(brut):
    ssc = 0.221 * brut
    imposable = max(0.0, brut - ssc - 5260)
    ir = _bareme(imposable, [(0, 0.16), (9210, 0.26), (27089, 0.33), (54178, 0.39), (78016, 0.50)])
    return brut - ssc - ir


NET_PAYS = {"LU": net_lu, "NL": net_nl, "NO": net_no, "DE": net_de, "AT": net_at, "DK": net_dk, "IS": net_is,
            "GB": net_gb, "SI": net_si}

# Salaire moyen 2025 (OCDE, monnaie locale) et taux moyen (impot + cotisations salariales, % du brut).
# Taux "lu" = publie ; "deduit" = tire du coin fiscal publie avec une part patronale estimee.
CALIBRAGE = {
    "LU": (77844, 0.320, "taux lu"),
    "NL": (69028, 0.279, "taux lu ; salaire moyen relayé"),
    "NO": (801695, 0.281, "taux lu ; salaire moyen relayé"),
    "DE": (66700, 0.387, "déduit du coin fiscal de 49,3 %"),
    "AT": (63054, 0.333, "lu, colonne incertaine"),
    "DK": (537071, 0.355, "déduit du coin fiscal de 35,8 %"),
    "IS": (12433527, 0.312, "déduit du coin fiscal de 31,5 % (27,2 %), plus 4 % de pension obligatoire"),
    "GB": (55983, 0.231, "déduit du coin fiscal de 32,4 %"),
    "SI": (31000, 0.365, "déduit du coin fiscal de 45,3 % ; salaire moyen imputé"),
}


def verification():
    out = {}
    for c, (aw, cible, prov) in CALIBRAGE.items():
        taux = 1 - NET_PAYS[c](aw) / aw
        out[c] = (aw, taux, cible, prov)
    return out


if __name__ == "__main__":
    for c, (aw, taux, cible, prov) in verification().items():
        print(f"{c} AW {aw:>12,.0f} calculé {100 * taux:5.1f} %  cible {100 * cible:5.1f} %  écart {100 * (taux - cible):+5.1f}  ({prov})")
    for x in (60000, 100000, 200000):
        print("GE", x, round(100 * taux_ge(x), 1))
    print("FR libéral 100 000 ->", round(apres_impot_fr(100000, True)), " salarié 40 000 ->", round(apres_impot_fr(40000, False)))
