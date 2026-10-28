# -*- coding: utf-8 -*-
"""Version 5 (28 octobre 2026) : grille de qualite de l'emploi d'Eurofound, 7 dimensions a poids egaux.

Dimensions (Eurofound, EWCS 2015 a 2024) : environnement physique (EP), intensite du travail (IT),
qualite du temps de travail (QT), environnement social (ES), competences et autonomie (CA),
perspectives et securite (PS), revenu (RE). Toutes notees de 1 (mauvais) a 5 (bon).

Conversion des notes v4, declaree avant calcul (section 1.12 du rapport) :
- L'ancienne note de charge valait 5 moins le nombre de facteurs F1 a F5. Chaque triplet recoit ici
  ses facteurs explicites (FACTEURS) ; 5 - leur nombre redonne la note v4 (verifie par controle()).
- EP : grille d'exposition physique par groupe de metiers, qui reprend et gradue le facteur F4.
- IT : grille d'intensite par groupe de metiers, qui reprend et gradue le facteur F2.
- QT : 5 - F1 (plus de 45 h) - F3 (nuits, week-ends, astreintes) - H (horaires imposes : controle v4
  de 3 ou moins), plancher 1. Composantes Eurofound : duree, horaires atypiques, amenagements.
- ES = relations v4 ; PS = securite v4 (perspectives de carriere non notees a part).
- CA = moyenne du controle v4 (latitude de decision) et du niveau de competence CITP-08 de l'OIT
  (niveau 4 -> 5 ; 3 -> 3,67 ; 2 -> 2,33 ; 1 -> 1).
- RE = note de revenu (median et P80 en equivalent temps plein, ajustes en PPA).
- Hors grille Eurofound, donc hors score : sens, lieu (teletravail), facteur F5 (trajet).
"""

DIMS = ("EP", "IT", "QT", "ES", "CA", "PS", "RE")
NOMS_DIMS = {
    "EP": "environnement physique", "IT": "intensité du travail", "QT": "qualité du temps de travail",
    "ES": "environnement social", "CA": "compétences et autonomie", "PS": "perspectives et sécurité",
    "RE": "revenu",
}

# Facteurs de l'ancienne note de charge (rubrique 1.3) : F1 plus de 45 h ; F2 forte intensite ou
# exigence emotionnelle ou decisionnelle ; F3 nuits, week-ends ou astreintes ; F4 penibilite physique ;
# F5 trajet d'au moins 1 h par sens ou decouches.
FACTEURS = {
    "T01": "F1 F2", "T02": "F2", "T03": "F1 F2", "T04": "F1 F2 F3", "T05": "F2 F4", "T06": "F2 F3 F4",
    "T07": "F1 F2 F3", "T08": "F2 F3", "T09": "F2", "T10": "F1 F4", "T11": "F4", "T12": "F2 F3 F4",
    "T13": "F1 F2 F3", "T14": "F2 F3", "T15": "", "T16": "F2", "T17": "F3", "T18": "F3",
    "T19": "F1 F3 F4", "T20": "F2", "T21": "F2 F3 F4", "T22": "F4", "T23": "F2 F3 F4",
    "T24": "F2 F3 F4 F5", "T25": "F2 F3 F4 F5", "T26": "F2 F3 F4", "T27": "F2 F3 F4", "T28": "F2 F3 F4",
    "T29": "F1 F2 F3", "T30": "F1 F2", "T31": "F1 F2 F3", "T32": "F1 F2 F3", "T33": "F2 F3 F4 F5",
    "T34": "F4 F5", "T35": "F2", "T36": "F2", "T37": "F2 F5", "T38": "F2", "T39": "F2 F5", "T40": "F2",
    "T41": "F2", "T42": "F2 F5", "T43": "F2", "T44": "F3 F4", "T45": "F3", "T46": "F2", "T47": "F4",
    "T48": "F1 F2 F4", "T49": "F4 F5", "T50": "F4", "T51": "F1 F2 F4", "T52": "F3 F4", "T53": "F3 F5",
    "T54": "F2 F3", "T55": "F1 F3 F4 F5", "T56": "F2", "T57": "F2", "T58": "F2 F3 F4", "T59": "F2 F3 F4",
    "T60": "F2", "T61": "F2", "T62": "", "T63": "F2 F3", "T64": "F2", "T65": "F5", "T66": "F3 F4 F5",
    "T67": "F1 F2", "T68": "F1 F2", "T69": "", "T70": "F5", "T71": "F1 F2", "T72": "F2 F5", "T73": "F2 F3",
    "T74": "F2 F3 F5", "T75": "F3 F4", "T76": "F4", "T77": "", "T78": "", "T79": "F3", "T80": "F2 F3",
    "T81": "F2", "T82": "F2 F3 F5", "T83": "F2", "T84": "F2 F3", "T85": "F2", "T86": "F2 F3", "T87": "F2 F3",
    "T88": "F2 F3", "T89": "F2", "T90": "F2", "T91": "F2 F4", "T92": "F2 F4", "T93": "",
}

