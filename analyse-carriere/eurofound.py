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
    "T07": "F1 F2 F3", "T08": "F2 F3", "T09": "F2", "T10": "F4", "T11": "F4", "T12": "F2 F3 F4",
    "T13": "F1 F2 F3", "T14": "F2 F3", "T15": "", "T16": "F2", "T17": "F3", "T18": "F3",
    "T19": "F1 F3 F4", "T20": "F2", "T21": "F2 F3 F4", "T22": "F4", "T23": "F2 F3 F4",
    "T24": "F2 F3 F4 F5", "T25": "F2 F3 F4 F5", "T26": "F2 F3 F4", "T27": "F2 F3 F4", "T28": "F2 F3 F4",
    "T29": "F1 F2 F3", "T30": "F2", "T31": "F1 F2 F3", "T32": "F1 F2 F3", "T33": "F2 F3 F4 F5",
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


# Facteurs corriges par une donnee nouvelle (la note de charge v4 ne les reproduit donc plus).
CORRECTIONS = {"T30": "F1 retiré : médecins de famille suisses à 43 h par semaine (S131)",
               "T10": "F1 retiré : kinésithérapeutes libéraux à 43,07 h par semaine (S132)"}


def controle(T):
    """Verifie que 5 - nombre de facteurs redonne la note de charge v4 (plancher 1), hors corrections."""
    ecarts = []
    for t in T:
        if t["id"] in CORRECTIONS:
            continue
        n = len(FACTEURS[t["id"]].split())
        if max(1, 5 - n) != t["Ch"]:
            ecarts.append((t["id"], t["Ch"], max(1, 5 - n)))
    return ecarts


# ---------------------------------------------------------------------------
# Ancrages des notes hors revenu (section 1.13 du rapport, declaree avant recalcul)
# ---------------------------------------------------------------------------
# Statut d'une note :
# - S (sourcee) : chiffre d'une source officielle, quantitatif (rapport a la moyenne ou bande declaree),
#   pour le metier lui-meme (ou le metier dans son type d'etablissement), dans le pays du triplet ;
# - M (mixte) : chiffre pour un groupe plus large (categorie socioprofessionnelle, grand groupe CITP,
#   secteur), un autre pays, un autre statut, sans ampleur publiee, ou issu d'une enquete non officielle ;
#   QT et CA sont au mieux M (horaires imposes et latitude de decision restent estimes) ;
# - E (estimee) : aucun chiffre trouve, note de la grille normative.
# Contradiction : un ancrage S remplace la note par la valeur compatible la plus proche ; un ancrage M
# signale une tension sans changer la note. Les notes sont comparees aux valeurs compatibles declarees.
PAYS = {"France": "FR", "Suisse": "CH", "Luxembourg": "LU", "Allemagne": "DE", "Canada": "CA",
        "Irlande": "IE", "Etats-Unis": "US"}
LANGUE = {"T27", "T31", "T38", "T87", "T88", "T90", "T92", "T93"}  # relations - 1 pour la langue (1.10)
PIRE, MOYEN, MIEUX = {1, 2}, {3}, {4, 5}
PAS_MIEUX = {1, 2, 3}


def pays_de(t):
    return next(v for k, v in PAYS.items() if t["pays"].startswith(k))


ANCRAGES = []


def anc(code, dim, ids, texte, src, metier, pays, ok=None, f1=None, f3=None, officiel=True, quant=True,
        partiel=""):
    """Declare un ancrage. ok : notes compatibles (ensemble, ou dictionnaire par triplet) ; f1, f3 :
    presence (True) ou absence (False) du facteur exigee par le chiffre ; partiel : triplets que le
    chiffre ne couvre qu'en partie (autre statut ou metier voisin), donc au mieux M."""
    ANCRAGES.append(dict(code=code, dim=dim, ids=ids.split(), texte=texte, src=src, metier=metier,
                         pays=pays, ok=ok, f1=f1, f3=f3, officiel=officiel, quant=quant,
                         partiel=set(partiel.split())))


CADRES_SAL = ("T35 T37 T38 T39 T40 T41 T42 T43 T46 T60 T61 T63 T64 T71 T80 T82 T83 T84 T85 T86 T87 T88 "
              "T89 T90")
INF_HOP = "T08 T12 T14 T23 T24 T25 T26 T27 T28"
# Environnement physique : bandes de la part declarant au moins 3 contraintes physiques (DARES, 2019).
anc("E1", "EP", CADRES_SAL, "cadres salariés, France : 7 % déclarent au moins 3 contraintes physiques "
    "(ensemble 35 %), bande 5", "S58", False, "FR", ok=MIEUX)
