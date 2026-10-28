# -*- coding: utf-8 -*-
"""Genere tableaux.md (tableaux du rapport, version 4) a partir de modele.py."""
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

# --- Classement v4, partie A : notes puis palier ----------------------------------
A("### Classement v4, partie A : notes par critere, puis palier\n")
A("| Rang | ID | Triplet | C (22) | Ch (19) | R (15) | Se (15) | Sn (6) | L (8) | Rev (15) | Palier |")
A("|---|---|---|---|---|---|---|---|---|---|---|")
for t in m.CLASSEMENT:
    A(f"| {rg(t)} | {t['id']} | {tri(t)} | {t['C']} | {t['Ch']} | {t['R']} | {t['Se']} | {t['Sn']} | {t['L']} | {t['Rev']:.1f} | {pal(t)} |")
A("")

# --- Partie B : cellules revenu ------------------------------------------------------
A("### Classement v4, partie B : cellules revenu (net, professionnel installe)\n")
A("| Rang | ID | Median nom./PPA kEUR | Source du median | P80 nom./PPA kEUR | Source du P80 | Temps de travail reel | Fiabilite |")
A("|---|---|---|---|---|---|---|---|")
for t in m.CLASSEMENT:
    A(f"| {rg(t)} | {t['id']} | {k(t['med_nom'])} / {k(t['med_ppa'])} | {t['src_med']} | {k(t['p80i_nom'])} / {k(t['p80i_ppa'])} | {t['src_p80']} | {t['h']} | {t['fiab']} |")
A("")

# --- Partie C : barriere informative --------------------------------------------------
A("### Classement v4, partie C : barriere d'entree et risque IA (informatif, hors score)\n")
A("| Rang | ID | Age d'entree | Formation et financement | Selectivite | Annees de revenu perdues | Cumul 24-45 ans PPA kEUR | IA : exposition, palier si IA fort | Domine sur les 7 criteres par |")
A("|---|---|---|---|---|---|---|---|---|")
for t in m.CLASSEMENT:
    A(f"| {rg(t)} | {t['id']} | {t['E']} ans | {t['fin']} | {t['sel']} | {t['pertes']:.1f} | {k(t['cum_ppa'])} | {t['ia']}, {pal(t, 'W_ia', 'palier_ia')} | {', '.join(t['domine_par']) or 'aucun'} |")
A("")

# --- Egalites -------------------------------------------------------------------------
A("### Egalites declarees (ecart inferieur a 0,03 avec le premier du groupe)\n")
groupes = {}
for t in m.CLASSEMENT:
    groupes.setdefault(t["rang"], []).append(t["id"])
lignes_eg = [f"rang {r} : {' = '.join(ids)}" for r, ids in groupes.items() if len(ids) > 1]
A(" ; ".join(lignes_eg) if lignes_eg else "aucune")
A("")

# --- Frontieres de palier -------------------------------------------------------------
A("### A moins de 0,1 d'une frontiere de palier\n")
A(", ".join(f"{t['id']} ({t['palier']})" for t in m.CLASSEMENT if m.proche_frontiere(t["W"])))
A("")

# --- Sensibilite aux poids --------------------------------------------------------------
VARIANTES = {
    "Base (22/19/15/15/6/15, lieu 8)": m.POIDS,
    "Poids egaux (7 criteres)": {kk: 100 / len(m.POIDS) for kk in m.POIDS},
    "Revenu 30 (18/16/12/12/5/30, lieu 7)": {"C": 18, "Ch": 16, "R": 12, "Se": 12, "Sn": 5, "Rev": 30, "L": 7},
    "Controle 30 (30/17/13/13/5/14, lieu 8)": {"C": 30, "Ch": 17, "R": 13, "Se": 13, "Sn": 5, "Rev": 14, "L": 8},
}
A("### Sensibilite des paliers aux poids (opinion, pas consensus)\n")
A("| Variante | Palier S | Nombre S/A/B/C | Premier |")
A("|---|---|---|---|")
for nom, P in VARIANTES.items():
    sc = {t["id"]: sum(P[c] * t[c] for c in P) / 100 for t in T}
    tiers = {i: m.classer(w) for i, w in sc.items()}
    cnt = Counter(tiers.values())
    s_ids = [i for i, v in sorted(tiers.items(), key=lambda kv: -sc[kv[0]]) if v == "S"]
    premier = max(sc, key=sc.get)
    A(f"| {nom} | {', '.join(s_ids) if s_ids else 'aucun'} | {cnt.get('S', 0)}/{cnt.get('A', 0)}/{cnt.get('B', 0)}/{cnt.get('C', 0)} | {premier} |")
A("")

