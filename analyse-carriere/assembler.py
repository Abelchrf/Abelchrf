# -*- coding: utf-8 -*-
"""Assemble rapport.md a partir de entete.md, tableaux.md (genere) et conclusion.md (version 4)."""
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
parties += [f"## 3. Classement v4 ({len(_m.T)} triplets, qualité de vie une fois installé)", "",
            "Lecture des colonnes : C contrôle, Ch charge, R relations, Se sécurité, Sn sens, L lieu (télétravail), notes entières de 1 à 5 ; "
            "Rev = note de revenu de 1 à 5, seule note continue, calculée sur les valeurs ajustées en PPA ; poids entre parenthèses. "
            "Palier : S ≥ 4,2, A ≥ 3,6, B ≥ 3,0, C en dessous ; * = à moins de 0,1 d'une frontière. "
            "« 7= » : rang partagé par des triplets à égalité (écart inférieur à 0,03). "
            "« X / Y k€ » : revenu net annuel en milliers d'euros, X au change 2025 sans ajustement, Y en parité de pouvoir d'achat (euros au niveau de prix français) ; le score utilise Y.", ""]
for prefixe in ("Classement v4, partie A", "Classement v4, partie B", "Classement v4, partie C"):
    titre, corps = sec(prefixe)
    parties += ["### " + titre, "", corps, ""]
parties += ["## 4. Égalités, frontières de palier, sensibilité aux poids", ""]
for prefixe in ("Égalités", "À moins de 0,1", "Sensibilité"):
    titre, corps = sec(prefixe)
    parties += ["### " + titre, "", corps, ""]
titre, corps = sec("Pourquoi T89")
parties += ["## 5. " + titre, "",
            "Le contrôle a le plus gros poids (22 sur 100), mais le score est une moyenne pondérée, pas un ordre strict : "
            "une note de contrôle en moins coûte 0,22, et une note de plus en relations et en sécurité rapporte 0,30. "
            "Un salarié peut donc passer devant un indépendant mieux noté en contrôle s'il le dépasse ailleurs. "
            "Si tu veux que le contrôle départage avant tout le reste, c'est un autre mode de calcul (ordre lexicographique), à décider explicitement.", "",
            corps, ""]
titre, corps = sec("Modifications de rang")
parties += ["## 6. " + titre, "", corps, ""]
parties += [lire("conclusion.md").strip(), ""]

texte = "\n".join(parties)
interdits = [c for c in texte if c in "‐‑‒–—―−"]
assert not interdits, "tiret interdit"
with open(os.path.join(ICI, "rapport.md"), "w", encoding="utf-8") as f:
    f.write(texte)
print("rapport.md :", len(texte), "caracteres")
