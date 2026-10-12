# -*- coding: utf-8 -*-
"""Classement de triplets metier x statut x pays pour le sujet de reference.

Toutes les entrees sont declarees dans ce fichier. Tout changement de resultat
doit etre tracable a une modification d'une entree ci-dessous.

Usage : python3 modele.py  (ecrit resultats.md et resultats.json a cote du script)
"""
import json
import math
import os

# ---------------------------------------------------------------------------
# 1. Poids des criteres (opinion fondee sur la litterature, pas un consensus)
# ---------------------------------------------------------------------------
# Version 2 (12 octobre 2026). Changements declares par rapport a la version 1 :
# - Sens 13 -> 7 : au niveau d'un triplet, seule l'utilite de la tache est previsible ; l'adhesion a la
#   mission depend de l'employeur. Les 6 points sont redistribues au prorata des autres poids.
# - Controle : retrait du malus "affectation geographique imposee" (hors definition : temps et methode).
# - Sens : moins 1 pour les soignants hospitaliers salaries ou la DARES documente des conflits de valeurs
#   frequents (aides-soignants, infirmiers, sages-femmes ; S58).
POIDS_V1 = {"C": 22, "Ch": 20, "R": 15, "Se": 15, "Sn": 13, "Rev": 15}
POIDS = {"C": 24, "Ch": 21, "R": 16, "Se": 16, "Sn": 7, "Rev": 16}
SEUILS = [("S", 4.2), ("A", 3.6), ("B", 3.0)]  # en dessous : C

# ---------------------------------------------------------------------------
# 2. Prix et change
# ---------------------------------------------------------------------------
# Indices de niveau de prix Eurostat 2024, consommation finale des menages, UE27=100.
# CA : estime a partir du ratio OCDE (niveaux de prix PIB 2024 : Canada 105, France 95).
PLI = {"FR": 111, "DE": 109, "LU": 133, "CH": 174, "CA": round(111 * 105 / 95)}
# Taux de change moyens 2024 (BCE), unites de devise pour 1 euro, coherents avec les PLI 2024.
XR2024 = {"EUR": 1.0, "CHF": 0.9526, "CAD": 1.4821}
# Taux de change aout-decembre 2025 (Banque de France, reference BCE) pour la valeur non ajustee.
XR2025 = {"EUR": 1.0, "CHF": 0.933, "CAD": 1.619}
# Surcout regional estime pour les frontaliers residant en France (pas de serie officielle).
PRIME_REGION = {"FR-GE": 0.10, "FR-LO": 0.05}


def facteur_nominal(cur):
    """Euros nominaux pour 1 unite de devise locale (change 2025)."""
    return 1.0 / XR2025[cur]


def facteur_ppa(cur, resid):
    """Euros 'niveau de prix France' pour 1 unite de devise locale."""
    if resid in PRIME_REGION:  # frontalier : depense en France au change courant
        return facteur_nominal(cur) / (1.0 + PRIME_REGION[resid])
    return PLI["FR"] / (PLI[resid] * XR2024[cur])


# ---------------------------------------------------------------------------
# 3. Trajectoire de reference (emploi immediat peu qualifie)
# ---------------------------------------------------------------------------
def base(age):
    """Revenu net annuel de reference (EUR, France) : SMIC 2026 vers mediane employes."""
    if age <= 40:
        return 18000 + (21000 - 18000) * (age - 24) / 16
    return 21000 * 1.005 ** (age - 40)


CROISSANCE_APRES_40 = 0.005
AGES = range(24, 46)  # 24 a 45 inclus = 22 annees

# ---------------------------------------------------------------------------
# 4. Pool de triplets
# ---------------------------------------------------------------------------
# Champs : id, metier, statut, pays, cur, resid, E (age d'entree), start, m40, p80
# (revenus nets annuels en devise locale, apres cotisations, avant impot),
# pre (phases avant E : (age_debut, age_fin, revenu, cur, resid)),
# notes C, Ch, R, Se, Sn, p (probabilite de reussite), cap (1-5), ia (faible/moyenne/elevee),
# src (source du median a 40 ans), fin (formation et financement), sel (selectivite).
MED_PRE = [(25, 27, 0), (28, 28, 3100), (29, 29, 3800), (30, 30, 4700),
           (31, 31, 24000), (32, 32, 25000), (33, 33, 26000), (34, 34, 34000)]
SPE_PRE = MED_PRE[:-1] + [(34, 34, 27000), (35, 35, 34000), (36, 37, 40000)]
IFSI_PRE = [(25, 27, 1200)]
ALT2 = [(25, 25, 11000), (26, 26, 17300)]  # BTS en apprentissage : 53 % puis 100 % du SMIC

T = []


def add(**kw):
    kw.setdefault("cur", "EUR")
    kw.setdefault("resid", "FR")
    kw.setdefault("pre", [])
    T.append(kw)


# --- Sante, France -----------------------------------------------------------
add(id="T01", metier="Medecin generaliste", statut="liberal", pays="France",
    E=35, start=60000, m40=76000, p80=100000, pre=MED_PRE,
    C=4, Ch=3, R=4, Se=5, Sn=5, p=0.10, cap=2, ia="faible",
    src="S02 (DREES 2021 : omnipraticiens 98 300 EUR moy.) + S05 (UNASA BNC 2022 : 90 141 EUR) ; estime : mediane a 5 ans d'installation = 0,82 x moyenne, x 0,94 (CSG/CRDS)",
    fin="Licence portail sante (rentree 2027) puis 9 ans ; internat remunere ; bourses", sel="2 candidatures ; PASS 2024 : 33,8 % admis en 1 an ; p estime 10 %")
add(id="T02", metier="Medecin generaliste", statut="salarie (centre de sante)", pays="France",
    E=35, start=58000, m40=64000, p80=76000, pre=MED_PRE,
    C=3, Ch=4, R=4, Se=5, Sn=5, p=0.10, cap=2, ia="faible",
    src="estime : pas de serie officielle ; ancrage S09 (INSEE FPH 2024 : personnels medicaux 6 926 EUR/mois moy.)",
    fin="Idem T01", sel="p estime 10 %")
add(id="T03", metier="Medecin specialiste (rang median)", statut="liberal", pays="France",
    E=38, start=75000, m40=82000, p80=130000, pre=SPE_PRE,
    C=4, Ch=3, R=4, Se=5, Sn=5, p=0.09, cap=2, ia="faible",
    src="S02 (DREES 2021 : pediatres 88 400 EUR, autres specialistes 153 300 EUR) ; estime specialite accessible au rang median, debut d'exercice",
    fin="Idem T01 + internat 5 ans + clinicat 2 ans", sel="Specialite selon rang EDN ; p estime 9 %")
add(id="T04", metier="Praticien hospitalier", statut="statut PH (public)", pays="France",
    E=38, start=62000, m40=68000, p80=82000, pre=SPE_PRE,
    C=3, Ch=2, R=3, Se=5, Sn=5, p=0.09, cap=2, ia="faible",
    src="S09 (INSEE FPH 2024 : personnels medicaux 6 926 EUR/mois moy. tous ages) ; estime debut de carriere PH",
    fin="Idem T03", sel="p estime 9 %")