# --- Pourquoi T89 devant des independants ------------------------------------------------
cyb = ID["T89"]
A("### Pourquoi T89 (cybersecurite, salarie, Suisse) est devant des independants\n")
A("Écart pondéré par critère (poids × différence de note, divisé par 100) entre T89 et chaque libéral, indépendant ou artisan classé sous lui ; un nombre positif favorise T89.\n")
A("| Triplet classe sous T89 | Rang | C | Ch | R | Se | Sn | L | Rev | Total |")
A("|---|---|---|---|---|---|---|---|---|---|")
for t in m.CLASSEMENT:
    if t["W"] >= cyb["W"] or not any(s in t["statut"] for s in ("liberal", "independant", "artisan")):
        continue
    d = {c: m.POIDS[c] * (cyb[c] - t[c]) / 100 for c in m.CRIT}
    A(f"| {t['id']} {tri(t)} | {rg(t)} | " + " | ".join(d2(d[c]) for c in m.CRIT) + f" | {d2(sum(d.values()))} |")
A("")

# --- Modifications de rang par rapport a la v3 ----------------------------------------------
v3 = json.load(open(os.path.join(ICI, "rangs_v3.json"), encoding="utf-8"))
r3 = m.rangs_partages([{"id": i, "W": d["W"]} for i, d in v3.items()], seuil=0.005)
lo_m, hi_m = min(d["m40_ppa"] for d in v3.values()), max(d["m40_ppa"] for d in v3.values())
lo_p, hi_p = min(d["p80_ppa"] for d in v3.values()), max(d["p80_ppa"] for d in v3.values())


def ech(x, lo, hi):
    import math
    return max(1.0, min(5.0, 1 + 4 * (math.log(x) - math.log(lo)) / (math.log(hi) - math.log(lo))))


A("### Modifications de rang par rapport a la version 3\n")
A("Décomposition de l'écart de score de chaque triplet : (1) cumul 24-45 ans retiré du score revenu ; (2) notes modifiées ; (3) cellules revenu re-sourcées (médian et P80 installés, nouvelles bornes). Rang v3 avec la règle d'égalité de la v3 (écart inférieur à 0,005), rang v4 avec la nouvelle règle (0,03). Seuls les triplets dont le rang change sont listés.\n")
A("| ID | Triplet | Rang v3 | Rang v4 | Variation | Cellule qui l'explique |")
A("|---|---|---|---|---|---|")
pos4 = {t["id"]: i for i, t in enumerate(m.CLASSEMENT, 1)}
pos3 = {i: d["pos"] for i, d in v3.items()}
for t in m.CLASSEMENT:
    d = v3[t["id"]]
    rev_a = (ech(d["m40_ppa"], lo_m, hi_m) + ech(d["p80_ppa"], lo_p, hi_p)) / 2
    w_a = d["W"] + m.POIDS["Rev"] * (rev_a - d["Rev"]) / 100
    notes = {c: t[c] - d[c] for c in ("C", "Ch", "R", "Se", "Sn", "L") if t[c] != d[c]}
    w_b = w_a + sum(m.POIDS[c] * v for c, v in notes.items()) / 100
    parts = [("cumul 24-45 ans retire du score", w_a - d["W"])]
    for c, v in notes.items():
        parts.append((f"{NOMS[c]} {d[c]} vers {t[c]}", m.POIDS[c] * v / 100))
    parts.append((f"revenu installé re-sourcé : médian {k(d['m40_ppa'])} vers {k(t['med_ppa'])} k€ PPA, P80 {k(d['p80_ppa'])} vers {k(t['p80i_ppa'])}", t["W"] - w_b))
    parts = [p for p in parts if abs(p[1]) >= 0.005]
    parts.sort(key=lambda p: -abs(p[1]))
    r_old, r_new = r3[t["id"]], (t["rang"], t["groupe"])
    s_old = f"{r_old[0]}{'=' if r_old[1] > 1 else ''}"
    var = r_old[0] - t["rang"]
    if var == 0 and s_old == rg(t):
        continue
    croise = [i for i in pos3 if (pos3[i] < pos3[t["id"]]) != (pos4[i] < pos4[t["id"]]) and i != t["id"]]
    expl = " ; ".join(f"{n} ({d2(v)})" for n, v in parts) or "score propre quasi inchange"
    if croise and len(croise) <= 4:
        expl += " ; croise par " + ", ".join(sorted(croise, key=lambda i: pos4[i]))
    elif croise:
        expl += f" ; croise par {len(croise)} triplets"
    A(f"| {t['id']} | {tri(t)} | {s_old} | {rg(t)} | {'+' if var > 0 else ''}{var} | {expl} |")
A("")

# --- Cellules sans source fiable -----------------------------------------------------------
A("### Cellules revenu sans source fiable\n")
A(", ".join(f"{t['id']} ({t['fiab']})" for t in T if t["fiab"] in ("estimee", "sans source fiable", "privee", "provisoire")) or "aucune")
A("")

texte = fr("\n".join(out) + "\n")
texte = re.sub(r"(?<=\d)\.(?=\d)", ",", texte)  # decimales a la francaise
texte = texte.replace(" x ", " × ")
with open(os.path.join(ICI, "tableaux.md"), "w", encoding="utf-8") as f:
    f.write(texte)
print("ok", len(T), "triplets")
