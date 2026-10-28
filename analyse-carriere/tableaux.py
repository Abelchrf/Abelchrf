# -*- coding: utf-8 -*-
"""Genere tableaux.md (tableaux du rapport, version 5) a partir de modele.py."""
import json
import os
import re
from collections import Counter

import modele as m

T = m.T
ID = {t["id"]: t for t in T}
ICI = os.path.dirname(os.path.abspath(__file__))
NOMS = {"C": "controle", "Ch": "charge", "R": "relations", "Se": "securite", "Sn": "sens", "Rev": "revenu", "L": "lieu"}

ACCENTS = [
    ("Medecine", "Médecine"), ("Medecin", "Médecin"), ("medecin", "médecin"), ("generaliste", "généraliste"),
    ("liberaux", "libéraux"), ("liberal", "libéral"), ("salaries", "salariés"), ("salarie", "salarié"),
    ("specialites", "spécialités"), ("specialiste", "spécialiste"), ("Specialite", "Spécialité"), ("specialite", "spécialité"),
    ("independant", "indépendant"), ("Masseur-kinesitherapeute", "Masseur-kinésithérapeute"),
    ("anesthesiste", "anesthésiste"), ("Ergotherapeute", "Ergothérapeute"), ("ergotherapeute", "ergothérapeute"),
    ("Pedicure", "Pédicure"), ("Dieteticien", "Diététicien"), ("dietetique", "diététique"), ("Veterinaire", "Vétérinaire"),
    ("veterinaires", "vétérinaires"), ("Osteopathe", "Ostéopathe"), ("Developpeur", "Développeur"), ("Ingenieur", "Ingénieur"),
    ("d'ingenieurs", "d'ingénieurs"), ("ingenieurs", "ingénieurs"), ("reseaux", "réseaux"), ("cybersecurite", "cybersécurité"),
    ("Electricien", "Électricien"), ("ecoles", "écoles"), ("certifies", "certifiés"), ("certifie", "certifié"),
    ("Attache", "Attaché"), ("attache", "attaché"), ("Controleur", "Contrôleur"), ("aerien", "aérien"), ("europeen", "européen"),
    ("Employe", "Employé"), ("employes", "employés"), ("reference", "référence"), ("Quebec", "Québec"), ("resident", "résident"),
    ("Perimetre", "Périmètre"), ("estime", "estimé"), ("Estime", "Estimé"), ("mediane", "médiane"), ("serie", "série"),
    ("recuperee", "récupérée"), ("remuneree", "rémunérée"), ("remuneres", "rémunérés"), ("remunere", "rémunéré"),
    ("Selectivite", "Sélectivité"), ("selectif", "sélectif"), ("Selectif", "Sélectif"), ("Tres", "Très"), ("reussite", "réussite"),
    ("annee", "année"), ("sante", "santé"), ("rentree", "rentrée"), ("debut", "début"), ("carriere", "carrière"),
    ("privee", "privée"), ("prives", "privés"), ("Fenetre", "Fenêtre"), ("etablissement", "établissement"),
    ("experience", "expérience"), ("mobilite", "mobilité"), ("creation", "création"), ("vehicule", "véhicule"),
    ("Ecole", "École"), ("ecole", "école"), ("residence", "résidence"), ("depot", "dépôt"), ("finances)", "financés)"),
    ("neo-bacheliers", "néo-bacheliers"), ("reservee", "réservée"), ("Marche", "Marché"), ("marche sature", "marché saturé"),
    ("derogation", "dérogation"), ("enchainement", "enchaînement"), ("revolus", "révolus"), ("mathematiques", "mathématiques"),
    ("Kine", "Kiné"), ("acces kine", "accès kiné"), ("Fachsprachprufung", "Fachsprachprüfung"), ("TV-Arzte", "TV-Ärzte"),
    ("A1 ", "Ä1 "), ("diplome exempte", "diplôme exempté"), ("diplomes", "diplômés"), ("hopital", "hôpital"),
    ("hospitalieres", "hospitalières"), ("medicaux", "médicaux"), ("pediatres", "pédiatres"), ("ecart", "écart"),
    ("competence", "compétence"), ("periode", "période"), ("Destatis avril", "Destatis avril"), ("tous ages", "tous âges"),
    ("anciennete", "ancienneté"), ("reeducateurs", "rééducateurs"), ("paramedicale", "paramédicale"),
    ("interne", "interne"), ("revalorise", "revalorisé"), ("Observatoire de l'activite", "Observatoire de l'activité"),
    ("deficit", "déficit"), ("Reussite", "Réussite"), ("theorique", "théorique"), ("verifiee", "vérifiée"),
    ("integre", "intégré"), ("Concours de niveau", "Concours de niveau"), ("Recrutement", "Recrutement"),
    ("acquereur endette", "acquéreur endetté"), ("pret", "prêt"), ("Pret", "Prêt"), ("apres", "après"),
    ("officine", "officine"), ("Tests", "Tests"), ("psychotechniques", "psychotechniques"), ("eleve", "élevé"),
    ("elevee", "élevée"), ("Idem", "Idem"), ("maieutique", "maïeutique"), ("mili", "mili"),
    ("echelon", "échelon"), ("IM ", "IM "), ("grille B", "grille B"), ("a bac+3", "à bac+3"), (" a 40 ans", " à 40 ans"),
    (" a 12 ans", " à 12 ans"), (" a 10 ans", " à 10 ans"), (" a 5 ans", " à 5 ans"), (" a 120 500", " à 120 500"),
    (" a 443", " à 443"), (" a 101", " à 101"), (" a 2 678", " à 2 678"), (" a 1 617", " à 1 617"), (" a 3 100", " à 3 100"),
    (" a 3 579", " à 3 579"), (" a 727", " à 727"), (" a 558", " à 558"), (" a 5 000", " à 5 000"), (" a 34 kEUR", " à 34 kEUR"),
    (" a 3 ans", " à 3 ans"), (" a 16 mois", " à 16 mois"), (" a 8 kEUR", " à 8 kEUR"), (" a 10 kEUR", " à 10 kEUR"),
    (" a 58 places", " à 58 places"), (" a 35 %", " à 35 %"), (" a 35 ans", " à 35 ans"), (" a 9 kEUR", " à 9 kEUR"),
    ("5-9 kEUR", "5 à 9 kEUR"), (" a 1 instituts", " à 1 instituts"), ("au Luxembourg", "au Luxembourg"),
    ("controle", "contrôle"), ("securite", "sécurité"), ("Entree", "Entrée"), ("entree", "entrée"),
    ("Elimines", "Éliminés"), ("Elimine", "Éliminé"), ("domines", "dominés"), ("Domine", "Dominé"), ("domine", "dominé"),
    ("scenarios", "scénarios"), ("scenario", "scénario"), ("tries", "triés"), ("decroissant", "décroissant"),
    ("conserve", "conservé"), ("rang median", "rang médian"), ("barriere", "barrière"), ("Barriere", "Barrière"),
    ("Med. ", "Méd. "), ("Src med.", "Src méd."), ("Annees", "Années"), ("annees", "années"), ("Frontiere", "Frontière"), ("frontiere", "frontière"),
    ("Egalites", "Égalités"), ("inferieur", "inférieur"), ("Sensibilite", "Sensibilité"), ("Poids egaux", "Poids égaux"),
    ("(estimees)", "(estimées)"), ("sourcees", "sourcées"), ("ajustees", "ajustées"), ("bien-etre", "bien-être"),
    ("pondere", "pondéré"), ("criteres", "critères"), ("critere", "critère"), ("Ce qu'on gagne en montant d'un cran", "Gain en montant d'un cran"),
    ("au moins aussi bien partout, et mieux sur", "au moins aussi bien partout, et mieux sur"),
    ("Audioprothesiste", "Audioprothésiste"), ("capacite", "capacité"), ("pres du", "près du"), ("condition d'age", "condition d'âge"),
    ("meme ordre", "même ordre"), ("### A moins", "### À moins"), ("inférieur a 0", "inférieur à 0"),
    ("jusqu'a ", "jusqu'à "),
    ("cloud et DevOps", "cloud et DevOps"), ("cybersecurite", "cybersécurité"), ("methodes-industrialisation", "méthodes-industrialisation"),
    ("administration systemes", "administration systèmes"), ("mastere", "mastère"), ("donnees", "données"), ("sources privees", "sources privées"),
    ("specialites", "spécialités"), ("specialite cloud", "spécialité cloud"), ("confirme)", "confirmé)"), ("a pourvoir", "à pourvoir"),
    ("de 2019 a 2024", "de 2019 à 2024"), ("poste 24", "posté 24"), ("bas de fourchette", "bas de fourchette"), ("a 5-10 ans", "à 5-10 ans"),
    ("Etats-Unis", "États-Unis"), ("americain", "américain"), ("developpeurs", "développeurs"), ("trouvee", "trouvée"),
    ("projetee", "projetée"), ("ponderee", "pondérée"), ("a la charge de", "à la charge de"), ("a l'etranger", "à l'étranger"),
    ("d'Etat", "d'État"), ("equivalence", "équivalence"), ("2 a 3 ans", "2 à 3 ans"), (" a Ohio State", " à Ohio State"),
    ("de 2024 a 2034", "de 2024 à 2034"), (" a Dublin", " à Dublin"), ("65 000 a 80 000", "65 000 à 80 000"),
    ("teletravail", "télétravail"),
    ("Fiabilite", "Fiabilité"), ("fiabilite", "fiabilité"), ("installe", "installé"), ("Installe", "Installé"),
    ("officielle ajustee", "officielle ajustée"), ("privee", "privée"), ("estimee", "estimée"), ("Modifications", "Modifications"),
    ("Egalites declarees", "Égalités déclarées"), ("ecart inferieur", "écart inférieur"), ("declare", "déclaré"),
    ("criteres", "critères"), ("Variation", "Variation"), ("croise par", "croisé par"), ("score propre", "score propre"),
    ("quasi inchange", "quasi inchangé"), ("retire", "retiré"), ("re-source", "re-sourcé"), ("notes modifiees", "notes modifiées"),
    ("Rang v3", "Rang v3"), ("Rang v4", "Rang v4"), ("informatif", "informatif"), ("hors score", "hors score"),
    ("Annees de revenu perdues", "Années de revenu perdues"), ("Age d'entree", "Âge d'entrée"),
    ("par rapport a la", "par rapport à la"), ("regle d'egalite", "règle d'égalité"), ("nouvelle regle", "nouvelle règle"),
    ("Decomposition de l'ecart", "Décomposition de l'écart"), ("Ecart pondere", "Écart pondéré"), ("classe sous", "classé sous"),
    ("kEUR", "k€"), ("EUR", "€"),
]