anc("E2", "EP", "T47 T48 T49 T50 T51 T52 T55", "ouvriers qualifiés, France : 61 % (bande 2) ; bruit 67,5 % ; "
    "produits cancérogènes 34,8 % (ensemble 11 %, rapport 3,2)", "S58, S144", False, "FR", ok=PIRE)
anc("E3", "EP", "T49", "construction, Suisse : plus de 80 % des actifs exposés à au moins 3 risques physiques "
    "sur 10 (ensemble 45 %, rapport supérieur à 1,8)", "S149", False, "CH", ok=PIRE)
anc("E4", "EP", "T47 T48 T49 T50 T51 T52", "Eurofound, artisanat et bâtiment (CITP 7) : indice "
    "d'environnement physique 70, moyenne de l'UE 84", "S146", False, "UE", ok=PIRE)
anc("E5", "EP", "T53 T54 T55", "Eurofound, conducteurs de machines et de véhicules (CITP 8) : indice 75, "
    "moyenne de l'UE 84", "S146", False, "UE", ok=PIRE)
anc("E6", "EP", "T21 T33 " + INF_HOP, "hôpital, France : contraintes physiques au 1er rang chez les "
    "aides-soignants, au 3e chez les infirmiers et sages-femmes ; secteur : station debout prolongée 66 % "
    "(ensemble 48 %), charges lourdes 61 % (41 %) ; fonction publique hospitalière : 54 % avec au moins "
    "3 contraintes (bande 2)", "S138, S58", True, "FR", ok=PIRE, quant=False)
anc("E7", "EP", "T56 T57", "enseignants, France : plus exposés que les autres cadres pour la posture "
    "(sans ampleur publiée)", "S145", True, "FR", ok={1, 2, 3, 4}, quant=False)
anc("E8", "EP", "T05 T91 T92", "orthodontistes, France (enquête 2020, 506 volontaires) : 84 % de troubles "
    "musculosquelettiques sur 12 mois (18-64 ans : 51 à 58 %, rapport 1,4 à 1,6)", "S153", False, "FR",
    ok={2, 3}, officiel=False)
# Intensite du travail.
anc("I1", "IT", INF_HOP, "infirmiers et sages-femmes à l'hôpital, France : 72 % doivent toujours ou souvent "
    "se dépêcher (secteur hospitalier 62 %) ; exigences émotionnelles 54 %", "S138", True, "FR",
    ok=PAS_MIEUX, quant=False)
anc("I2", "IT", "T04 T29 T31", "médecins hospitaliers, France : exigences émotionnelles 74 %", "S138", True,
    "FR", ok=PAS_MIEUX, quant=False)
anc("I3", "IT", "T56 T57", "enseignants, France : plus exposés que les autres cadres à l'intensité et aux "
    "exigences émotionnelles, sans ampleur publiée ; les cadres ont eux-mêmes une forte demande "
    "psychologique (S70)", "S145, S70", True, "FR", ok=PAS_MIEUX, quant=False)
# Qualite du temps de travail : F1 si plus de 45 h en moyenne ou au moins 40 % a 48 h ou plus ; F3 si au
# moins 40 % travaillent la nuit ou le dimanche au moins une fois par mois (moyennes : nuit 10 %, dimanche 23 %).
anc("Q1", "QT", "T01", "généralistes libéraux, France : 46 h par semaine en 2025, donc F1 (seuil 45 h, "
    "à 1 h près)", "S07", True, "FR", f1=True)
anc("Q2", "QT", "T01 T02 T03", "médecins hors hôpital, France : moins de 20 % travaillent de nuit, donc pas "
    "de F3", "S138", True, "FR", f3=False)
anc("Q3", "QT", "T04 T29 T31", "médecins hospitaliers, France : nuit 62 %, dimanche 72 %, donc F3", "S138",
    True, "FR", f3=True)
anc("Q4", "QT", INF_HOP, "infirmiers et sages-femmes à l'hôpital, France : nuit 47 %, dimanche 75 %, donc F3",
    "S138", True, "FR", f3=True)
anc("Q5", "QT", "T21 T33", "aides-soignants à l'hôpital, France : nuit 39 %, dimanche 87 %, donc F3", "S138",
    True, "FR", f3=True)
anc("Q6", "QT", "T58 T59 T66", "policiers, militaires et pompiers, France : samedi 69 %, dimanche 61 %, "
    "nuit 54 %, donc F3", "S141", True, "FR", f3=True)