add(id="T05", metier="Chirurgien-dentiste", statut="liberal", pays="France",
    E=31, start=55000, m40=92000, p80=127000, pre=[(25, 27, 0), (28, 30, 2000)],
    C=5, Ch=3, R=4, Se=5, Sn=5, p=0.05, cap=3, ia="faible",
    src="S04 (CARCDSF 2023 : mediane 97 672 EUR) + S03 (DREES 2021 : 118 100 EUR moy.) ; x 0,94",
    fin="Licence portail sante + 5 ans ; pret d'installation apres collaboration", sel="Places d'odontologie rares ; p estime 5 %")
add(id="T06", metier="Pharmacien adjoint", statut="salarie", pays="France",
    E=31, start=35000, m40=40000, p80=48000, pre=[(25, 29, 0), (30, 30, 3000)],
    C=2, Ch=2, R=3, Se=5, Sn=4, p=0.25, cap=2, ia="faible",
    src="estime : grille de la convention collective officine (non recuperee) ; aucune serie officielle",
    fin="Licence portail sante + 5 ans", sel="Places de pharmacie souvent non pourvues ; p estime 25 %")
add(id="T07", metier="Pharmacien titulaire", statut="independant", pays="France",
    E=35, start=50000, m40=56000, p80=85000,
    pre=[(25, 29, 0), (30, 30, 3000), (31, 31, 35000), (32, 32, 36000), (33, 33, 37000), (34, 34, 38000)],
    C=3, Ch=2, R=3, Se=3, Sn=4, p=0.12, cap=5, ia="faible",
    src="S01 (INSEE 2024 : commerce pharmaceutique 6 390 EUR/mois moy.) ; estime nouvel acquereur endette",
    fin="Idem T06 + rachat d'officine (pret, apport)", sel="p estime 12 % (financement sans capital)")
add(id="T08", metier="Sage-femme", statut="fonctionnaire FPH", pays="France",
    E=31, start=30000, m40=39600, p80=45000, pre=[(25, 27, 0), (28, 30, 1500)],
    C=3, Ch=3, R=3, Se=5, Sn=4, p=0.18, cap=2, ia="faible",
    src="S10 (DREES : sages-femmes hospitalieres 3 442 EUR/mois moy.)",
    fin="Licence portail sante + 5 ans (maieutique en 6 ans)", sel="p estime 18 %")
add(id="T09", metier="Sage-femme", statut="liberal", pays="France",
    E=31, start=32000, m40=40000, p80=55000, pre=[(25, 27, 0), (28, 30, 1500)],
    C=5, Ch=4, R=4, Se=5, Sn=5, p=0.16, cap=2, ia="faible",
    src="S03 (DREES 2021 : sages-femmes liberales 42 200 EUR moy., +6,3 %/an) x 0,94",
    fin="Licence portail sante + 5 ans (maieutique en 6 ans)", sel="p estime 16 %")
add(id="T10", metier="Masseur-kinesitherapeute", statut="liberal", pays="France",
    E=30, start=30000, m40=45000, p80=60000, pre=[(25, 29, 0)],
    C=5, Ch=3, R=4, Se=5, Sn=5, p=0.07, cap=3, ia="faible",
    src="S03 (DREES 2021 : 51 100 EUR moy.) + S06 (UNASA titulaires mediane 31 356 EUR) ; estime",
    fin="Licence portail sante ou STAPS acces kine + IFMK 4 ans ; IFMK prives 5-9 kEUR/an", sel="Tres selectif ; p estime 7 %")
add(id="T11", metier="Masseur-kinesitherapeute", statut="fonctionnaire FPH", pays="France",
    E=30, start=25000, m40=30000, p80=34000, pre=[(25, 29, 0)],
    C=3, Ch=4, R=4, Se=5, Sn=5, p=0.07, cap=3, ia="faible",
    src="estime : grille reeducateurs FPH ; ancrage S09",
    fin="Idem T10", sel="p estime 7 %")
add(id="T12", metier="Infirmier", statut="fonctionnaire FPH", pays="France",
    E=28, start=27000, m40=34800, p80=39600, pre=IFSI_PRE,
    C=2, Ch=2, R=3, Se=5, Sn=4, p=0.25, cap=2, ia="faible",
    src="S10 (DREES 2023 : infirmiers hopital public 2 872 EUR/mois moy.) + S09",
    fin="IFSI 3 ans (Parcoursup, ou voie FPC avec 3 ans de cotisations ; Transition Pro possible)", sel="2025 : 116 000 candidats pour 25 000 places ; p estime 25 %")
add(id="T13", metier="Infirmier", statut="liberal", pays="France",
    E=30, start=40000, m40=50000, p80=66000, pre=IFSI_PRE + [(28, 28, 27000), (29, 29, 28000)],
    C=4, Ch=2, R=4, Se=5, Sn=5, p=0.22, cap=2, ia="faible",
    src="S03 (DREES 2021 : infirmiers liberaux 57 100 EUR moy.) x 0,94 x 0,93",
    fin="IFSI + 24 mois d'exercice salarie avant installation", sel="p estime 22 %")
add(id="T14", metier="Infirmier anesthesiste (IADE)", statut="fonctionnaire FPH", pays="France",
    E=32, start=36000, m40=42000, p80=48000,
    pre=IFSI_PRE + [(28, 28, 27000), (29, 29, 28000), (30, 31, 29000)],
    C=3, Ch=3, R=3, Se=5, Sn=4, p=0.09, cap=2, ia="faible",
    src="estime : grille IADE FPH ; ancrage S09",
    fin="IFSI + 2 ans d'exercice + concours + 2 ans (promotion professionnelle remuneree)", sel="p estime 9 %")
add(id="T15", metier="Orthophoniste", statut="liberal", pays="France",
    E=30, start=24000, m40=31000, p80=42000, pre=[(25, 29, 0)],
    C=5, Ch=5, R=4, Se=5, Sn=5, p=0.03, cap=2, ia="faible",
    src="S06 (UNASA 2022 : 27 550 EUR moy., temps partiel inclus) ; estime temps plein",
    fin="CFUO 5 ans (grade master)", sel="2025 : 3,29 % d'admis ; p estime 3 %")
add(id="T16", metier="Orthoptiste", statut="salarie", pays="France",
    E=28, start=24000, m40=31200, p80=36000, pre=[(25, 27, 0)],
    C=3, Ch=4, R=4, Se=5, Sn=4, p=0.10, cap=2, ia="moyenne",
    src="estime : aucune serie officielle recuperee",
    fin="Certificat de capacite 3 ans", sel="Selectif ; p estime 10 %")
add(id="T17", metier="Manipulateur radio (MERM)", statut="fonctionnaire FPH", pays="France",
    E=28, start=26000, m40=33600, p80=38000, pre=[(25, 27, 0)],
    C=2, Ch=4, R=3, Se=5, Sn=4, p=0.30, cap=2, ia="faible",
    src="estime : grille paramedicale cat. A FPH ; ancrage S09",
    fin="DE ou DTS 3 ans", sel="p estime 30 %")