def fr(s):
    for a, b in ACCENTS:
        s = s.replace(a, b)
    return s


def k(x):
    return f"{x / 1000:.0f}"


def tri(t):
    return f"{t['metier']} x {t['statut']} x {t['pays']}"


def pal(t, w="W", p="palier"):
    return t[p] + ("*" if m.proche_frontiere(t[w]) else "")


def rg(t):
    return f"{t['rang']}{'=' if t['groupe'] > 1 else ''}"


def d2(x):
    return f"{x:+.2f}"


out = []
A = out.append
EU = m.EU
CFG = list(m.VARIANTES5)
COURT = {"Poids égaux": "égaux", "environnement physique doublé": "EP×2", "intensité du travail doublé": "IT×2",
         "qualité du temps de travail doublé": "QT×2", "environnement social doublé": "ES×2",
         "compétences et autonomie doublé": "CA×2", "perspectives et sécurité doublé": "PS×2", "revenu doublé": "RE×2"}


def note(x):
    return f"{x:.1f}" if isinstance(x, float) and abs(x - round(x)) > 1e-9 else f"{x:.0f}"


# --- Pool ---------------------------------------------------------------------
A(f"### Pool ({len(T)} triplets)\n")
A("| ID | Triplet | ID | Triplet |")
A("|---|---|---|---|")
half = (len(T) + 1) // 2
for i in range(half):
    a = T[i]
    b = T[i + half] if i + half < len(T) else None
    A(f"| {a['id']} | {tri(a)} | {b['id'] if b else ''} | {tri(b) if b else ''} |")
