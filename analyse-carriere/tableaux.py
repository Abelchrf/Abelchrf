# -*- coding: utf-8 -*-
"""Genere tableaux.md (tableaux du rapport) a partir de modele.py."""
import os
import re
from collections import Counter

import modele as m

T = m.T
FIN = [t for t in T if not t["domine_par"]]
ID = {t["id"]: t for t in T}

# Sources du P80 quand elles different de la regle generale (ratio estime par statut).
SRC80 = {
    "T23": "S64 haut de fourchette ; est.", "T24": "S64 haut de fourchette ; est.",
    "T28": "S35 (Q3 45 CAD/h)", "T36": "S19 (TJM 15 ans et plus : 672 EUR) ; est.",
    "T67": "S18 ; est.", "T05": "S04 (ecart moyenne/mediane) ; est.",
}


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
    ("kEUR", "k€"), ("EUR", "€"),
]


def fr(s):
    for a, b in ACCENTS:
        s = s.replace(a, b)
    return s


def codes(s):
    c = sorted(set(re.findall(r"S\d\d", s)))
    est = "estime" in s or "est." in s
    if not c:
        return "est."
    return ",".join(c) + (" ; est." if est else "")


def k(x):
    return f"{x / 1000:.0f}"


def pct(p):
    return f"{p * 100:.0f} %"


def tri(t):
    return f"{t['metier']} x {t['statut']} x {t['pays']}"


def pal(t, w="W", p="palier"):
    return t[p] + ("*" if m.proche_frontiere(t[w]) else "")


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

# --- Elimination -----------------------------------------------------------------
A("### Elimines (domines dans les deux scenarios IA)\n")
A("| Elimine | Domine par | Pourquoi (le dominant fait au moins aussi bien partout, et mieux sur) |")
A("|---|---|---|")
noms = {"C": "controle", "Ch": "charge", "R": "relations", "Se": "securite", "Sn": "sens", "Rev": "revenu"}
for x in T:
    if not x["domine_par"]:
        continue
    restants = [i for i in x["domine_par"] if not ID[i]["domine_par"]]
    y = ID[(restants or x["domine_par"])[0]]
    mieux = [noms[c] for c in m.CRIT if y[c] > x[c] + 1e-9]
    if y["E"] < x["E"]:
        mieux.append(f"entree {y['E']} ans au lieu de {x['E']}")
    if round(y["pertes"], 1) < round(x["pertes"], 1):
        mieux.append(f"annees perdues {y['pertes']:.1f} au lieu de {x['pertes']:.1f}")
    if y["p"] > x["p"]:
        mieux.append(f"p {pct(y['p'])} au lieu de {pct(x['p'])}")
    if y["cap"] < x["cap"]:
        mieux.append("moins de capital")
    A(f"| {x['id']} {tri(x)} | {', '.join(x['domine_par'])} | {y['id']} : {', '.join(mieux)} |")
for x in T:
    if not x["domine_par"] and x["domine_base_seul"]:
        A(f"| (conserve) {x['id']} {tri(x)} | {', '.join(x['domine_base_seul'])} sans IA seulement | domination perdue dans le scenario IA fort |")
A("")