add(id="T18", metier="Audioprothesiste", statut="salarie", pays="France",
    E=28, start=26000, m40=36000, p80=45000, pre=[(25, 27, 0)],
    C=3, Ch=4, R=4, Se=4, Sn=4, p=0.10, cap=2, ia="faible",
    src="S21 (APEC : offres 36 600 EUR brut moy. ; confirme 2 300-3 100 EUR net/mois)",
    fin="DE 3 ans", sel="Peu de places ; p estime 10 %")
add(id="T19", metier="Veterinaire", statut="liberal", pays="France",
    E=32, start=38000, m40=52000, p80=76000, pre=[(25, 31, 0)],
    C=4, Ch=2, R=3, Se=5, Sn=4, p=0.05, cap=2, ia="faible",
    src="S01 (INSEE 2024 : veterinaires 6 370 EUR/mois moy.) ; estime debut de carriere",
    fin="L2 ou BUT + concours (2 tentatives) + 5 ans ; ou ecole UE payante", sel="Voie post-bac reservee aux neo-bacheliers ; 46 a 58 places par voie ; p estime 5 %")
add(id="T20", metier="Psychologue", statut="contractuel FPH", pays="France",
    E=30, start=24000, m40=30000, p80=35000, pre=[(25, 29, 0)],
    C=4, Ch=4, R=4, Se=3, Sn=5, p=0.20, cap=2, ia="faible",
    src="estime : grille psychologues FPH ; aucune serie recuperee",
    fin="Licence + master selectif", sel="p estime 20 %")
add(id="T21", metier="Aide-soignant", statut="fonctionnaire FPH", pays="France",
    E=26, start=22000, m40=27000, p80=30000, pre=[(25, 25, 0)],
    C=1, Ch=2, R=3, Se=5, Sn=4, p=0.75, cap=1, ia="faible",
    src="S14 (grille AS FPH 2025, IM 372 a 558) + CTI ; S12 (point 4,92278 EUR)",
    fin="IFAS 1 an (apprentissage possible)", sel="p estime 75 %")
add(id="T22", metier="Osteopathe", statut="liberal", pays="France",
    E=30, start=18000, m40=32000, p80=45000, pre=[(25, 29, -8000)],
    C=5, Ch=4, R=4, Se=2, Sn=4, p=0.65, cap=4, ia="faible",
    src="estime : aucune serie officielle recuperee",
    fin="Ecole privee 5 ans, 7 a 10 kEUR/an (pret)", sel="Peu selectif ; marche sature ; p estime 65 %")

# --- Sante, etranger ---------------------------------------------------------
add(id="T23", metier="Infirmier", statut="salarie", pays="Suisse (resident)", cur="CHF", resid="CH",
    E=28, start=65600, m40=77600, p80=89600, pre=IFSI_PRE,
    C=2, Ch=2, R=3, Se=5, Sn=5, p=0.22, cap=2, ia="faible",
    src="S23 (OFS : mediane infirmiers 7 400 CHF/mois 13e inclus, 2018) x 1,074 (S22, ajustement estime) ; S64 (HUG 86 500 a 120 500 CHF/an) ; net = brut x 0,80",
    fin="IFSI + reconnaissance Croix-Rouge suisse (mois) + permis B", sel="p estime 22 %")
add(id="T24", metier="Infirmier", statut="salarie", pays="Suisse (frontalier)", cur="CHF", resid="FR-GE",
    E=28, start=65600, m40=77600, p80=89600, pre=IFSI_PRE,
    C=2, Ch=1, R=3, Se=5, Sn=5, p=0.22, cap=2, ia="faible",
    src="S23 (OFS : mediane infirmiers 7 400 CHF/mois 13e inclus, 2018) x 1,074 (S22, ajustement estime) ; S64 (HUG 86 500 a 120 500 CHF/an) ; net = brut x 0,80",
    fin="IFSI + reconnaissance + permis G", sel="p estime 22 %")
add(id="T25", metier="Infirmier", statut="salarie", pays="Luxembourg (frontalier)", cur="EUR", resid="FR-LO",
    E=28, start=61950, m40=75075, p80=91000, pre=IFSI_PRE,
    C=2, Ch=1, R=3, Se=5, Sn=5, p=0.22, cap=2, ia="faible",
    src="S29 (FHL CS7 : 227 a 443 points ; point 23,99 EUR en 2026) ; estime 6 600 EUR/mois x 13 a 12 ans ; net = brut x 0,875",
    fin="IFSI + autorisation d'exercer (diplome exempte de reconnaissance)", sel="p estime 22 %")
add(id="T26", metier="Infirmier", statut="salarie", pays="Luxembourg (resident)", cur="EUR", resid="LU",
    E=28, start=61950, m40=75075, p80=91000, pre=IFSI_PRE,
    C=2, Ch=2, R=3, Se=5, Sn=5, p=0.22, cap=2, ia="faible",
    src="S29 (FHL CS7 : 227 a 443 points ; point 23,99 EUR en 2026) ; estime 6 600 EUR/mois x 13 a 12 ans ; net = brut x 0,875",
    fin="IFSI + autorisation d'exercer (diplome exempte de reconnaissance)", sel="p estime 22 %")
add(id="T27", metier="Infirmier", statut="salarie", pays="Allemagne", cur="EUR", resid="DE",
    E=29, start=35100, m40=45240, p80=51480, pre=IFSI_PRE + [(28, 28, 27000)],
    C=2, Ch=2, R=2, Se=4, Sn=5, p=0.12, cap=2, ia="faible",
    src="S32 (Destatis avril 2024 : 4 310 EUR/mois brut) x 12,8 ; net = brut x 0,78",
    fin="IFSI + allemand B2 + Anerkennung", sel="p estime 12 %")
add(id="T28", metier="Infirmier", statut="salarie", pays="Canada (Quebec)", cur="CAD", resid="CA",
    E=29, start=59070, m40=80555, p80=93085, pre=IFSI_PRE + [(28, 28, 27000)],
    C=2, Ch=2, R=3, Se=4, Sn=5, p=0.18, cap=2, ia="faible",
    src="S35 (Guichet-Emplois QC : mediane 40 CAD/h, Q3 45 CAD/h) ; 45 CAD x 1 950 h x 0,918",
    fin="IFSI + ARM (stage d'adaptation 75 jours) + immigration", sel="p estime 18 %")
add(id="T29", metier="Medecin", statut="salarie (hopital)", pays="Suisse (resident)", cur="CHF", resid="CH",
    E=35, start=99600, m40=141100, p80=182600, pre=MED_PRE,
    C=3, Ch=2, R=3, Se=5, Sn=5, p=0.08, cap=2, ia="faible",
    src="S25 (OFSP/BASS : salaries 226 900 CHF moy. AVS, 2009-2014) ; estime 170 000 CHF brut x 0,83",
    fin="Medecine en France + autorisation MEBEKO", sel="p estime 8 %")
add(id="T30", metier="Medecin generaliste", statut="independant", pays="Suisse (resident)", cur="CHF", resid="CH",
    E=38, start=119000, m40=136000, p80=187000, pre=MED_PRE + [(35, 37, 99600, "CHF", "CH")],
    C=4, Ch=3, R=4, Se=5, Sn=5, p=0.07, cap=3, ia="faible",
    src="S24 (OFS 2019 : premier recours mediane 172 000 CHF) ; estime debut 160 000 CHF x 0,85",
    fin="Medecine en France + 3 ans en etablissement suisse (admission LAMal)", sel="p estime 7 %")