A("")

# --- Partie A : notes Eurofound puis palier ---------------------------------------------------
A("### Classement v5, partie A : notes des 7 dimensions Eurofound, puis palier\n")
A("| Rang | ID | Triplet | EP | IT | QT | ES | CA | PS | RE | Palier | Top 10 (sur 8 configurations) |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|")
for t in m.CLASSEMENT:
    A(f"| {rg(t)} | {t['id']} | {tri(t)} | " + " | ".join(note(t[d]) for d in EU.DIMS) + f" | {pal(t)} | {t['nb_top']} |")
A("")

# --- Partie B : revenu equivalent temps plein ---------------------------------------------------
A("### Classement v5, partie B : revenu net en équivalent temps plein\n")
A("| Rang | ID | Médian au temps réel nom./PPA k€ | Temps de travail et quotité | Médian ETP nom./PPA k€ | P80 ETP nom./PPA k€ | Source du médian | Source du P80 | Fiabilité |")
A("|---|---|---|---|---|---|---|---|---|")
for t in m.CLASSEMENT:
    A(f"| {rg(t)} | {t['id']} | {k(t['med_nom'])} / {k(t['med_ppa'])} | {t['etp']} (quotité {t['q']:.2f}) | "
      f"{k(t['med_etp_nom'])} / {k(t['med_etp_ppa'])} | {k(t['p80_etp_nom'])} / {k(t['p80_etp_ppa'])} | {t['src_med']} | {t['src_p80']} | {t['fiab']} |")
