# -*- coding: utf-8 -*-
"""Assemble rapport.md a partir de entete.md, tableaux.md (genere) et conclusion.md."""
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(ICI, "tableaux.py")], check=True, cwd=ICI)


def lire(nom):
    with open(os.path.join(ICI, nom), encoding="utf-8") as f:
        return f.read()


tab = lire("tableaux.md")
sections = {}
for bloc in re.split(r"(?m)^### ", tab)[1:]:
    titre, _, corps = bloc.partition("\n")
    sections[titre.strip()] = corps.strip()


def sec(prefixe):
    for titre, corps in sections.items():
        if titre.startswith(prefixe):
            return titre, corps
    raise KeyError(prefixe)


parties = [lire("entete.md").strip(), ""]
parties += ["## 2. Pool (" + sec("Pool")[0].split("(")[1], "", sec("Pool")[1], ""]
parties += ["## 3. Élimination", "", "Règle : section 1.5. Douze retraits ; un triplet dominé seulement sans IA est conservé.", "",
            sec("Éliminés")[1], ""]
parties += ["## 4. Tableau final (67 triplets non dominés, triés par score interne décroissant)", "",
            "Notes : nom. = euros nominaux au change 2025 ; PPA = euros au niveau de prix français ; est. = valeur ajustée ou estimée ; * = à moins de 0,1 d'une frontière de palier.", ""]
for prefixe in ("Tableau final, partie A", "Tableau final, partie B"):
    titre, corps = sec(prefixe)
    parties += ["### " + titre, "", corps, ""]
parties += ["## 5. Frontière de Pareto", "", sec("Frontière de Pareto")[1], ""]
for prefixe in ("À moins de 0,1", "Égalités", "Sensibilité", "Marge"):
    titre, corps = sec(prefixe)
    parties += ["### " + titre, "", corps, ""]
parties += [lire("conclusion.md").strip(), ""]

texte = "\n".join(parties)
interdits = [c for c in texte if c in "‐‑‒–—―−"]
assert not interdits, "tiret interdit"
with open(os.path.join(ICI, "rapport.md"), "w", encoding="utf-8") as f:
    f.write(texte)
print("rapport.md :", len(texte), "caracteres")
