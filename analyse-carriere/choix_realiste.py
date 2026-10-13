# -*- coding: utf-8 -*-
"""Classement en deux temps demande le 13 octobre 2026 :
1. garder les triplets ou l'on vit bien une fois dedans (palier S ou A, modele v3 depuis le 13 octobre) ;
2. les classer par meilleur pari realiste (esperance de bien-etre avec les vraies chances).

Hypotheses declarees avant calcul :
- Esperance = moyenne, sur l'horizon (24 a 45 ans par defaut), du score de bien-etre annuel.
- Avant l'entree dans le metier : score de l'emploi actuel (T75).
- Reussite avec la probabilite p estimee du modele.
- Echec connu a un age qui depend de la voie (AGE_ECHEC), puis 1 an de reconversion,
  puis plan B = electricien salarie (T47), meilleur metier accessible en moins d'un an avec p >= 80 %.
- Egalite declaree si l'ecart d'esperance est inferieur a 0,01.
"""
import modele as m

T = {t["id"]: t for t in m.T}
BASE = T["T75"]["W"]

# Age auquel l'echec de la selection est connu (fin de l'annee indiquee).
AGE_ECHEC_DEFAUT = 26  # Parcoursup ou licence sante (2 chances), alternance, concours de niveau bac
AGE_ECHEC = {i: 28 for i in ("T20", "T46", "T56", "T57", "T60", "T61", "T64")}  # licence puis concours ou master
AGE_ECHEC.update({"T67": 29, "T71": 29, "T19": 27, "T74": 27})


def esperance(t, horizon=45, plan_b="T47"):
    fb = T[plan_b]
    if t["id"] in (plan_b, "T75"):
        return sum(BASE if a < t["E"] else t["W"] for a in range(24, horizon + 1)) / (horizon - 23)
    echec = min(t["E"] - 1, AGE_ECHEC.get(t["id"], AGE_ECHEC_DEFAUT))
    reussite = sum(BASE if a < t["E"] else t["W"] for a in range(24, horizon + 1))
    rate = sum(BASE if a <= echec + 1 else fb["W"] for a in range(24, horizon + 1))
    return (t["p"] * reussite + (1 - t["p"]) * rate) / (horizon - 23)


finaux = [t for t in m.T if not t["domine_par"]]
shortlist = [t for t in finaux if t["palier"] in ("S", "A")]
for t in shortlist:
    t["EV45"] = esperance(t)
    t["EV64"] = esperance(t, horizon=64)
    t["EV45_base"] = esperance(t, plan_b="T75")
classes = sorted(shortlist, key=lambda t: -t["EV45"])

if __name__ == "__main__":
    r64 = {t["id"]: i for i, t in enumerate(sorted(shortlist, key=lambda t: -t["EV64"]), 1)}
    rb = {t["id"]: i for i, t in enumerate(sorted(shortlist, key=lambda t: -t["EV45_base"]), 1)}
    print(f"Shortlist S ou A : {len(shortlist)} triplets")
    for i, t in enumerate(classes, 1):
        print(i, t["id"], t["metier"], "|", t["statut"], "|", t["pays"], "|", t["palier"],
              "| EV45", round(t["EV45"], 3), "| rang 24-64:", r64[t["id"]], "| rang plan B emploi actuel:", rb[t["id"]],
              "| p", t["p"], "| E", t["E"], "| m40", round(t["m40_ppa"] / 1000))


def ecrire_section(chemin="choix_realiste.md"):
    import os
    import re
    import tableaux as tb
    r64 = {t["id"]: i for i, t in enumerate(sorted(shortlist, key=lambda t: -t["EV64"]), 1)}
    rb = {t["id"]: i for i, t in enumerate(sorted(shortlist, key=lambda t: -t["EV45_base"]), 1)}
    L = ["## 10. Classement en deux temps (13 octobre 2026)", "",
         "Demande : d'abord les métiers où l'on vit bien une fois dedans (palier S ou A), puis, parmi eux, le meilleur pari réaliste. Aucun filtre de domaine.", "",
         "Hypothèses déclarées avant calcul : espérance du score de bien-être annuel de 24 à 45 ans ; avant l'entrée, score de l'emploi actuel (T75) ; réussite avec la probabilité p du modèle ; en cas d'échec, connu à 26 ans (28 ou 29 ans pour les voies licence puis concours), 1 an de reconversion puis plan B = électricien salarié (T47) ; égalité si l'écart est inférieur à 0,01. Variantes : horizon 24 à 64 ans ; plan B = emploi actuel.", "",
         "Limite : pour une variante à l'étranger (frontalier, résident en Suisse, États-Unis, Irlande), un échec à la dernière étape (permis, visa, équivalence) laisse en réalité la version française du métier, pas le plan B ; l'espérance de ces variantes est donc sous-estimée.", "",
         "| Rang | ID | Triplet | Palier une fois dedans | Chances p | Entrée | Médian 40 ans PPA k€ | Rang 24-64 ans | Rang si plan B = emploi actuel |",
         "|---|---|---|---|---|---|---|---|---|"]
    for i, t in enumerate(classes, 1):
        L.append(f"| {i} | {t['id']} | {tb.tri(t)} | {t['palier']} | {t['p'] * 100:.0f} % | {t['E']} | {t['m40_ppa'] / 1000:.0f} | {r64[t['id']]} | {rb[t['id']]} |")
    L.append("")
    s = tb.fr("\n".join(L))
    s = re.sub(r"(?<=\d)\.(?=\d)", ",", s).replace(" x ", " × ")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), chemin), "w", encoding="utf-8") as f:
        f.write(s)


ecrire_section()