A("")

# --- Partie C : provenance des notes hors revenu --------------------------------------------------
A("### Classement v5, partie C : provenance des notes hors revenu\n")
A("S = sourcée : chiffre officiel et chiffré pour le métier lui-même, dans le pays du triplet. "
  "M = mixte : chiffre pour un groupe plus large, un autre pays ou un autre statut, sans ampleur publiée, "
  "issu d'une enquête non officielle, ou ne couvrant qu'une partie de la dimension (QT et CA sont au mieux M). "
  "E = estimée : aucun chiffre trouvé, note de la grille normative. "
  "Ancrages : codes de la partie C2. Tensions : note maintenue alors qu'un chiffre de statut M indique une autre valeur.\n")
A("| Rang | ID | EP | IT | QT | ES | CA | PS | Ancrages | Tensions |")
A("|---|---|---|---|---|---|---|---|---|---|")
LETTRE = {"sourcée": "S", "mixte": "M", "estimée": "E"}
D6 = ("EP", "IT", "QT", "ES", "CA", "PS")
compte = Counter()
for t in m.CLASSEMENT:
    p = t["prov"]
    for d in D6:
        compte[(d, p[d][0])] += 1
    anc = " ; ".join(f"{d} {', '.join(p[d][1])}" for d in D6 if p[d][1])
    ten = " ; ".join(f"{d} ({', '.join(p[d][2])})" for d in D6 if p[d][2])
    A(f"| {rg(t)} | {t['id']} | " + " | ".join(LETTRE[p[d][0]] for d in D6) + f" | {anc or 'aucun'} | {ten or 'aucune'} |")
A("")
A("| Dimension | Sourcées | Mixtes | Estimées |")
A("|---|---|---|---|")
for d in D6:
    A(f"| {d} | {compte[(d, 'sourcée')]} | {compte[(d, 'mixte')]} | {compte[(d, 'estimée')]} |")