# --- Tableau final ------------------------------------------------------------------
A("### Tableau final (non domines, tries par score interne decroissant)\n")
A("| ID | Triplet | Palier | Med. 40 ans nom./PPA kEUR | Src med. | P80 40 ans nom./PPA kEUR | Src P80 | Cumul 24-45 ans PPA kEUR | C | Ch | R | Se | Sn | Entree | Formation et financement | Selectivite | Annees perdues | Indice barriere | IA : exposition, palier si IA fort |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for t in sorted(FIN, key=lambda t: -t["W"]):
    A(f"| {t['id']} | {tri(t)} | {pal(t)} | {k(t['m40_nom'])} / {k(t['m40_ppa'])} | {codes(t['src'])} | "
      f"{k(t['p80_nom'])} / {k(t['p80_ppa'])} | {SRC80.get(t['id'], 'est.')} | {k(t['cum_ppa'])} | "
      f"{t['C']} | {t['Ch']} | {t['R']} | {t['Se']} | {t['Sn']} | {t['E']} ans | {t['fin']} | {t['sel']} | "
      f"{t['pertes']:.1f} | {t['B']:.2f} | {t['ia']}, {pal(t, 'W_ia', 'palier_ia')} |")
A("")

# --- Tableau final scinde (lecture sur ecran etroit) ------------------------------------
A("### Tableau final, partie A : paliers, revenus et criteres\n")
A("| ID | Triplet | Palier | Med. 40 ans nom./PPA kEUR | Src med. | P80 nom./PPA kEUR | Src P80 | Cumul 24-45 PPA kEUR | C | Ch | R | Se | Sn |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for t in sorted(FIN, key=lambda t: -t["W"]):
    A(f"| {t['id']} | {tri(t)} | {pal(t)} | {k(t['m40_nom'])} / {k(t['m40_ppa'])} | {codes(t['src'])} | "
      f"{k(t['p80_nom'])} / {k(t['p80_ppa'])} | {SRC80.get(t['id'], 'est.')} | {k(t['cum_ppa'])} | "
      f"{t['C']} | {t['Ch']} | {t['R']} | {t['Se']} | {t['Sn']} |")
A("")
A("### Tableau final, partie B : barriere d'entree et risque IA (meme ordre)\n")
A("| ID | Entree | Formation et financement | Selectivite | Annees perdues | Indice barriere | IA : exposition, palier si IA fort |")
A("|---|---|---|---|---|---|---|")
for t in sorted(FIN, key=lambda t: -t["W"]):
    A(f"| {t['id']} | {t['E']} ans | {t['fin']} | {t['sel']} | {t['pertes']:.1f} | {t['B']:.2f} | {t['ia']}, {pal(t, 'W_ia', 'palier_ia')} |")
A("")

# --- Frontiere de Pareto -----------------------------------------------------------
A("### Frontiere de Pareto (bien-etre pondere contre indice de barriere)\n")
A("| Rang barriere | ID | Triplet | Indice barriere | Palier | Ce qu'on gagne en montant d'un cran |")
A("|---|---|---|---|---|---|")
prev = None
for i, t in enumerate(m.front, 1):
    gain = "" if prev is None else f"+{t['W'] - prev['W']:.2f} point de score pour +{t['B'] - prev['B']:.2f} de barriere"
    A(f"| {i} | {t['id']} | {tri(t)} | {t['B']:.2f} | {pal(t)} | {gain} |")
    prev = t
A("")

# --- Frontieres de palier et egalites ------------------------------------------------
A("### A moins de 0,1 d'une frontiere de palier\n")
proches = [t for t in sorted(T, key=lambda t: -t["W"]) if m.proche_frontiere(t["W"])]
A(", ".join(f"{t['id']} ({t['palier']})" for t in proches))
A("")
A("### Egalites (ecart de score interne inferieur a 0,005)\n")
eg = []
S_ = sorted(T, key=lambda t: -t["W"])
for i in range(len(S_)):
    for j in range(i + 1, len(S_)):
        if abs(S_[i]["W"] - S_[j]["W"]) < 0.005:
            eg.append(f"{S_[i]['id']} = {S_[j]['id']}")
A(", ".join(eg) if eg else "aucune")
A("")

# --- Sensibilite aux poids -------------------------------------------------------------
VARIANTES = {
    "Base v2 (24/21/16/16/7/16)": m.POIDS,
    "Poids v1 (22/20/15/15/13/15), notes v2": m.POIDS_V1,
    "Poids egaux": {kk: 100 / 6 for kk in m.POIDS},
    "Revenu 30 (17/15/13/13/12/30)": {"C": 17, "Ch": 15, "R": 13, "Se": 13, "Sn": 12, "Rev": 30},
}
A("### Sensibilite des paliers aux poids (opinion, pas consensus)\n")
A("| Variante | Palier S | Nombre S/A/B/C |")
A("|---|---|---|")
for nom, P in VARIANTES.items():
    tiers = {}
    for t in T:
        w = sum(P[c] * (t[c] if c != "Rev" else t["Rev"]) for c in m.POIDS) / 100
        tiers[t["id"]] = m.classer(w)
    cnt = Counter(tiers.values())
    S_ids = [i for i, v in tiers.items() if v == "S"]
    A(f"| {nom} | {', '.join(S_ids) if S_ids else 'aucun'} | {cnt.get('S', 0)}/{cnt.get('A', 0)}/{cnt.get('B', 0)}/{cnt.get('C', 0)} |")
A("")

# --- Marge des triplets S ------------------------------------------------------------------
A("### Marge des triplets S au-dessus de 4,2\n")
for t in sorted(T, key=lambda t: -t["W"]):
    if t["palier"] == "S":
        marge = t["W"] - 4.2
        bascule = [noms[c] for c in ("C", "Ch", "R", "Se", "Sn") if m.POIDS[c] / 100 > marge]
        A(f"- {t['id']} : marge {marge:.2f} ; une note de moins sur {', '.join(bascule) if bascule else 'aucun critere seul'} le fait passer en A.")
A("")

# --- Cellules estimees -------------------------------------------------------------------
A("### Cellules revenu sans source directe (estimees)\n")
A(", ".join(t["id"] for t in T if codes(t["src"]) == "est."))
A("")
A("### Cellules revenu sourcees mais ajustees (anciennete, conversion net, proxy)\n")
A(", ".join(t["id"] for t in T if codes(t["src"]).endswith("est.") and codes(t["src"]) != "est."))
A("")

texte = fr("\n".join(out) + "\n")
texte = re.sub(r"(?<=\d)\.(?=\d)", ",", texte)  # decimales a la francaise
texte = texte.replace(" x ", " × ")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tableaux.md"), "w", encoding="utf-8") as f:
    f.write(texte)
print("ok", len(FIN), "finaux")
