# -*- coding: utf-8 -*-
"""Extrait les 111 familles de l'etude Apec 2025 (Les remunerations des cadres dans 111 familles de metiers) :
nom, 1er decile, mediane et 9e decile (k EUR bruts annuels, fixe et variable), liste des metiers.

Source : https://corporate.apec.fr/files/live/sites/corporate/files/Nos%20etudes/PDF/Les%20remunerations%20des%20cadres%20dans%20111%20familles%20de%20metiers%202025.pdf
Usage : pdftotext -layout etude.pdf apec.txt ; python apec_parse.py apec.txt apec_111_familles_2025.json
"""
import json
import re
import sys

txt = open(sys.argv[1], encoding="latin-1").read()
out = []
for bloc in re.split(r"\n\s+(?=LES M.TIERS )", txt)[1:]:
    m = re.search(r"(\d+)\s*k\s+(\d+)\s*k\s+(\d+)\s*k", bloc)
    liste = re.search(r"Liste des m.tiers correspondants[^\n]*\n(.*?)(?:\n\s*\d+ -- |\Z)", bloc, re.S)
    metiers = [x.strip(" \x95•\t") for x in (liste.group(1).splitlines() if liste else []) if x.strip()]
    out.append(dict(nom=bloc.splitlines()[0].strip(), d1=int(m.group(1)) if m else None,
                    med=int(m.group(2)) if m else None, d9=int(m.group(3)) if m else None, metiers=metiers))
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "familles")