# Groupes de metiers et grilles EP / IT (estimations normatives, sauf ancrage DARES signale dans ANCRAGES).
# EP : 5 bureau ou cabinet sans contrainte notable ; 4 contraintes legeres (station debout, deplacements,
# bruit modere) ; 3 postures contraignantes ou risques biologiques, chimiques ou rayonnements reguliers ;
# 2 port de charges ou manutention de personnes, postures penibles, risques physiques ; 1 cumul fort
# (chaleur, fumees, efforts violents, manutention lourde quotidienne).
# IT : 5 rythme libre, pas d'exigence emotionnelle ; 4 pression moderee ; 3 forte exigence
# (delais, objectifs, patients ou public) ; 2 urgence, vigilance de securite ou tension forte et frequente ;
# 1 cumul extreme.
GROUPES = {
    "medecin_cabinet": (4, 3, ["T01", "T02", "T03", "T30", "T32"]),
    "medecin_hopital": (3, 2, ["T04", "T29", "T31"]),
    "dentiste": (3, 3, ["T05", "T91", "T92"]),
    "pharmacien": (4, 3, ["T06", "T07"]),
    "sage_femme_hopital": (3, 2, ["T08"]),
    "sage_femme_cabinet": (4, 3, ["T09"]),
    "kine": (2, 4, ["T10", "T11", "T34"]),
    "infirmier_hopital": (2, 2, ["T12", "T23", "T24", "T25", "T26", "T27", "T28"]),
    "iade": (3, 2, ["T14"]),
    "infirmier_domicile": (2, 3, ["T13"]),
    "orthophoniste": (5, 4, ["T15", "T93"]),
    "orthoptiste": (5, 4, ["T16"]),
    "manipulateur_radio": (3, 3, ["T17"]),
    "audio_optique": (4, 4, ["T18", "T79"]),
    "veterinaire": (2, 3, ["T19"]),
    "psychologue": (5, 3, ["T20"]),
    "aide_soignant": (1, 2, ["T21", "T33"]),
    "osteo_podologue": (3, 4, ["T22", "T76"]),
    "ergotherapeute": (4, 4, ["T77"]),
    "dieteticien": (5, 4, ["T78"]),
    "informatique": (5, 3, ["T35", "T36", "T37", "T38", "T39", "T40", "T80", "T81", "T82", "T83", "T85",
                            "T86", "T87", "T88", "T89", "T90"]),
    "soc": (5, 2, ["T84"]),
    "ingenieur_industrie": (4, 3, ["T41", "T42", "T43"]),
    "technicien_maintenance": (2, 3, ["T44"]),
    "technicien_reseaux": (4, 4, ["T45"]),
    "bureau_cadre": (5, 3, ["T46", "T60", "T61", "T64", "T67", "T68", "T71"]),
    "bureau_non_cadre": (5, 4, ["T62", "T65", "T69", "T70"]),
    "batiment_electricite": (2, 4, ["T47", "T49", "T50", "T52"]),
    "artisan_batiment": (2, 3, ["T48", "T51"]),
    "conducteur_train": (4, 3, ["T53", "T54"]),
    "conducteur_routier": (2, 3, ["T55"]),
    "enseignant": (4, 3, ["T56", "T57"]),
    "police": (2, 2, ["T58"]),
    "pompier": (1, 2, ["T59"]),
    "controleur_aerien": (5, 2, ["T63"]),
    "militaire": (2, 3, ["T66"]),
    "commercial_immobilier": (4, 3, ["T72", "T73"]),
    "pilote": (4, 3, ["T74"]),
    "employe_commerce": (3, 3, ["T75"]),
}