add(id="T31", metier="Medecin", statut="salarie (hopital)", pays="Allemagne", cur="EUR", resid="DE",
    E=35, start=85000, m40=102900, p80=119000, pre=MED_PRE,
    C=3, Ch=2, R=2, Se=5, Sn=5, p=0.06, cap=2, ia="faible",
    src="S34 (TV-Arzte VKA : A1 5 722 EUR ; Oberarzt 8 743 EUR) ; estime Facharzt + gardes 121 000 EUR brut",
    fin="Medecine en France + allemand C1 (Fachsprachprufung)", sel="p estime 6 %")
add(id="T32", metier="Medecin de famille", statut="liberal (RAMQ)", pays="Canada (Quebec)", cur="CAD", resid="CA",
    E=35, start=150000, m40=180000, p80=240000, pre=MED_PRE,
    C=3, Ch=2, R=3, Se=5, Sn=5, p=0.07, cap=2, ia="faible",
    src="estime : donnees RAMQ/ICIS non recuperees ; 180 000 CAD nets de frais",
    fin="Medecine en France (DES MG) + ARM + immigration", sel="p estime 7 %")
add(id="T33", metier="Aide-soignant (ASSC)", statut="salarie", pays="Suisse (frontalier)", cur="CHF", resid="FR-GE",
    E=26, start=49920, m40=57200, p80=62400, pre=[(25, 25, 0)],
    C=1, Ch=1, R=3, Se=4, Sn=5, p=0.55, cap=1, ia="faible",
    src="S22 (ESS 2024 : niveau de competence 2 = 5 866 CHF) ; estime 5 500 CHF x 13 x 0,80",
    fin="IFAS + reconnaissance Croix-Rouge suisse", sel="p estime 55 %")
add(id="T34", metier="Masseur-kinesitherapeute", statut="salarie", pays="Suisse (frontalier)", cur="CHF", resid="FR-GE",
    E=30, start=62400, m40=74880, p80=83200, pre=[(25, 29, 0)],
    C=3, Ch=3, R=4, Se=5, Sn=5, p=0.06, cap=3, ia="faible",
    src="S22 (ESS 2024 : niveau 3 = 7 523 CHF) ; estime 7 200 CHF x 13 x 0,80",
    fin="Kine en France + reconnaissance", sel="p estime 6 %")

# --- Numerique, ingenierie ---------------------------------------------------
add(id="T35", metier="Developpeur", statut="salarie", pays="France",
    E=27, start=30000, m40=40500, p80=50700, pre=ALT2,
    C=4, Ch=4, R=4, Se=3, Sn=3, p=0.45, cap=1, ia="elevee",
    src="S17 (APEC 2025 : IT 35-45 ans 49 a 101 kEUR) ; estime 52 000 EUR brut x 0,78",
    fin="BTS SIO ou BUT en alternance (remunere)", sel="Marche junior tendu 2024-2026 ; p estime 45 %")
add(id="T36", metier="Developpeur", statut="independant (freelance)", pays="France",
    E=32, start=45000, m40=58000, p80=76000,
    pre=ALT2 + [(27, 27, 30000), (28, 28, 31500), (29, 29, 33000), (30, 30, 34500), (31, 31, 36000)],
    C=5, Ch=4, R=3, Se=2, Sn=3, p=0.30, cap=1, ia="elevee",
    src="S19 (Malt : TJM 8-15 ans 576 EUR) x 170 jours x 0,59",
    fin="Idem T35 + 5 ans salarie", sel="p estime 30 %")
add(id="T37", metier="Developpeur", statut="salarie", pays="Suisse (frontalier)", cur="CHF", resid="FR-GE",
    E=30, start=76000, m40=91200, p80=108000, pre=ALT2 + [(27, 27, 30000), (28, 28, 31500), (29, 29, 33000)],
    C=4, Ch=3, R=4, Se=3, Sn=3, p=0.25, cap=2, ia="elevee",
    src="S26 (ESS 2024 TIC : 9 490 CHF/mois) x 12 x 0,80",
    fin="Idem T35 + 3 ans d'experience ; permis G", sel="p estime 25 %")
add(id="T38", metier="Developpeur", statut="salarie", pays="Allemagne", cur="EUR", resid="DE",
    E=28, start=37440, m40=56940, p80=70200, pre=ALT2 + [(27, 27, 30000)],
    C=4, Ch=4, R=3, Se=3, Sn=3, p=0.20, cap=2, ia="elevee",
    src="S33 (BA 2024 : IKT 6 114 EUR/mois) x 12 x 0,78",
    fin="Idem T35 + allemand", sel="p estime 20 %")
add(id="T39", metier="Developpeur", statut="salarie", pays="Luxembourg (frontalier)", cur="EUR", resid="FR-LO",
    E=29, start=48125, m40=65625, p80=83125, pre=ALT2 + [(27, 27, 30000), (28, 28, 31500)],
    C=4, Ch=3, R=4, Se=3, Sn=3, p=0.25, cap=2, ia="elevee",
    src="S30 (STATEC 2022 : mediane 58 126 EUR) ; estime TIC 75 000 EUR x 0,875",
    fin="Idem T35 + mobilite", sel="p estime 25 %")
add(id="T40", metier="Developpeur", statut="salarie", pays="Canada (Quebec)", cur="CAD", resid="CA",
    E=29, start=62650, m40=89505, p80=107406, pre=ALT2 + [(27, 27, 30000), (28, 28, 31500)],
    C=4, Ch=4, R=4, Se=3, Sn=3, p=0.25, cap=2, ia="elevee",
    src="S35 (QC : mediane 45,67 CAD/h) ; estime 50 CAD x 1 950 h x 0,918",
    fin="Idem T35 + immigration", sel="p estime 25 %")
ING_PRE = [(25, 25, 0), (26, 27, 17300), (28, 30, 18500)]
add(id="T41", metier="Ingenieur", statut="salarie", pays="France",
    E=31, start=35000, m40=45000, p80=56000, pre=ING_PRE,
    C=4, Ch=4, R=4, Se=4, Sn=3, p=0.30, cap=1, ia="moyenne",
    src="S16 (IESF 2025 : mediane 67 000 EUR brut tous ages) ; estime 10 ans d'experience 58 000 EUR x 0,775",
    fin="BUT puis ecole d'ingenieurs en apprentissage (29 ans revolus ; derogation jusqu'a 35 ans en enchainement)", sel="p estime 30 %")
add(id="T42", metier="Ingenieur", statut="salarie", pays="Suisse (frontalier)", cur="CHF", resid="FR-GE",
    E=31, start=72000, m40=91200, p80=112000, pre=ING_PRE,
    C=4, Ch=3, R=4, Se=3, Sn=3, p=0.20, cap=2, ia="moyenne",
    src="S28 (ESS 2022 : diplomes HES 9 000 CHF/mois) ; estime 114 000 CHF x 0,80",
    fin="Idem T41 + permis G", sel="p estime 20 %")