anc("Q7", "QT", "T55", "conducteurs routiers de fret, France : 4 sur 10 font au moins 48 h de service par "
    "semaine, donc F1 ; transport et entreposage : 56 % en horaires atypiques", "S143, S140", True, "FR",
    f1=True, f3=True)
anc("Q8", "QT", "T75", "employés peu qualifiés, France : samedi 49 %, dimanche 32 %, sous le seuil de 40 %, "
    "donc F3 non établi ; commerce : 59 % en horaires atypiques", "S140", False, "FR", f3=False)
anc("Q9", "QT", "T10", "kinésithérapeutes libéraux, France : 43,07 h par semaine, donc pas de F1", "S132",
    True, "FR", f1=False)
anc("Q10", "QT", "T30", "médecins de famille, Suisse : 43 h par semaine (étude Workforce 2020), donc pas "
    "de F1", "S131", True, "CH", f1=False)
anc("Q11", "QT", "T29", "médecins assistants et chefs de clinique, Suisse : 56 à 58 h par semaine (enquête "
    "syndicale ASMAC), donc F1", "S130", True, "CH", f1=True, officiel=False)
anc("Q12", "QT", "T91", "dentistes, Suisse : environ 42 h par semaine, donc pas de F1", "S111", True, "CH",
    f1=False)
anc("Q13", "QT", "T92", "dentistes, États-Unis : 36,1 h par semaine, donc pas de F1", "S114", True, "US",
    f1=False)
anc("Q14", "QT", "T56 T57", "enseignants, France : 42 à 43 h par semaine déclarées, donc pas de F1", "S101",
    True, "FR", f1=False)
# Environnement social : rapport r a la moyenne des actifs ; r >= 1,5 : 1 ou 2 ; r <= 2/3 : 4 ou 5 ; sinon 3.
anc("S1", "ES", "T58", "policiers et gendarmes, France : 31,2 % victimes d'agressions verbales (ensemble "
    "14,3 %, rapport 2,2) ; agressions physiques près de 7 fois plus fréquentes", "S142", True, "FR", ok=PIRE)
anc("S2", "ES", "T08 T09 T10 T11 T12 T13 T14 T15 T16 T17 T18 T23 T24 T25 T26 T27 T28 T34 T76 T77 T78 T79 T93",
    "professions intermédiaires de la santé et du travail social, France : 20,9 % victimes d'agressions "
    "verbales (ensemble 14,3 %, rapport 1,46)", "S142", False, "FR", ok=MOYEN)
anc("S3", "ES", "T56 T57", "France, menaces ou insultes : professeurs des écoles 10,1 % (rapport 1,44), "
    "enseignants du second degré 12,5 % (rapport 1,79), ensemble des actifs 7,0 % ; second degré : tensions "
    "avec le public deux fois plus fréquentes que chez les autres cadres", "S145", True, "FR",
    ok={"T56": MOYEN, "T57": PIRE})
anc("S4", "ES", "T53 T54 T55 T74", "transports, UE : part la plus élevée de soutien rare ou absent de la "
    "hiérarchie et des collègues", "S147", False, "UE", ok=PAS_MIEUX, quant=False)
# Perspectives et securite : rapport a la moyenne, ou grille 1.3 appliquee au chiffre publie
# (metier en tension ou forte creation d'emplois = forte demande = 4 pour un salarie sans statut).
anc("P1", "PS", "T04 T08 T11 T12 T14 T17 T21 T56 T57 T58 T59 T60 T61 T62 T63 T71 T77", "agents publics sans "
    "limite de durée, France : 12 % craignent pour leur emploi dans l'année (ensemble des salariés : un sur "
    "cinq, rapport 0,6)", "S139", False, "FR", ok=MIEUX)
anc("P2", "PS", "T02 T06 T35 T41 T46 T80 T83 T84 T85", "cadres, France : 13 % craignent pour leur emploi "
    "(rapport 0,65, à la limite du seuil de 2/3)", "S139", False, "FR", ok=MIEUX)
anc("P3", "PS", "T35 T80 T83 T85 T36 T81", "ingénieurs de l'informatique, France : 115 000 créations nettes "
    "d'emplois de 2019 à 2030, soit +26 % (ensemble des métiers : environ 1 million, près de 4 %) ; pénurie "
    "citée en cybersécurité et en développement ; grille 1.3 : forte demande = 4 pour un salarié, 3 pour "
    "un indépendant", "S117", True, "FR",
    ok={"T35": {4}, "T80": {4}, "T83": {4}, "T85": {4}, "T36": {3}, "T81": {3}}, partiel="T36 T81")
