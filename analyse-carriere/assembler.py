# -*- coding: utf-8 -*-
"""Assemble rapport.md (version 7) a partir de entete.md, tableaux_v7.md (genere) et conclusion_v7.md.

La version 6 du rapport est archivee dans rapport_v6.md ; ses sources S01 a S166 sont reprises de
conclusion.md (section « 11. Sources »).
"""
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(ICI, "tableaux_v7.py")], check=True, cwd=ICI)


def lire(nom):
    with open(os.path.join(ICI, nom), encoding="utf-8") as f:
        return f.read()


tab = lire("tableaux_v7.md")
sections = {}
for bloc in re.split(r"(?m)^### ", tab)[1:]:
    titre, _, corps = bloc.partition("\n")
    sections[titre.strip()] = corps.strip()


def sec(prefixe):
    for titre, corps in sections.items():
        if titre.startswith(prefixe):
            return titre, corps
    raise KeyError(prefixe)


def bloc(prefixes, niveau="###"):
    out = []
    for p in prefixes:
        titre, corps = sec(p)
        out += [f"{niveau} {titre}", "", corps, ""]
    return out


import modele_v7 as _m1  # noqa: E402
import classement2_v7 as _m2  # noqa: E402

LECTURE = ("Lecture des colonnes : EP environnement physique, IT intensité du travail, QT qualité du temps de travail, ES environnement "
           "social, CA compétences et autonomie, PS perspectives et sécurité, RE revenu net après impôt ; notes de 1 (mauvais) à 5 (bon), "
           "poids égaux. CA et RE sont continues, les autres entières. Palier : S ≥ 4,2, A ≥ 3,6, B ≥ 3,0, C en dessous ; * = à moins "
           "de 0,1 d'une frontière. « 2= » : rang partagé (écart inférieur à 0,03). P(10 premiers) : part des 10 000 tirages de la "
           "variante A où le triplet est dans les 10 premiers.")
parties = [lire("entete.md").strip(), ""]
parties += ["## 2. Tri des pays (OCDE, Singapour, Émirats arabes unis)", ""] + bloc(["Tri des pays"])
parties += [f"## 3. Classement 1 : France et Suisse ({len(_m1.R1)} triplets, postes précis)", "", LECTURE, ""]
parties += bloc(["Classement 1, catalogue", "Classement 1, partie A", "Classement 1, partie B", "Classement 1, partie C",
                 "Classement 1, partie D", "Classement 1, partie E", "Classement 1, partie F", "Classement 1, partie G"])
parties += [f"## 4. Classement 2 : les 10 pays retenus ({len(_m2.R2)} triplets)", "", LECTURE, ""]
parties += bloc(["Classement 2, postes retenus", "Classement 2, revenus", "Classement 2, partie A", "Classement 2, partie B",
                 "Classement 2, partie C", "Classement 2, partie D", "Classement 2, partie E", "Classement 2, partie F",
                 "Classement 2, partie G", "Classement 2, partie H"])
parties += ["## 5. Vérification des barèmes fiscaux", ""] + bloc(["Vérification des barèmes"])
parties += ["## 6. Cellules signalées", ""] + bloc(["Cellules revenu signalées"])
groupes = "\n".join(bloc(["Classement 1, groupe de tête", "Classement 1, deux scénarios IA", "Classement 2, groupe de tête",
                          "Classement 2, deux scénarios IA"], niveau="####"))
v6 = lire("conclusion.md")
sources_v6 = v6.split("## 11. Sources", 1)[1].strip().split("\n")[2:]
conclusion = lire("conclusion_v7.md").replace("{GROUPES}", groupes).replace("{SOURCES_V6}", "\n".join(sources_v6))
parties += [conclusion.strip(), ""]

texte = "\n".join(parties)
interdits = [c for c in texte if c in "‐‑‒–—―−"]
assert not interdits, f"tiret interdit : {set(interdits)}"
cites = set(re.findall(r"S(\d{2,3})\b", texte))
listes = set(re.findall(r"(?m)^\| S(\d{2,3}) \|", texte))
manquants = sorted(c for c in cites if c not in listes and int(c) <= 200)
assert not manquants, f"sources citées absentes de la liste : {manquants}"
with open(os.path.join(ICI, "rapport.md"), "w", encoding="utf-8") as f:
    f.write(texte)
print("rapport.md :", len(texte), "caracteres ;", len(listes), "sources listées")
