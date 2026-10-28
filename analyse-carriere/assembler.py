# -*- coding: utf-8 -*-
"""Assemble rapport.md a partir de entete.md, tableaux.md (genere) et conclusion.md (version 5)."""
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


import modele as _m  # noqa: E402

parties = [lire("entete.md").strip(), ""]
parties += ["## 2. Pool (" + sec("Pool")[0].split("(")[1], "", sec("Pool")[1], ""]
parties += [f"## 3. Classement v5 ({len(_m.T)} triplets, grille Eurofound à poids égaux)", "",
            "Lecture des colonnes : EP environnement physique, IT intensité du travail, QT qualité du temps de travail, ES environnement social, "
            "CA compétences et autonomie, PS perspectives et sécurité, RE revenu ; notes de 1 (mauvais) à 5 (bon), poids égaux. "
            "CA et RE sont des notes continues (moyenne ou échelle logarithmique), les autres sont entières. "
            "Palier : S ≥ 4,2, A ≥ 3,6, B ≥ 3,0, C en dessous ; * = à moins de 0,1 d'une frontière. "
            "« 7= » : rang partagé (écart inférieur à 0,03). "
            "« X / Y k€ » : revenu net annuel en milliers d'euros, X au change 2025 sans ajustement, Y en parité de pouvoir d'achat ; le score utilise Y en équivalent temps plein.", ""]
for prefixe in ("Classement v5, partie A", "Classement v5, partie B", "Classement v5, partie C :",
                "Classement v5, partie C2", "Notes modifiées", "Classement v5, partie D"):
    titre, corps = sec(prefixe)
    parties += ["### " + titre, "", corps, ""]
parties += ["## 4. Robustesse aux pondérations", ""]
for prefixe in ("Robustesse", "Noyau robuste", "Sensibilité aux notes"):
    titre, corps = sec(prefixe)
    parties += ["### " + titre, "", corps, ""]
parties += ["## 5. Égalités et frontières de palier", ""]
for prefixe in ("Égalités", "À moins de 0,1"):
    titre, corps = sec(prefixe)
    parties += ["### " + titre, "", corps, ""]
titre, corps = sec("Conversion des notes")
parties += ["## 6. " + titre, "", corps, ""]
titre, corps = sec("Modifications de rang")
parties += ["## 7. " + titre, "", corps, ""]
titre, corps = sec("Cellules revenu sans source fiable")
parties += ["## 8. " + titre, "", corps, ""]
parties += [lire("conclusion.md").strip(), ""]

texte = "\n".join(parties)
interdits = [c for c in texte if c in "‐‑‒–—―−"]
assert not interdits, "tiret interdit"
with open(os.path.join(ICI, "rapport.md"), "w", encoding="utf-8") as f:
    f.write(texte)
print("rapport.md :", len(texte), "caracteres")