anc("P4", "PS", "T83 T84 T45 T89", "cybersécurité, France : offres +49 % de 2019 à 2024 (observatoire de "
    "l'ANSSI), 25 000 postes à pourvoir d'ici 2028 (OPIIEC) ; forte demande = 4", "S78", True, "FR",
    ok={4}, partiel="T45")
anc("P5", "PS", "T90", "analystes en sécurité de l'information, États-Unis : emploi projeté +29 % de 2024 à "
    "2034 (tous métiers +3,1 %) ; forte demande = 4", "S87", True, "US", ok={4})
anc("P6", "PS", "T01 T02 T03 T04", "médecins, France : tension de recrutement « particulièrement élevée » "
    "en 2024 (indicateur de la DARES, déclinaison régionale) ; profession réglementée en pénurie = 5",
    "S152", True, "FR", ok={5}, quant=False)
anc("P7", "PS", "T15", "orthophonistes libéraux, France : 90 % ne peuvent pas proposer de nouveau bilan "
    "(enquête de la FNO citée dans une question parlementaire) ; pénurie = 5", "S154", True, "FR", ok={5},
    officiel=False)


def _statut(a, t):
    s = (a["metier"] and a["quant"] and a["officiel"] and a["pays"] == pays_de(t)
         and a["dim"] not in ("QT", "CA") and t["id"] not in a["partiel"])
    return "S" if s else "M"


def _compatibles(a, tid):
    return a["ok"][tid] if isinstance(a["ok"], dict) else a["ok"]


def _accord(a, t, d):
    """Vrai si la note (ou les facteurs, pour QT) est compatible avec le chiffre."""
    if a["dim"] == "QT":
        f = set(FACTEURS[t["id"]].split())
        return all(exige is None or (fx in f) == exige for fx, exige in (("F1", a["f1"]), ("F3", a["f3"])))
    n = d[a["dim"]] + (1 if a["dim"] == "ES" and t["id"] in LANGUE else 0)
    return n in _compatibles(a, t["id"])


def variante_tensions(t, d):
    """Sensibilite (informatif) : notes en tension avec un ancrage M ramenees a la valeur compatible la
    plus proche ; pour QT, facteur F1 ou F3 mis comme le chiffre l'indique."""
    d = dict(d)
    f = set(FACTEURS[t["id"]].split())
    for a in ANCRAGES:
        if t["id"] not in a["ids"] or _accord(a, t, d):
            continue
        if a["dim"] == "QT":
            for fx, exige in (("F1", a["f1"]), ("F3", a["f3"])):
                if exige is not None:
                    (f.add if exige else f.discard)(fx)
            d["QT"] = max(1, 5 - ("F1" in f) - ("F3" in f) - (1 if t["C"] <= 3 else 0))
        else:
            lang = 1 if a["dim"] == "ES" and t["id"] in LANGUE else 0
            n = d[a["dim"]] + lang
            d[a["dim"]] = min(_compatibles(a, t["id"]), key=lambda v: (abs(v - n), v)) - lang
    return d


def ancrer(t):
    """Notes Eurofound du triplet apres ancrage, provenance par dimension et notes modifiees."""
    d = dimensions(t)
    liste = [a for a in ANCRAGES if t["id"] in a["ids"]]
    modifs = []
    for a in liste:
        if _statut(a, t) == "S" and not _accord(a, t, d):
            lang = 1 if a["dim"] == "ES" and t["id"] in LANGUE else 0
            n = d[a["dim"]] + lang
            nouveau = min(_compatibles(a, t["id"]), key=lambda v: (abs(v - n), v)) - lang
            modifs.append((a["dim"], d[a["dim"]], nouveau, a["code"]))
            d[a["dim"]] = nouveau
    prov = {}
    for dim in ("EP", "IT", "QT", "ES", "CA", "PS"):
        aa = [a for a in liste if a["dim"] == dim]
        statuts = [_statut(a, t) for a in aa]
        tensions = [a["code"] for a in aa if not _accord(a, t, d)]
        if dim == "CA":
            prov[dim] = ("mixte", [], [])
        elif "S" in statuts:
            prov[dim] = ("sourcée", [a["code"] for a in aa], tensions)
        elif aa:
            prov[dim] = ("mixte", [a["code"] for a in aa], tensions)
        else:
            prov[dim] = ("estimée", [], [])
    return d, prov, modifs