add(id="T43", metier="Ingenieur", statut="salarie", pays="Allemagne", cur="EUR", resid="DE",
    E=31, start=42900, m40=58500, p80=70200, pre=ING_PRE,
    C=4, Ch=4, R=3, Se=4, Sn=3, p=0.15, cap=2, ia="moyenne",
    src="S33 (BA 2024 : IKT 6 114 EUR/mois, proxy) ; estime 75 000 EUR x 0,78",
    fin="Idem T41 + allemand", sel="p estime 15 %")
add(id="T44", metier="Technicien de maintenance industrielle", statut="salarie", pays="France",
    E=27, start=24000, m40=28800, p80=34000, pre=ALT2,
    C=3, Ch=3, R=3, Se=4, Sn=3, p=0.70, cap=1, ia="faible",
    src="S08 (INSEE 2023 : professions intermediaires mediane 2 440 EUR/mois) ; estime 2 400 EUR",
    fin="BTS MS en alternance", sel="p estime 70 %")
add(id="T45", metier="Technicien reseaux et cybersecurite", statut="salarie", pays="France",
    E=27, start=26000, m40=33600, p80=42000, pre=ALT2,
    C=3, Ch=4, R=3, Se=4, Sn=3, p=0.60, cap=1, ia="moyenne",
    src="S08 (PI mediane 2 440 EUR, D9 3 680 EUR) ; estime 2 800 EUR/mois",
    fin="BTS SIO ou BUT R&T en alternance", sel="p estime 60 %")
add(id="T46", metier="Actuaire", statut="salarie", pays="France",
    E=30, start=38000, m40=52000, p80=66000, pre=[(25, 28, 0), (29, 29, 18000)],
    C=4, Ch=4, R=4, Se=4, Sn=2, p=0.06, cap=2, ia="elevee",
    src="estime : enquete de l'Institut des actuaires non recuperee",
    fin="Licence de mathematiques + master d'actuariat", sel="p estime 6 %")

# --- Metiers techniques et manuels ---------------------------------------------
ARTISAN_PRE = [(25, 25, 10000), (26, 26, 20500), (27, 27, 21300), (28, 28, 22100), (29, 29, 22900), (30, 30, 23700)]
add(id="T47", metier="Electricien", statut="salarie", pays="France",
    E=26, start=20500, m40=26400, p80=31000, pre=[(25, 25, 10000)],
    C=3, Ch=4, R=3, Se=4, Sn=4, p=0.85, cap=1, ia="faible",
    src="S08 (INSEE 2023 : ouvriers mediane 1 920 EUR/mois) ; estime ouvrier qualifie 2 200 EUR",
    fin="Titre professionnel ou CAP adulte en moins d'un an (France Travail, CPF)", sel="p estime 85 %")
add(id="T48", metier="Electricien", statut="artisan", pays="France",
    E=31, start=26000, m40=31000, p80=45000, pre=ARTISAN_PRE,
    C=4, Ch=2, R=3, Se=3, Sn=4, p=0.45, cap=3, ia="faible",
    src="estime : tableau INSEE BTP non-salaries 2024 non recupere",
    fin="Idem T47 + 5 ans salarie + creation (outillage, vehicule)", sel="p estime 45 % (survie a 5 ans)")
add(id="T49", metier="Electricien", statut="salarie", pays="Suisse (frontalier)", cur="CHF", resid="FR-GE",
    E=28, start=52000, m40=62400, p80=72800, pre=[(25, 25, 10000), (26, 26, 20500), (27, 27, 21300)],
    C=3, Ch=3, R=3, Se=3, Sn=4, p=0.45, cap=2, ia="faible",
    src="S27 (CCT ELEKT 2025 : 4 500 a 5 000 CHF) + S28 (CFC mediane 6 190 CHF) ; estime 6 000 CHF x 13 x 0,80",
    fin="Idem T47 + reconnaissance SEFRI ; permis G", sel="p estime 45 %")
add(id="T50", metier="Electricien", statut="salarie", pays="Canada (Quebec)", cur="CAD", resid="CA",
    E=28, start=52880, m40=78490, p80=91800, pre=[(25, 25, 10000), (26, 26, 20500), (27, 27, 21300)],
    C=3, Ch=4, R=3, Se=4, Sn=4, p=0.35, cap=2, ia="faible",
    src="S35 (QC 2024 : mediane 41 CAD/h) ; estime 45 CAD x 1 900 h x 0,918",
    fin="Idem T47 + certificat CCQ + immigration", sel="p estime 35 %")
add(id="T51", metier="Plombier-chauffagiste", statut="artisan", pays="France",
    E=31, start=26000, m40=31000, p80=45000, pre=ARTISAN_PRE,
    C=4, Ch=2, R=3, Se=3, Sn=4, p=0.45, cap=3, ia="faible",
    src="estime : comme T48",
    fin="CAP adulte + 5 ans salarie + creation", sel="p estime 45 %")
add(id="T52", metier="Frigoriste (CVC)", statut="salarie", pays="France",
    E=27, start=23000, m40=30000, p80=36000, pre=ALT2,
    C=3, Ch=3, R=3, Se=4, Sn=4, p=0.70, cap=1, ia="faible",
    src="S08 (ouvriers et PI) ; estime 2 500 EUR/mois",
    fin="CAP ou BTS froid en alternance", sel="p estime 70 %")
add(id="T53", metier="Conducteur de train", statut="salarie (SNCF)", pays="France",
    E=26, start=24000, m40=37200, p80=45600, pre=[(25, 25, 19000)],
    C=2, Ch=3, R=3, Se=4, Sn=4, p=0.30, cap=1, ia="faible",
    src="S15 (SNCF : 26 a 34 kEUR brut apres formation) ; estime 3 100 EUR/mois a 40 ans",
    fin="Recrutement + 12 mois de formation remuneree", sel="Tests psychotechniques ; p estime 30 %")
add(id="T54", metier="Conducteur de train", statut="salarie", pays="Suisse (resident)", cur="CHF", resid="CH",
    E=26, start=60000, m40=72800, p80=81600, pre=[(25, 25, 37600, "CHF", "CH")],
    C=2, Ch=3, R=3, Se=4, Sn=4, p=0.15, cap=2, ia="faible",
    src="S55 (BLS : 3 615 CHF/mois en formation) + S22 ; estime 7 000 CHF x 13 x 0,80",
    fin="Formation 14 a 16 mois remuneree ; residence pres du depot", sel="p estime 15 %")
add(id="T55", metier="Conducteur poids lourd", statut="salarie", pays="France",
    E=25, start=22000, m40=26400, p80=31000, pre=[],
    C=2, Ch=1, R=2, Se=4, Sn=3, p=0.85, cap=1, ia="moyenne",
    src="S08 (ouvriers mediane 1 920 EUR) + heures supplementaires ; estime 2 200 EUR",
    fin="Permis C/CE + FIMO (3 mois, finances)", sel="p estime 85 %")

# --- Public, droit, finance ----------------------------------------------------
ENS_PRE = [(25, 27, 0), (28, 28, 16800), (29, 29, 21600)]
add(id="T56", metier="Professeur des ecoles", statut="fonctionnaire", pays="France",
    E=30, start=25200, m40=27300, p80=32400, pre=ENS_PRE,
    C=4, Ch=4, R=3, Se=5, Sn=5, p=0.40, cap=2, ia="moyenne",
    src="S44 (debut 2 100 EUR net) + S12 (point 4,92278 EUR) + S11 (DEPP : moy. 2 680 EUR) ; calcul grille echelon 7 = 2 275 EUR",
    fin="Licence puis CRPE a bac+3 + 2 ans de master remuneres (1 400 puis 1 800 EUR net)", sel="p estime 40 %")