tot = {s: sum(compte[(d, s)] for d in D6) for s in LETTRE}
A(f"| Total ({6 * len(T)} notes) | {tot['sourcée']} | {tot['mixte']} | {tot['estimée']} |")
A("")


def ens(s):
    v = sorted(s)
    if len(v) > 2 and v == list(range(v[0], v[-1] + 1)):
        return f"{v[0]} à {v[-1]}"
    return " ou ".join(str(x) for x in v)


A("### Classement v5, partie C2 : ancrages utilisés\n")
A("Règles de conversion et de statut : section 1.13. Notes compatibles : valeurs que le chiffre autorise (pour QT, présence ou absence des facteurs F1 et F3).\n")
A("| Code | Dim. | Chiffre publié | Source | Statut | Notes compatibles | Triplets couverts | Tensions |")
A("|---|---|---|---|---|---|---|---|")
for a in EU.ANCRAGES:
    par = {}
    for i in a["ids"]:
        par.setdefault(EU._statut(a, ID[i]), []).append(i)
    statut = next(iter(par)) if len(par) == 1 else " ; ".join(f"{s} : {', '.join(ids)}" for s, ids in sorted(par.items()))
    if a["dim"] == "QT":
        compat = " ; ".join(f"{fx} {'présent' if ex else 'absent'}" for fx, ex in (("F1", a["f1"]), ("F3", a["f3"])) if ex is not None)
    elif isinstance(a["ok"], dict):
        grp = {}
        for i, s in a["ok"].items():
            grp.setdefault(ens(s), []).append(i)
        compat = " ; ".join(f"{v} ({', '.join(ids)})" for v, ids in grp.items())
    else:
        compat = ens(a["ok"])
    tens = [i for i in a["ids"] if not EU._accord(a, ID[i], ID[i])]
    A(f"| {a['code']} | {a['dim']} | {a['texte']} | {a['src']} | {statut} | {compat} | {', '.join(a['ids'])} | {', '.join(tens) or 'aucune'} |")
A("")
A("### Notes modifiées par un ancrage de statut S\n")
for t in T:
    for dim, avant, apres, code in t["modifs"]:
        A(f"- {t['id']} {tri(t)} : {dim} {avant} → {apres} ({code}).")
A("")

# --- Partie D : barriere et IA (informatif) ------------------------------------------------------
A("### Classement v5, partie D : barrière d'entrée, risque IA et dominance (informatif, hors score)\n")
A("| Rang | ID | Âge d'entrée | Formation et financement | Sélectivité | Années de revenu perdues | Cumul 24-45 ans PPA k€ | IA : exposition, palier si IA fort | Dominé sur les 7 dimensions par |")
A("|---|---|---|---|---|---|---|---|---|")
for t in m.CLASSEMENT:
    A(f"| {rg(t)} | {t['id']} | {t['E']} ans | {t['fin']} | {t['sel']} | {t['pertes']:.1f} | {k(t['cum_ppa'])} | {t['ia']}, {pal(t, 'W_ia', 'palier_ia')} | {', '.join(t['domine_par']) or 'aucun'} |")
A("")

# --- Robustesse ---------------------------------------------------------------------------------
A("### Robustesse : rang dans chacune des 8 configurations de poids\n")
A("Configurations : poids égaux, puis chaque dimension doublée à son tour. Haut du classement = 10 premiers, rangs partagés compris. Sont listés les triplets présents au moins une fois dans le haut du classement.\n")
A("| ID | Triplet | " + " | ".join(COURT[c] for c in CFG) + " | Top 10 (sur 8) |")
A("|---|---|" + "---|" * len(CFG) + "---|")
for t in sorted([t for t in T if t["nb_top"] >= 1], key=lambda t: (-t["nb_top"], t["rangs_var"]["Poids égaux"])):
    A(f"| {t['id']} | {tri(t)} | " + " | ".join(str(t["rangs_var"][c]) for c in CFG) + f" | {t['nb_top']} |")