# Niveau de competence CITP-08 (OIT) par code de profession (source publiee : classification CITP-08).
CITP = {
    "T01": ("2211", 4), "T02": ("2211", 4), "T03": ("2212", 4), "T04": ("2212", 4), "T05": ("2261", 4),
    "T06": ("2262", 4), "T07": ("2262", 4), "T08": ("2222", 4), "T09": ("2222", 4), "T10": ("2264", 4),
    "T11": ("2264", 4), "T12": ("2221", 4), "T13": ("2221", 4), "T14": ("2221", 4), "T15": ("2266", 4),
    "T16": ("2267", 4), "T17": ("3211", 3), "T18": ("2266", 4), "T19": ("2250", 4), "T20": ("2634", 4),
    "T21": ("5321", 2), "T22": ("2230", 4), "T23": ("2221", 4), "T24": ("2221", 4), "T25": ("2221", 4),
    "T26": ("2221", 4), "T27": ("2221", 4), "T28": ("2221", 4), "T29": ("2212", 4), "T30": ("2211", 4),
    "T31": ("2212", 4), "T32": ("2211", 4), "T33": ("5321", 2), "T34": ("2264", 4), "T35": ("2512", 4),
    "T36": ("2512", 4), "T37": ("2512", 4), "T38": ("2512", 4), "T39": ("2512", 4), "T40": ("2512", 4),
    "T41": ("2141", 4), "T42": ("2141", 4), "T43": ("2141", 4), "T44": ("3115", 3), "T45": ("3513", 3),
    "T46": ("2120", 4), "T47": ("7411", 2), "T48": ("7411", 2), "T49": ("7411", 2), "T50": ("7411", 2),
    "T51": ("7126", 2), "T52": ("7127", 2), "T53": ("8311", 2), "T54": ("8311", 2), "T55": ("8332", 2),
    "T56": ("2341", 4), "T57": ("2330", 4), "T58": ("5412", 2), "T59": ("5411", 2), "T60": ("2422", 4),
    "T61": ("2411", 4), "T62": ("3352", 3), "T63": ("3154", 3), "T64": ("2422", 4), "T65": ("3343", 3),
    "T66": ("0210", 2), "T67": ("2611", 4), "T68": ("2411", 4), "T69": ("3313", 3), "T70": ("3313", 3),
    "T71": ("2612", 4), "T72": ("3322", 3), "T73": ("3334", 3), "T74": ("3153", 3), "T75": ("5223", 2),
    "T76": ("2269", 4), "T77": ("2269", 4), "T78": ("2265", 4), "T79": ("3254", 3), "T80": ("2522", 4),
    "T81": ("2522", 4), "T82": ("2522", 4), "T83": ("2529", 4), "T84": ("2529", 4), "T85": ("2521", 4),
    "T86": ("2522", 4), "T87": ("2522", 4), "T88": ("2522", 4), "T89": ("2529", 4), "T90": ("2529", 4),
    "T91": ("2261", 4), "T92": ("2261", 4), "T93": ("2266", 4),
}
K_NIVEAU = {4: 5.0, 3: 1 + 4 * 2 / 3, 2: 1 + 4 * 1 / 3, 1: 1.0}

# Ancrages sources par note (remplis a partir des recherches ; vide = estimation normative).
ANCRAGES = {}


def groupe_de(tid):
    for nom, (ep, it, ids) in GROUPES.items():
        if tid in ids:
            return nom, ep, it
    raise KeyError(tid)


def dimensions(t):
    f = set(FACTEURS[t["id"]].split())
    _, ep, it = groupe_de(t["id"])
    h = 1 if t["C"] <= 3 else 0
    qt = max(1, 5 - ("F1" in f) - ("F3" in f) - h)
    ca = (t["C"] + K_NIVEAU[CITP[t["id"]][1]]) / 2
    return {"EP": ep, "IT": it, "QT": qt, "ES": t["R"], "CA": ca, "PS": t["Se"]}


def controle(T):
    """Verifie que 5 - nombre de facteurs redonne la note de charge v4 (plancher 1)."""
    ecarts = []
    for t in T:
        n = len(FACTEURS[t["id"]].split())
        if max(1, 5 - n) != t["Ch"]:
            ecarts.append((t["id"], t["Ch"], max(1, 5 - n)))
    return ecarts


# Provenance des notes hors revenu. Une note est « sourcée » si un chiffre publié (DARES, Eurofound,
# OFS, BLS...) l'ancre pour ce groupe de métiers ou ce triplet ; « mixte » si une partie de ses
# composantes est sourcée ; « estimée » sinon. Les ancrages sont remplis a partir des recherches.
ANCRAGES_GROUPE = {}
ANCRAGES_TRIPLET = {}


def provenance(t):
    g = groupe_de(t["id"])[0]
    anc = dict(ANCRAGES_GROUPE.get(g, {}))
    anc.update(ANCRAGES_TRIPLET.get(t["id"], {}))
    out = {}
    for d in ("EP", "IT", "ES", "PS"):
        out[d] = ("sourcée", anc[d]) if d in anc else ("estimée", "")
    qt = [anc["QT"]] if "QT" in anc else []
    if t.get("h_src"):
        qt.append(f"heures {t['h_src']}")
    out["QT"] = ("mixte", " ; ".join(qt)) if qt else ("estimée", "")
    out["CA"] = ("mixte", f"CITP-08 {CITP[t['id']][0]}, niveau {CITP[t['id']][1]} (S115) ; latitude estimée")
    return out