add(id="T57", metier="Professeur certifie", statut="fonctionnaire", pays="France",
    E=30, start=25800, m40=29400, p80=34800, pre=ENS_PRE,
    C=4, Ch=4, R=3, Se=5, Sn=5, p=0.35, cap=2, ia="moyenne",
    src="S11 (DEPP 2024 : certifies 3 130 EUR moy. tous ages) ; calcul grille 2 450 EUR",
    fin="Licence puis CAPES a bac+3 + 2 ans remuneres", sel="p estime 35 %")
add(id="T58", metier="Gardien de la paix", statut="fonctionnaire", pays="France",
    E=26, start=26400, m40=34200, p80=39600, pre=[(25, 25, 19000)],
    C=2, Ch=2, R=2, Se=5, Sn=4, p=0.30, cap=1, ia="faible",
    src="S13 (grille brigadier-chef 2 550 a 2 678 EUR brut + ISSP 28,5 %)",
    fin="Concours (bac) + 12 mois remuneres (1 570 a 1 617 EUR net)", sel="p estime 30 %")
add(id="T59", metier="Sapeur-pompier professionnel", statut="fonctionnaire territorial", pays="France",
    E=27, start=24000, m40=30600, p80=34000, pre=[],
    C=2, Ch=2, R=4, Se=5, Sn=5, p=0.08, cap=1, ia="faible",
    src="estime : grille cat. C + indemnite de feu (non recuperee)",
    fin="Volontariat + concours + recrutement par un SDIS", sel="p estime 8 %")
add(id="T60", metier="Attache d'administration", statut="fonctionnaire", pays="France",
    E=29, start=27600, m40=33000, p80=42000, pre=[(25, 27, 0), (28, 28, 21600)],
    C=3, Ch=4, R=3, Se=5, Sn=3, p=0.10, cap=2, ia="moyenne",
    src="estime : grille attache + IFSE ; ancrage S66 (DGAFP : cat. A 3 321 EUR moy. 2023, via secondaire)",
    fin="Licence + concours IRA + 1 an remunere", sel="p estime 10 %")
add(id="T61", metier="Inspecteur des finances publiques", statut="fonctionnaire", pays="France",
    E=29, start=30000, m40=38400, p80=48000, pre=[(25, 27, 0), (28, 28, 22800)],
    C=3, Ch=4, R=3, Se=5, Sn=3, p=0.15, cap=2, ia="moyenne",
    src="estime : grille + primes DGFiP ; ancrage S67 (INSEE FPE 2024 : cat. A 3 543 EUR moy.)",
    fin="Licence + concours + ENFiP remuneree", sel="p estime 15 %")
add(id="T62", metier="Controleur des finances publiques", statut="fonctionnaire", pays="France",
    E=26, start=24000, m40=30600, p80=36000, pre=[(25, 25, 20400)],
    C=3, Ch=5, R=3, Se=5, Sn=3, p=0.30, cap=1, ia="moyenne",
    src="estime : grille B + primes DGFiP ; ancrage S66 (DGAFP : cat. B 2 588 EUR moy. 2023)",
    fin="Concours de niveau bac + formation remuneree", sel="p estime 30 %")
add(id="T63", metier="Controleur aerien (ICNA)", statut="fonctionnaire", pays="France",
    E=30, start=48000, m40=66000, p80=78000, pre=[(25, 27, 21600), (28, 29, 30000)],
    C=2, Ch=3, R=4, Se=5, Sn=4, p=0.01, cap=1, ia="faible",
    src="estime : S68 (Cour des comptes 2010 via iFRAP : 5 000 EUR net/mois moy.), revalorise",
    fin="Concours externe : moins de 26 ans au 1er janvier, niveau CPGE ; formation remuneree", sel="Fenetre 2027-2028 seulement ; p estime 1 %")
add(id="T64", metier="Administrateur UE (AD)", statut="fonctionnaire europeen", pays="Luxembourg (resident)", cur="EUR", resid="LU",
    E=29, start=76930, m40=98780, p80=108780, pre=[(25, 27, 0), (28, 28, 19000)],
    C=3, Ch=4, R=3, Se=5, Sn=3, p=0.03, cap=2, ia="moyenne",
    src="S31 (AD5 echelon 1 : 6 152,64 EUR de base) + indemnite de depaysement 16 % ; estime AD7 a 40 ans ; avant impot UE",
    fin="Licence + concours EPSO AD5 (C1 + B2)", sel="2026 : environ 3 % de reussite ; p estime 3 %")
add(id="T65", metier="Agent contractuel UE (GF II-III)", statut="contractuel", pays="Luxembourg (frontalier)", cur="EUR", resid="FR-LO",
    E=26, start=33685, m40=45910, p80=57070, pre=[],
    C=2, Ch=4, R=3, Se=3, Sn=3, p=0.15, cap=1, ia="elevee",
    src="S31 (GF II-4 : 2 714,73 EUR ; GF III-8 : 3 475,62 EUR) ; estime base 3 700 EUR a 40 ans + 16 %",
    fin="CAST permanent (bac + 3 ans d'experience, C1 + B2), inscription continue", sel="p estime 15 %")
add(id="T66", metier="Sous-officier", statut="militaire", pays="France",
    E=26, start=22800, m40=33000, p80=40000, pre=[(25, 25, 18000)],
    C=2, Ch=2, R=4, Se=4, Sn=4, p=0.70, cap=1, ia="faible",
    src="estime : grille de solde non recuperee",
    fin="Ecole de sous-officiers 8 mois (moins de 32 ans, bac)", sel="p estime 70 %")
add(id="T67", metier="Avocat", statut="liberal", pays="France",
    E=32, start=34600, m40=49000, p80=94000, pre=[(25, 29, 0), (30, 30, 3000), (31, 31, 6000)],
    C=3, Ch=3, R=3, Se=3, Sn=3, p=0.25, cap=2, ia="moyenne",
    src="S18 (mediane 2022 : 49 342 EUR ; debut 34 627 EUR) x 0,94 ajuste anciennete",
    fin="Licence + M1 + CRFPA (3 tentatives) + 18 mois", sel="Reussite 25 a 35 % ; p estime 25 %")
add(id="T68", metier="Expert-comptable", statut="liberal", pays="France",
    E=33, start=45000, m40=65000, p80=103000,
    pre=[(25, 25, 11000), (26, 27, 17300), (28, 29, 18500), (30, 32, 25000)],
    C=4, Ch=3, R=3, Se=4, Sn=3, p=0.20, cap=1, ia="moyenne",
    src="S20 (UNASA 2024 : 87 024 EUR moy.) ; estime debut d'exercice",
    fin="DCG + DSCG en alternance + stage 3 ans + DEC", sel="p estime 20 %")
add(id="T69", metier="Comptable", statut="salarie", pays="France",
    E=27, start=22800, m40=28800, p80=34000, pre=ALT2,
    C=3, Ch=5, R=3, Se=3, Sn=3, p=0.75, cap=1, ia="elevee",
    src="S08 (PI) ; estime 2 400 EUR/mois",
    fin="BTS CG en alternance", sel="p estime 75 %")