A("")
cites = ["Poids égaux", "revenu doublé", "compétences et autonomie doublé", "perspectives et sécurité doublé"]
noyau4 = [t for t in m.CLASSEMENT if all(t["rangs_var"][c] <= m.TOP for c in cites)]
A("### Noyau robuste et triplets fragiles\n")
A("- Dans le haut du classement dans les 8 configurations : " + (", ".join(f"{t['id']} {tri(t)}" for t in m.ROBUSTES) or "aucun") + ".")
A("- Dans le haut du classement dans les 4 configurations citées dans la demande (poids égaux, revenu, autonomie et sécurité doublés) : " + (", ".join(f"{t['id']} {tri(t)}" for t in noyau4) or "aucun") + ".")
A("- Dans le haut du classement dans une seule configuration : " + (", ".join(f"{t['id']} {tri(t)} ({COURT[[c for c in CFG if t['rangs_var'][c] <= m.TOP][0]]})" for t in m.UNE_SEULE) or "aucun") + ".")
A("")
A("### Sensibilité aux notes en tension (informatif, hors classement)\n")
A("Poids égaux ; chaque note en tension avec un chiffre de statut M prend la valeur compatible avec ce chiffre (partie C2). Les autres triplets gardent leur score.\n")
A("| ID | Triplet | Note en tension | Rang v5 | Rang si chiffre appliqué | Palier v5 | Palier si chiffre appliqué |")
A("|---|---|---|---|---|---|---|")
for t in m.CLASSEMENT:
    tn = [f"{d} ({', '.join(t['prov'][d][2])})" for d in D6 if t["prov"][d][2]]
    if not tn:
        continue
    r2, g2 = m.RANG_TENSION[t["id"]]
    A(f"| {t['id']} | {tri(t)} | {' ; '.join(tn)} | {rg(t)} | {r2}{'=' if g2 > 1 else ''} | {pal(t)} | {m.classer(t['W_tension'])} |")
A("")

# --- Egalites et frontieres ------------------------------------------------------------------------
A("### Égalités déclarées (écart inférieur à 0,03 avec le premier du groupe)\n")
groupes = {}
for t in m.CLASSEMENT:
    groupes.setdefault(t["rang"], []).append(t["id"])
lignes_eg = [f"rang {r} : {' = '.join(ids)}" for r, ids in groupes.items() if len(ids) > 1]
A(" ; ".join(lignes_eg) if lignes_eg else "aucune")
A("")
A("### À moins de 0,1 d'une frontière de palier\n")
A(", ".join(f"{t['id']} ({t['palier']})" for t in m.CLASSEMENT if m.proche_frontiere(t["W"])))
A("")

