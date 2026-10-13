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
import modele as _m
n_elim = sum(1 for t in _m.T if t["domine_par"])
n_fin = len(_m.T) - n_elim
parties += ["## 3. Élimination", "", f"Règle : section 1.5. {n_elim} retraits ; un triplet dominé seulement sans IA est conservé.", "",
            sec("Éliminés")[1], ""]
parties += [f"## 4. Tableau final ({n_fin} triplets non dominés, triés par score interne décroissant)", "",
            "Notes : nom. = euros nominaux au change 2025 ; PPA = euros au niveau de prix français ; est. = valeur ajustée ou estimée ; * = à moins de 0,1 d'une frontière de palier.", ""]
for prefixe in ("Tableau final, partie A", "Tableau final, partie B"):
    titre, corps = sec(prefixe)
    parties += ["### " + titre, "", corps, ""]
parties += ["## 5. Frontière de Pareto", "", sec("Frontière de Pareto")[1], ""]
for prefixe in ("À moins de 0,1", "Égalités", "Sensibilité", "Marge"):
    titre, corps = sec(prefixe)
    parties += ["### " + titre, "", corps, ""]
parties += [lire("conclusion.md").strip(), ""]
import choix_realiste  # ecrit choix_realiste.md
parties += [lire("choix_realiste.md").strip(), ""]

texte = "\n".join(parties)
interdits = [c for c in texte if c in "‐‑‒–—―−"]
assert not interdits, "tiret interdit"
with open(os.path.join(ICI, "rapport.md"), "w", encoding="utf-8") as f:
    f.write(texte)
print("rapport.md :", len(texte), "caracteres")