add(id="T70", metier="Comptable", statut="salarie", pays="Luxembourg (frontalier)", cur="EUR", resid="FR-LO",
    E=27, start=36750, m40=54250, p80=65625, pre=ALT2,
    C=3, Ch=4, R=3, Se=3, Sn=2, p=0.45, cap=1, ia="elevee",
    src="S30 (STATEC 2022 : mediane 58 126 EUR) ; estime 62 000 EUR x 0,875",
    fin="BTS CG + emploi au Luxembourg", sel="p estime 45 %")
add(id="T71", metier="Magistrat", statut="fonctionnaire", pays="France",
    E=33, start=40000, m40=51600, p80=60000, pre=[(25, 29, 0), (30, 32, 21600)],
    C=4, Ch=3, R=3, Se=5, Sn=5, p=0.08, cap=2, ia="faible",
    src="estime : grille magistrats + primes non recuperee",
    fin="Licence + M1 + concours ENM + 31 mois remuneres", sel="Environ 10,5 % de reussite ; p estime 8 %")

# --- Paramedical a 2-3 ans, ajoutes pour completer le pool -----------------------
add(id="T76", metier="Pedicure-podologue", statut="liberal", pays="France",
    E=28, start=22000, m40=33000, p80=45000, pre=[(25, 27, -5000)],
    C=5, Ch=4, R=4, Se=4, Sn=4, p=0.25, cap=3, ia="faible",
    src="estime : S69 (Observatoire de l'activite liberale, DGE : 27 600 EUR moy. en 2011), revalorise ; serie recente non recuperee",
    fin="DE 3 ans (instituts surtout prives, 6 a 8 kEUR/an)", sel="p estime 25 %")
add(id="T77", metier="Ergotherapeute", statut="fonctionnaire FPH", pays="France",
    E=28, start=23000, m40=30000, p80=34000, pre=[(25, 27, 0)],
    C=3, Ch=5, R=4, Se=5, Sn=5, p=0.08, cap=2, ia="faible",
    src="S65 (grille ergotherapeute FPH : IM 395 a 727, soit 1 944 a 3 579 EUR brut) + CTI 183 EUR net/mois ; calcul echelon a 10 ans",
    fin="DE 3 ans (Parcoursup ou apres annee sante)", sel="Selectif ; p estime 8 %")
add(id="T78", metier="Dieteticien", statut="liberal", pays="France",
    E=27, start=15000, m40=24000, p80=32000, pre=[(25, 26, 0)],
    C=4, Ch=5, R=4, Se=2, Sn=4, p=0.50, cap=2, ia="moyenne",
    src="estime : aucune serie recuperee",
    fin="BTS dietetique ou BUT 2 a 3 ans", sel="p estime 50 %")
add(id="T79", metier="Opticien", statut="salarie", pays="France",
    E=27, start=21500, m40=27000, p80=32000, pre=ALT2,
    C=2, Ch=4, R=3, Se=4, Sn=3, p=0.70, cap=1, ia="faible",
    src="S08 (PI mediane 2 440 EUR) ; estime 2 250 EUR/mois",
    fin="BTS OL en alternance", sel="p estime 70 %")

# --- Commerce et autres --------------------------------------------------------
add(id="T72", metier="Commercial B2B", statut="salarie", pays="France",
    E=27, start=28000, m40=38400, p80=55000, pre=ALT2,
    C=4, Ch=3, R=3, Se=3, Sn=2, p=0.80, cap=1, ia="moyenne",
    src="S08 (PI et cadres) ; estime 3 200 EUR/mois variable inclus",
    fin="Embauche directe ou BTS NDRC en alternance", sel="p estime 80 %")
add(id="T73", metier="Agent immobilier", statut="independant (mandataire)", pays="France",
    E=26, start=18000, m40=24000, p80=45000, pre=[(25, 25, 10000)],
    C=4, Ch=3, R=3, Se=1, Sn=2, p=0.50, cap=1, ia="moyenne",
    src="estime : aucune serie ; forte volatilite",
    fin="Statut d'agent commercial, formation courte", sel="p estime 50 % (survie)")
add(id="T74", metier="Pilote de ligne", statut="salarie", pays="France",
    E=28, start=45000, m40=84000, p80=110000, pre=[(25, 26, -50000), (27, 27, 0)],
    C=2, Ch=2, R=3, Se=3, Sn=3, p=0.10, cap=5, ia="faible",
    src="estime : aucune serie officielle recuperee",
    fin="ATPL integre (environ 100 kEUR) ou EPL (condition d'age non verifiee)", sel="p estime 10 %")
add(id="T75", metier="Employe commerce ou accueil (reference)", statut="salarie", pays="France",
    E=24, start=18000, m40=21000, p80=25000, pre=[],
    C=2, Ch=3, R=2, Se=3, Sn=2, p=1.0, cap=1, ia="moyenne",
    src="S08 (employes mediane 1 800 EUR/mois) + SMIC 2026 1 823,03 EUR brut (S43)",
    fin="Aucune", sel="p 100 %")

# ---------------------------------------------------------------------------
# 5. Calculs
# ---------------------------------------------------------------------------

def revenu_annuel(t, age):
    """(revenu local, devise, residence) pour un age donne."""
    if age < t["E"]:
        for ph in t["pre"]:
            a0, a1, inc = ph[0], ph[1], ph[2]
            cur = ph[3] if len(ph) > 3 else "EUR"
            res = ph[4] if len(ph) > 4 else "FR"
            if a0 <= age <= a1:
                return inc, cur, res
        return base(age), "EUR", "FR"  # emploi actuel conserve
    if age <= 40:
        if t["E"] >= 40:
            inc = t["m40"]
        else:
            inc = t["start"] + (t["m40"] - t["start"]) * (age - t["E"]) / (40 - t["E"])
    else:
        inc = t["m40"] * (1 + CROISSANCE_APRES_40) ** (age - 40)
    return inc, t["cur"], t["resid"]


def classer(score):
    for nom, s in SEUILS:
        if score >= s:
            return nom
    return "C"


def proche_frontiere(score):
    return any(abs(score - s) < 0.1 for _, s in SEUILS)


# Indice de barriere continu (1 = faible, 5 = forte), moyenne simple de 4 composantes.
def b_delai(n):
    """Annees entre 24 ans et l'entree ; 12 ans ou plus = 5."""
    return 1 + 4 * min(1.0, n / 12)


def b_pertes(x):
    """Annees de revenu perdues par rapport a l'emploi immediat ; 8 ou plus = 5."""
    return 1 + 4 * min(1.0, x / 8)


def b_proba(p):
    """Echelle log : p = 100 % donne 1, p <= 2 % donne 5."""
    return 1 + 4 * min(1.0, math.log(1 / p) / math.log(50))