# --- Conversion des notes v4 vers Eurofound ----------------------------------------------------------
A("### Conversion des notes v4 vers les dimensions Eurofound, triplet par triplet\n")
A("Facteurs de l'ancienne charge : F1 plus de 45 h, F2 intensité ou exigences émotionnelles, F3 nuits, week-ends ou astreintes, F4 pénibilité physique, F5 trajet (hors grille). H = horaires imposés (contrôle v4 de 3 ou moins).\n")
A("ES reprend les relations v4 et PS la sécurité v4, sauf note modifiée par un ancrage de statut S (code entre parenthèses).\n")
A("| ID | Groupe de métiers | Facteurs | Charge v4 | Contrôle v4 | H | CITP-08 (niveau) | EP | IT | QT | CA | Relations v4 → ES | Sécurité v4 → PS |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
MODIF = {(t["id"], dim): code for t in T for dim, _, _, code in t["modifs"]}


def vers(t, v4, dim):
    c = MODIF.get((t["id"], dim))
    return f"{t[v4]} → {t[dim]} ({c})" if c else f"{t[v4]} → {t[dim]}"


for t in T:
    g = EU.groupe_de(t["id"])[0].replace("_", " ")
    code, niv = EU.CITP[t["id"]]
    A(f"| {t['id']} | {g} | {EU.FACTEURS[t['id']] or 'aucun'} | {t['Ch']} | {t['C']} | {1 if t['C'] <= 3 else 0} | {code} ({niv}) | {t['EP']} | {t['IT']} | {t['QT']} | {note(t['CA'])} | {vers(t, 'R', 'ES')} | {vers(t, 'Se', 'PS')} |")
A("")

# --- Modifications de rang v4 -> v5 --------------------------------------------------------------------
v4 = json.load(open(os.path.join(ICI, "rangs_v4.json"), encoding="utf-8"))
P4 = {"C": 22, "Ch": 19, "R": 15, "Se": 15, "Sn": 6, "Rev": 15, "L": 8}
BLOCS = {
    "conditions de travail (EP, IT, QT ; ancienne charge)": lambda t, d: (t["EP"] + t["IT"] + t["QT"]) / 7 - P4["Ch"] * d["Ch"] / 100,
    "autonomie et compétences (CA ; ancien contrôle)": lambda t, d: t["CA"] / 7 - P4["C"] * d["C"] / 100,
    "environnement social (ES ; anciennes relations)": lambda t, d: t["ES"] / 7 - P4["R"] * d["R"] / 100,
    "perspectives et sécurité (PS)": lambda t, d: t["PS"] / 7 - P4["Se"] * d["Se"] / 100,
    "revenu (RE, équivalent temps plein)": lambda t, d: t["RE"] / 7 - P4["Rev"] * d["Rev"] / 100,
    "sens retiré": lambda t, d: -P4["Sn"] * d["Sn"] / 100,
    "lieu (télétravail) retiré": lambda t, d: -P4["L"] * d["L"] / 100,
}
moy = {b: sum(f(t, v4[t["id"]]) for t in T) / len(T) for b, f in BLOCS.items()}
A("### Modifications de rang par rapport à la version 4\n")
A("Chaque bloc compare la contribution d'un groupe de critères au score v5 et au score v4, par rapport à la moyenne des 93 triplets : un nombre positif fait monter le triplet. Les deux blocs les plus forts sont indiqués.\n")
A("| ID | Triplet | Rang v4 | Rang v5 | Variation | Ce qui l'explique |")
A("|---|---|---|---|---|---|")
for t in m.CLASSEMENT:
    d = v4[t["id"]]
    s_old = f"{d['rang']}{'=' if d['groupe'] > 1 else ''}"
    if s_old == rg(t):
        continue
    contrib = sorted(((b, f(t, d) - moy[b]) for b, f in BLOCS.items()), key=lambda x: -abs(x[1]))[:2]
    expl = " ; ".join(f"{b} ({d2(v)})" for b, v in contrib)
    var = d["rang"] - t["rang"]
    A(f"| {t['id']} | {tri(t)} | {s_old} | {rg(t)} | {'+' if var > 0 else ''}{var} | {expl} |")
A("")

# --- Cellules a signaler ---------------------------------------------------------------------------------
A("### Cellules revenu sans source fiable ou sans temps de travail réel\n")
A("- Sans source fiable ou non officielles : " + (", ".join(f"{t['id']} ({t['fiab']})" for t in T if t["fiab"] in ("estimee", "sans source fiable", "non officielle", "non re-sourcée")) or "aucune") + ".")
A("- Temps de travail réel non trouvé (pas de conversion en équivalent temps plein) : " + (", ".join(t["id"] for t in T if not t["etp_ok"]) or "aucune") + ".")
A("")

texte = fr("\n".join(out) + "\n")
texte = re.sub(r"(?<=\d)\.(?=\d)", ",", texte)  # decimales a la francaise
texte = texte.replace("section 1,13", "section 1.13").replace("grille 1,3", "grille 1.3")  # numeros de section
texte = texte.replace(" x ", " × ")
with open(os.path.join(ICI, "tableaux.md"), "w", encoding="utf-8") as f:
    f.write(texte)
print("ok", len(T), "triplets")
