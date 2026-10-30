# -*- coding: utf-8 -*-
"""Version 8.1 : variantes et notes de la v8, revenu net apres impot, deux classements separes.

Regles (declarees avant calcul, sans nouvelle recherche) :
- revenu : cellule v8 nette de cotisations, moins l'impot sur le revenu d'un celibataire sans enfant,
  baremes et approximations de la v7 (fiscalite_v7.py, section 1.15) : France, bareme 2025 (salarie :
  net x 1,035 moins 10 % de frais ; independant : benefice = net / 0,96) ; Suisse, impot a la source
  genevois bareme A0 en % du brut (salarie : brut = cellule / 0,80 ; independant : cellule plus prime
  LAMal), applique aussi aux residents ; meme regle pour la mediane et le P80 ; puis EQTP et PPA ;
- classement France : variantes France seulement (salarie, independant), sans frontalier ;
- classement Suisse : variantes de residents en Suisse seulement (salarie, independant) ;
- chaque classement a ses propres bornes de l'echelle de revenu (regle v7.1 : les variantes du
  classement) et ses propres tirages (variante A, 10 000 tirages, graine 20261029) ;
- signal : variante suisse dont le revenu vient d'un groupe CITP a 2 chiffres de l'ESS (et non d'une
  cellule propre au metier).
Usage : python modele_v8_1.py (ecrit resultats_v8_1.json a cote du script).
"""
import copy
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.dirname(ICI))
import fiscalite_v7 as F  # noqa: E402
import modele_v8 as M  # noqa: E402


def apres_impot(v, x):
    if v["resid"] == "FR":
        return F.apres_impot_fr(x, v["kind"] == "FR-ind")
    return F.apres_impot_ch(x, v["kind"] == "CH-ind")


def preparer(v):
    w = copy.deepcopy(v)
    r = w["rev"]
    f = M.PPA[w["resid"]]
    r["med_ai"], r["p80_ai"] = apres_impot(w, r["med"]), apres_impot(w, r["p80"])
    r["taux_impot"] = 1 - r["med_ai"] / r["med"]
    r["med_ai_ppa"], r["p80_ai_ppa"] = r["med_ai"] * f, r["p80_ai"] * f
    w["citp2"] = w["resid"] != "FR" and r["fiab"] == "officielle, groupe CITP"
    return w


CLASSEMENTS = {
    "France": [preparer(v) for v in M.V if v["resid"] == "FR"],
    "Suisse": [preparer(v) for v in M.V if v["resid"] == "CH"],
}

out = {}
for nom, V in CLASSEMENTS.items():
    R, bornes = M.classer(V, "med_ai_ppa", "p80_ai_ppa")
    M.tirages(R)
    out[nom] = dict(bornes=bornes, n_variantes=len(V), n_metiers=len(R), classement=R)
    print(f"== {nom} : {len(V)} variantes, {len(R)} métiers, bornes médiane {[round(x) for x in bornes['med']]}, "
          f"P80 {[round(x) for x in bornes['p80']]}, max P(1er) {max(v['p_1'] for v in R):.3f}")
    if nom == "Suisse":
        print("   métiers dont le revenu suisse vient d'un groupe CITP à 2 chiffres :",
              sum(v["citp2"] for v in R), "sur", len(R))
    for i, v in enumerate(sorted(R, key=lambda v: (-v["p_top"], -v["W"]))[:22], 1):
        r, n = v["rev"], v["notes"]
        print(f"{i:2} {v['metier']:7} {v['nom'][:60]:60} {v['kind']:6} W={v['W']:.3f} rang={v['rang_base']:3} "
              f"P10={v['p_top']:.3f} P1={v['p_1']:.3f} | EP{n['EP']} IT{n['IT']} QT{n['QT']} ES{n['ES']} CA{n['CA']:.2f} "
              f"PS{n['PS']} RE{v['RE']:.2f} | ai {r['med_ai']:,.0f} {r['cur']} (impôt {100 * r['taux_impot']:.1f} %)"
              f"{' CITP2' if v['citp2'] else ''}".replace(",", " "))

json.dump(out, open(os.path.join(ICI, "resultats_v8_1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1,
          default=float)