for t in T:
    fp = facteur_ppa(t["cur"], t["resid"])
    fn = facteur_nominal(t["cur"])
    t["m40_nom"], t["p80_nom"] = t["m40"] * fn, t["p80"] * fn
    t["m40_ppa"], t["p80_ppa"] = t["m40"] * fp, t["p80"] * fp
    cum_nom = cum_ppa = pertes = 0.0
    for a in AGES:
        inc, cur, res = revenu_annuel(t, a)
        v_ppa = inc * facteur_ppa(cur, res)
        cum_ppa += v_ppa
        cum_nom += inc * facteur_nominal(cur)
        if a < t["E"]:
            pertes += max(0.0, base(a) - v_ppa) / base(a)
    t["cum_nom"], t["cum_ppa"], t["pertes"] = cum_nom, cum_ppa, pertes
    t["b"] = [b_delai(t["E"] - 24), b_pertes(pertes), b_proba(t["p"]), t["cap"]]
    t["B"] = sum(t["b"]) / 4


def echelle_log(vals):
    lo, hi = min(vals), max(vals)
    return lo, hi, (lambda x: max(1.0, min(5.0, 1 + 4 * (math.log(x) - math.log(lo)) / (math.log(hi) - math.log(lo)))))


BORNES = {}
for k in ("m40_ppa", "p80_ppa", "cum_ppa"):
    lo, hi, f = echelle_log([t[k] for t in T])
    BORNES[k] = (lo, hi, f)


def score_revenu(t, mult=1.0):
    return sum(BORNES[k][2](t[k] * mult) for k in ("m40_ppa", "p80_ppa", "cum_ppa")) / 3


def total(t, rev, se):
    return (POIDS["C"] * t["C"] + POIDS["Ch"] * t["Ch"] + POIDS["R"] * t["R"]
            + POIDS["Se"] * se + POIDS["Sn"] * t["Sn"] + POIDS["Rev"] * rev) / 100


# Scenario IA fort (poids de preuve faible) : exposition moyenne = Securite -1 et revenus x 0,9 ;
# exposition elevee = Securite -2 et revenus x 0,8. Scenario IA faible = scenario de base.
IA_FORT = {"faible": (0, 1.0), "moyenne": (1, 0.9), "elevee": (2, 0.8)}
for t in T:
    t["Rev"] = score_revenu(t)
    t["W"] = total(t, t["Rev"], t["Se"])
    t["palier"] = classer(t["W"])
    t["proche"] = proche_frontiere(t["W"])
    d_se, mult = IA_FORT[t["ia"]]
    if "fonctionnaire" in t["statut"]:  # statut protege : choc de securite reduit d'un cran
        d_se = max(0, d_se - 1)
    t["Se_ia"] = max(1, t["Se"] - d_se)
    t["Rev_ia"] = score_revenu(t, mult)
    t["W_ia"] = total(t, t["Rev_ia"], t["Se_ia"])
    t["palier_ia"] = classer(t["W_ia"])

CRIT = ("C", "Ch", "R", "Se", "Sn", "Rev")
CRIT_IA = ("C", "Ch", "R", "Se_ia", "Sn", "Rev_ia")


def domine(y, x, crit=CRIT):
    """y domine x : au moins aussi bon sur les 6 criteres ET sur chaque composante brute de la
    barriere (age d'entree, annees perdues, probabilite, capital), strictement meilleur une fois."""
    py, px = round(y["pertes"], 1), round(x["pertes"], 1)
    ge = (all(y[k] >= x[k] for k in crit) and y["E"] <= x["E"] and py <= px
          and y["p"] >= x["p"] and y["cap"] <= x["cap"])
    gt = (any(y[k] > x[k] for k in crit) or y["E"] < x["E"] or py < px
          or y["p"] > x["p"] or y["cap"] < x["cap"])
    return ge and gt


# Elimination retenue seulement si la domination tient dans les deux scenarios IA.
for x in T:
    x["domine_par"] = [y["id"] for y in T if y is not x and domine(y, x) and domine(y, x, CRIT_IA)]
    x["domine_base_seul"] = [y["id"] for y in T if y is not x and domine(y, x) and not domine(y, x, CRIT_IA)]

finaux = [t for t in T if not t["domine_par"]]


def pareto(ens):
    out = []
    for x in ens:
        if not any((y["W"] >= x["W"] and y["B"] <= x["B"]) and (y["W"] > x["W"] or y["B"] < x["B"]) for y in ens if y is not x):
            out.append(x)
    return sorted(out, key=lambda t: t["B"])


front = pareto(T)

# ---------------------------------------------------------------------------
# 6. Sorties
# ---------------------------------------------------------------------------

def k(x):
    return f"{x / 1000:.0f}"


def triplet(t):
    return f"{t['metier']} x {t['statut']} x {t['pays']}"


lignes = []
lignes.append("## Bornes de l'echelle log (EUR PPA France)\n")
for key, (lo, hi, _) in BORNES.items():
    lignes.append(f"- {key} : min {lo:,.0f}, max {hi:,.0f}")
lignes.append("")
lignes.append("## Pool\n")
lignes.append("| ID | Triplet | C | Ch | R | Se | Sn | Med40 PPA kEUR | Cumul PPA kEUR | Barriere | W | Palier |")
lignes.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for t in sorted(T, key=lambda t: -t["W"]):
    lignes.append(f"| {t['id']} | {triplet(t)} | {t['C']} | {t['Ch']} | {t['R']} | {t['Se']} | {t['Sn']} | {k(t['m40_ppa'])} | {k(t['cum_ppa'])} | {t['B']:.2f} | {t['W']:.3f} | {t['palier']}{'*' if t['proche'] else ''} |")
lignes.append("")
lignes.append("## Elimines (domines)\n")
for t in T:
    if t["domine_par"]:
        lignes.append(f"- {t['id']} {triplet(t)} : domine par {', '.join(t['domine_par'])}")
    elif t["domine_base_seul"]:
        lignes.append(f"- (conserve) {t['id']} {triplet(t)} : domine seulement sans IA par {', '.join(t['domine_base_seul'])}")
lignes.append("")
lignes.append("## Frontiere de Pareto (W, B)\n")
for t in front:
    lignes.append(f"- {t['id']} {triplet(t)} : B={t['B']:.2f} W={t['W']:.3f} {t['palier']}")
lignes.append("")
lignes.append("## Detail revenus et barriere\n")
lignes.append("| ID | Med40 nom | Med40 PPA | P80 nom | P80 PPA | Cumul nom | Cumul PPA | E | pertes | b | IA | Palier IA fort |")
lignes.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for t in T:
    lignes.append(f"| {t['id']} | {k(t['m40_nom'])} | {k(t['m40_ppa'])} | {k(t['p80_nom'])} | {k(t['p80_ppa'])} | {k(t['cum_nom'])} | {k(t['cum_ppa'])} | {t['E']} | {t['pertes']:.1f} | {'/'.join(f'{v:.1f}' for v in t['b'])} | {t['ia']} | {t['palier_ia']} ({t['W_ia']:.2f}) |")

ici = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ici, "resultats.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lignes) + "\n")
with open(os.path.join(ici, "resultats.json"), "w", encoding="utf-8") as f:
    json.dump([{kk: v for kk, v in t.items() if kk != "pre"} for t in T], f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    from collections import Counter
    print("Pool :", len(T), "triplets ; finaux :", len(finaux), "; frontiere :", len(front))
    print("Paliers :", Counter(t["palier"] for t in T))
    print("Paliers finaux :", Counter(t["palier"] for t in finaux))
