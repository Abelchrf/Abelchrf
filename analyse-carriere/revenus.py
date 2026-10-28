# -*- coding: utf-8 -*-
"""Cellules revenu de la version 4 (28 octobre 2026), une par triplet.

Definition : revenu net annuel d'un professionnel installe, en devise locale, apres cotisations
et contributions sociales (CSG et CRDS comprises en France), avant impot sur le revenu, au temps
de travail reel indique. Mediane de la profession tous ages ; a defaut moyenne convertie. Aucune
decote pour l'entree tardive du sujet (barriere d'entree, hors score).

Regles de conversion declarees avant calcul (section 1.11 du rapport) :
- France, salaries : salaire net publie tel quel ; brut x 0,78.
- France, liberaux : revenus Insee (CSG et CRDS non deduites, S97) x 0,874 = 1 - 9,7 % x 1,3
  (assiette = revenu + cotisations, environ 1,3 fois le revenu) ; artisans (cotisations plus lourdes)
  x 0,864 = 1 - 9,7 % x 1,4 ; benefices fiscaux DREES, CARMF, CARCDSF, CNBF, UNASA (CSG deductible
  deja retiree) x 0,96.
- Moyenne seule publiee : non-salaries x 0,85 (ADA 2023 : 185 360 / 218 710 = 0,85 ; OFS 2019,
  premier recours : 172 000 / 199 975 = 0,86) ; grilles statutaires x 1 (moyenne et mediane proches :
  fonction publique de l'Etat 2024, moyenne 3 018 EUR, mediane relayee 3 044 EUR).
- P80 : interpolation lineaire entre P75 et P90 publies ; sinon log-normale (sigma tire du rapport
  moyenne / mediane de la meme source, ou sigma des liberaux = 0,57, soit P80 = 1,62 x mediane) ;
  grilles statutaires sans dispersion publiee : 1,2 x mediane (amplitude de grille) ; autres salaries
  sans dispersion publiee : rapport P80 / median de la v3 (estime).
- Suisse : salaries brut x 0,80 (AVS, AC, LPP, AANP, LAMal) ; medecins salaries x 0,83 ; independants :
  revenu OFS net d'AVS et de 2e pilier moins la prime LAMal moyenne adulte (449,20 CHF x 12, S112).
- Etats-Unis : salaires BLS x 0,91 ; proprietaires (ADA) : moins la cotisation des independants
  (15,3 % sur 92,35 % du revenu jusqu'a 176 100 USD, 2,9 % au-dela, 0,9 % au-dela de 200 000 USD)
  et 7 000 USD d'assurance sante individuelle (estime).
- Allemagne x 0,78 ; Luxembourg x 0,875 ; Quebec x 0,918 ; Irlande : PRSI 4,2 % et USC (S85).
"""
import math

Z80 = 0.8416
NET_INSEE = 1 - 0.097 * 1.3
NET_INSEE_ARTISAN = 1 - 0.097 * 1.4
NET_BNC = 0.96
MED_MOY_LIB = 0.85
P80_LIB = math.exp(Z80 * math.sqrt(2 * math.log(1 / MED_MOY_LIB)))
P80_GRILLE = 1.2
LAMAL = 449.20 * 12
SRC_LIB = "estimé : log-normale des libéraux (× 1,62)"
SRC_GRILLE = "estimé : amplitude de grille (× 1,2)"


def p80_ln(med, moy_sur_med):
    return med * math.exp(Z80 * math.sqrt(2 * math.log(moy_sur_med)))


def p80_interp(p75, p90):
    return p75 + (p90 - p75) / 3


def net_proprio_us(g, sante=7000):
    b = 0.9235 * g
    return g - (0.124 * min(b, 176100) + 0.029 * b + 0.009 * max(0, b - 200000)) - sante


def net_irlande(g):
    usc = (0.005 * min(g, 12012) + 0.02 * max(0, min(g, 27382) - 12012)
           + 0.03 * max(0, min(g, 70044) - 27382) + 0.08 * max(0, g - 70044))
    return g - usc - 0.042 * g


def c(med, p80, h, src_med, src_p80, fiab):
    return dict(med=round(med, -2), p80=round(p80, -2), h=h, src_med=src_med, src_p80=src_p80, fiab=fiab)


def lib(med, h, src, fiab):
    return c(med, med * P80_LIB, h, src, SRC_LIB, fiab)


def grille(med, h, src, fiab):
    return c(med, med * P80_GRILLE, h, src, SRC_GRILLE, fiab)


def v3(med, p80, src, h="non trouvé"):
    return c(med, p80, h, "non re-sourcé, valeur v3 : " + src, "estimé (v3)", "non re-sourcée")


def sal(med, ratio, h, src, fiab):
    return c(med, med * ratio, h, src, f"estimé : rapport P80/médian de la v3 (× {ratio:.2f})", fiab)


H_NT = "non trouvé"
H_FR = "35 h légales (non mesurée)"
H_CH = "41 h 47 contractuelles, tous salariés (OFS 2024, S112)"
H_US = "40 h usuelles (non mesurée)"

REV = {
    # --- Santé, France : médecins, dentistes, pharmaciens, vétérinaires -------------------------
    "T01": lib(98300 * NET_BNC * MED_MOY_LIB, "46 h (DREES, ER 1381, données 2025, S07)",
               "DREES 2021 (S02) : omnipraticiens, revenu d'activité moyen 98 300 € ; × 0,96 × 0,85 ; recoupement CARMF 2024 (S98) : 97 099 € moy.",
               "relayée"),
    "T02": v3(64000, 76000, "estime : pas de serie officielle ; ancrage S09 (INSEE FPH 2024 : personnels medicaux 6 926 EUR/mois moy.)"),
    "T03": lib((88400 + 92800) / 2 * NET_BNC * MED_MOY_LIB, H_NT,
               "DREES 2021 (S02) : pédiatres 88 400 €, psychiatres 92 800 € moy. (spécialités du rang médian) ; × 0,96 × 0,85 ; CARMF 2022 (S98), part libérale seule : 74 884 € et 73 014 €",
               "relayée"),
    "T04": grille(6926 * 12, H_NT,
                  "Insee FPH 2024 (S09) : personnels médicaux, 6 926 €/mois net moyen en EQTP ; moyenne = médiane (grille)",
                  "officielle, champ plus large"),
    "T05": lib(97672 * NET_BNC, H_NT,
               "CARCDSF 2023 (S04) : médiane 97 672 € ; × 0,96 ; recoupement Insee (S99) : dentistes 10 300 €/mois moy.",
               "relayée"),
    "T06": v3(40000, 48000, "estime : grille de la convention collective officine (non recuperee) ; aucune serie officielle"),
    "T07": lib(6390 * 12 * NET_INSEE * MED_MOY_LIB, H_NT,
               "Insee 2024 (S99) : pharmaciens non salariés, 6 390 €/mois moy. ; × 0,874 × 0,85",
               "relayée"),
    "T19": lib(6370 * 12 * NET_INSEE * MED_MOY_LIB, H_NT,
               "Insee 2024 (S01) : vétérinaires, 6 370 €/mois moy. ; × 0,874 × 0,85",
               "relayée"),
    # --- Santé, France : paramédical ------------------------------------------------------------
    "T08": grille(3442 * 12, H_NT,
                  "DREES 2022 (S10) : sages-femmes salariées des hôpitaux, 3 442 €/mois net moyen (3 487 € dans le tableau) ; moyenne = médiane (grille)",
                  "officielle"),
    "T09": lib(42200 * NET_BNC * MED_MOY_LIB, H_NT,
               "DREES 2021 (S03) : sages-femmes libérales, 42 200 € moy. ; × 0,96 × 0,85", "officielle"),
    "T10": lib(51100 * NET_BNC * MED_MOY_LIB, H_NT,
               "DREES 2021 (S03) : masseurs-kinésithérapeutes libéraux, 51 100 € moy. ; × 0,96 × 0,85", "officielle"),
    "T11": v3(30000, 34000, "estime : grille reeducateurs FPH ; ancrage S09"),
    "T12": grille(2755 * 12, "12 h ou 7 h 30 par poste ; durée non trouvée",
                  "DREES 2022 (S10) : infirmiers, 2 755 €/mois net moyen en EQTP, toutes structures ; moyenne = médiane (grille) ; FPH 2024, tous agents : moyenne 2 896 €, médiane 2 474 € (S100)",
                  "officielle"),
    "T13": lib(57100 * NET_BNC * MED_MOY_LIB, H_NT,
               "DREES 2021 (S03) : infirmiers libéraux, 57 100 € moy. ; × 0,96 × 0,85", "officielle"),
    "T14": v3(42000, 48000, "estime : grille IADE FPH ; ancrage S09"),
    "T15": lib(27550 * NET_BNC * MED_MOY_LIB, "temps partiel fréquent, durée non trouvée",
               "UNASA 2022 (S06) : 27 550 € moy., temps partiel inclus ; × 0,96 × 0,85 ; recoupement FNO 2023 : 2 400 €/mois moy.",
               "non officielle"),
    "T16": v3(31200, 36000, "estime : aucune serie officielle recuperee"),
    "T17": v3(33600, 38000, "estime : grille paramedicale cat. A FPH ; ancrage S09"),
    "T18": v3(36000, 45000, "S21 (APEC : offres 36 600 EUR brut moy. ; confirme 2 300-3 100 EUR net/mois)"),
    "T20": v3(30000, 35000, "estime : grille psychologues FPH ; aucune serie recuperee"),
    "T21": grille(2184 * 12, "12 h ou 7 h 30 par poste ; durée non trouvée",
                  "DREES 2022 (S10) : aides-soignants et ASH, 2 184 €/mois net moyen ; moyenne = médiane (grille)",
                  "officielle, champ plus large"),
    "T22": v3(32000, 45000, "estime : aucune serie officielle recuperee"),
    "T76": v3(33000, 45000, "estime : S69 (Observatoire de l'activite liberale, DGE : 27 600 EUR moy. en 2011), revalorise"),
    "T77": c(30000, 34000, H_NT, "grille officielle FPH (S65) : IM 395 à 727 + CTI 183 € net/mois ; calcul à 10 ans d'exercice", "estimé (v3)", "officielle (grille)"),
    "T78": v3(24000, 32000, "estime : aucune serie recuperee"),
    "T79": v3(27000, 32000, "S08 (PI mediane 2 440 EUR) ; estime 2 250 EUR/mois"),
    # --- Santé, étranger ---------------------------------------------------------------------------
    "T23": c(7400 * 12 * 1.074 * 0.80, 89600, H_CH,
             "OFSP (S23) : médiane des infirmiers 7 400 CHF/mois, 2018 ; × 1,074 (hausse de la médiane ESS 2018-2024) × 0,80",
             "v3 (haut de la fourchette HUG, S64)", "officielle ancienne"),
    "T24": c(7400 * 12 * 1.074 * 0.80, 89600, H_CH,
             "OFSP (S23) : médiane des infirmiers 7 400 CHF/mois, 2018 ; × 1,074 × 0,80", "v3 (S64)", "officielle ancienne"),
    "T25": c(75075, 91000, "40 h (non mesurée)", "grille officielle FHL (S29) : 6 600 €/mois × 13 à 12 ans d'exercice ; × 0,875", "estimé (v3)", "officielle (grille)"),
    "T26": c(75075, 91000, "40 h (non mesurée)", "grille officielle FHL (S29) : 6 600 €/mois × 13 à 12 ans d'exercice ; × 0,875", "estimé (v3)", "officielle (grille)"),
    "T27": sal(4310 * 12.8 * 0.78, 51480 / 45240, H_NT,
               "Destatis avril 2024 (S32) : 4 310 €/mois brut ; × 12,8 (primes annuelles, estimé) × 0,78", "relayée"),
    "T28": c(40 * 1950 * 0.918, math.exp(math.log(40) + Z80 / 0.6745 * math.log(45 / 40)) * 1950 * 0.918, "37,5 à 40 h (non mesurée)",
             "Guichet-Emplois, Québec 2024 (S35) : médiane 40 CAD/h ; × 1 950 h × 0,918",
             "log-normale entre la médiane et le salaire élevé (45 CAD/h, lu comme Q3)", "officielle"),
    "T29": sal(197100 * 0.83, 182600 / 141100, "50,7 h (médecins assistants, ASMAC 2023, S109)",
               "BASS pour l'OFSP (S110) : revenu AVS médian des médecins salariés 197 100 CHF, 2014 ; × 0,83", "officielle ancienne"),
    "T30": c(172000 - LAMAL, p80_ln(172000, 199975 / 172000) - LAMAL, "plein temps = 10 demi-journées (OFS) ; heures non trouvées",
             "OFS 2019 (S24, S108) : premier recours, médiane 172 000 CHF nets d'AVS et de 2e pilier (relayée par la presse) ; moins la prime LAMal",
             "log-normale (moyenne OFS 199 975 CHF)", "relayée"),
    "T31": c(102900, 119000, "48 h au plus (non mesurée)", "grille officielle TV-Ärzte VKA (S34) : Facharzt + gardes, 121 000 € brut estimé ; × 0,78", "estimé (v3)", "officielle (grille)"),
    "T32": v3(180000, 240000, "estime : donnees RAMQ/ICIS non recuperees ; 180 000 CAD nets de frais"),
    "T33": sal(5866 * 12 * 0.80, 62400 / 57200, H_CH,
               "OFS, ESS 2024 (S22) : niveau de compétence 2, médiane 5 866 CHF/mois (proxy) ; × 12 × 0,80", "officielle, proxy"),
    "T34": sal(7523 * 12 * 0.80, 83200 / 74880, H_CH,
               "OFS, ESS 2024 (S22) : niveau de compétence 3, médiane 7 523 CHF/mois (proxy) ; × 12 × 0,80", "officielle, proxy"),
    "T91": lib(88 * 1800 * 0.85, "non trouvé (1 800 h par an supposées)",
               "ZHAW pour la FMH (S111) : revenu horaire médian des dentistes 88 CHF (versions en conflit : 73 à 88 CHF), statut non précisé ; × 1 800 h × 0,85",
               "sans source fiable"),
    "T92": c(net_proprio_us(185360), net_proprio_us(p80_ln(185360, 218710 / 185360)), "36,1 h au cabinet (ADA, 2024, S114)",
             "ADA HPI 2023 (S114) : médiane 185 360 USD, généralistes en cabinet privé ; moins cotisation des indépendants et assurance santé",
             "log-normale (moyenne ADA 218 710 USD)", "officielle (ordre professionnel)"),
    "T93": c(95410 * 0.91, p80_interp(112510, 132850) * 0.91, H_US,
             "BLS OEWS mai 2024 (S113) : orthophonistes, médiane 95 410 USD ; × 0,91",
             "interpolé entre P75 112 510 et P90 132 850 USD (S113)", "officielle"),
    # --- Numérique, ingénierie -----------------------------------------------------------------
    "T35": v3(40500, 50700, "S17 (APEC 2025 : IT 35-45 ans 49 a 101 kEUR) ; estime 52 000 EUR brut x 0,78"),
    "T36": c(58000, 76000, H_NT, "non officielle : TJM Malt (S19) 576 € × 170 jours × 0,59 ; Insee 2024 (S106), information et communication : 4 190 €/mois moy., champ plus large",
             "estimé (v3)", "non officielle"),
    "T37": sal(9490 * 12 * 0.80, 108000 / 91200, H_CH,
               "OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois ; × 12 × 0,80", "relayée"),
    "T38": sal(6114 * 12 * 0.78, 70200 / 56940, H_NT,
               "Bundesagentur für Arbeit 2024 (S33) : informatique, médiane 6 114 €/mois brut ; × 12 × 0,78", "relayée"),
    "T39": v3(65625, 83125, "S30 (STATEC 2022 : mediane 58 126 EUR) ; estime TIC 75 000 EUR x 0,875"),
    "T40": sal(45.67 * 1950 * 0.918, 107406 / 89505, "37,5 à 40 h (non mesurée)",
               "Guichet-Emplois, Québec 2024 (S35) : médiane 45,67 CAD/h ; × 1 950 h × 0,918", "officielle"),
    "T41": sal(67000 * 0.78, 56000 / 45000, H_NT,
               "IESF 2025 (S16) : médiane 67 000 € brut, tous ingénieurs (proxy) ; × 0,78", "relayée, proxy"),
    "T42": sal(9000 * 12 * 0.80, 112000 / 91200, H_CH,
               "OFS, ESS 2022 (S28) : diplômés HES, médiane 9 000 CHF/mois (proxy) ; × 12 × 0,80", "relayée, proxy"),
    "T43": v3(58500, 70200, "S33 (BA 2024 : IKT 6 114 EUR/mois, proxy) ; estime 75 000 EUR x 0,78"),
    "T80": sal(55000 * 0.78, 62400 / 50700, H_NT,
               "APEC 2025 (S17, S103) : famille « systèmes, réseaux et télécoms », médiane 51 k€ + 4 k€ de variable, brut (proxy) ; × 0,78", "relayée, proxy"),
    "T81": c(69000, 90000, H_NT, "non officielle : TJM Free-Work et Morgan Philips (S74, S75) 650 € × 180 jours × 0,59 ; Insee 2024 (S106) : 4 190 €/mois moy., champ plus large",
             "estimé (v3)", "non officielle"),
    "T82": sal(9490 * 12 * 0.80, 116000 / 100000, H_CH,
               "OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre au cloud) ; × 12 × 0,80", "relayée, proxy"),
    "T83": sal(64000 * 0.78, 60800 / 48400, H_NT,
               "APEC 2025 (S17, S103) : famille « sécurité informatique », médiane 60 k€ + 4 k€ de variable, brut ; × 0,78", "relayée"),
    "T84": v3(39000, 46800, "estime : S76 (bas de fourchette 37 000 EUR brut) ; 50 000 EUR brut a 40 ans x 0,78"),
    "T85": sal(54000 * 0.78, 56200 / 46800, H_NT,
               "APEC 2025 (S17, S103) : famille « business intelligence », médiane 50 k€ + 4 k€ de variable, brut (proxy) ; × 0,78", "relayée, proxy"),
    "T86": sal(9490 * 12 * 0.80, 116000 / 100000, H_CH,
               "OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre au cloud) ; × 12 × 0,80", "relayée, proxy"),
    "T87": c(net_irlande(79000), net_irlande(math.exp(math.log(79000) + Z80 / 0.6745 * math.log(107000 / 79000))), "39 h (non mesurée)",
             "non officielle : Jobmentis et Morgan McKinley (S79), médiane DevOps 79 000 € brut ; moins PRSI et USC (S85)",
             "log-normale entre la médiane et P75 107 000 € (S79)", "non officielle"),
    "T88": c(130390 * 0.91, p80_interp(164440, 198030) * 0.91, H_US,
             "BLS OEWS mai 2024 (S113) : architectes réseaux et cloud (15-1241), médiane 130 390 USD ; × 0,91",
             "interpolé entre P75 164 440 et P90 198 030 USD (S113)", "officielle, proxy"),
    "T89": sal(9490 * 12 * 0.80, 112000 / 96000, H_CH,
               "OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre à la cybersécurité) ; × 12 × 0,80", "relayée, proxy"),
    "T90": c(124910 * 0.91, p80_interp(159600, 186420) * 0.91, H_US,
             "BLS OEWS mai 2024 (S113) : analystes en sécurité de l'information (15-1212), médiane 124 910 USD ; × 0,91",
             "interpolé entre P75 159 600 et P90 186 420 USD (S113)", "officielle"),
    # --- Métiers techniques et manuels ------------------------------------------------------------
    "T44": v3(28800, 34000, "S08 (INSEE 2023 : professions intermediaires mediane 2 440 EUR/mois) ; estime 2 400 EUR"),
    "T45": v3(33600, 42000, "S08 (PI mediane 2 440 EUR, D9 3 680 EUR) ; estime 2 800 EUR/mois"),
    "T47": v3(26400, 31000, "S08 (INSEE 2023 : ouvriers mediane 1 920 EUR/mois) ; estime ouvrier qualifie 2 200 EUR"),
    "T48": lib(3050 * 12 * NET_INSEE_ARTISAN * MED_MOY_LIB, H_NT,
               "Insee 2024 (S01) : construction, non-salariés classiques, 3 050 €/mois moy. (proxy) ; × 0,864 × 0,85", "relayée, proxy"),
    "T49": sal(6190 * 12 * 0.80, 72800 / 62400, H_CH,
               "OFS, ESS 2022 (S28) : titulaires d'un CFC, médiane 6 190 CHF/mois (proxy) ; × 12 × 0,80", "relayée, proxy"),
    "T50": sal(41 * 1900 * 0.918, 91800 / 78490, "40 h (non mesurée)",
               "Guichet-Emplois, Québec 2024 (S35) : électriciens en construction, médiane 41 CAD/h ; × 1 900 h × 0,918", "officielle"),
    "T51": lib(3050 * 12 * NET_INSEE_ARTISAN * MED_MOY_LIB, H_NT,
               "Insee 2024 (S01) : construction, non-salariés classiques, 3 050 €/mois moy. (proxy) ; × 0,864 × 0,85", "relayée, proxy"),
    "T52": v3(30000, 36000, "S08 (ouvriers et PI) ; estime 2 500 EUR/mois"),
    "T53": v3(37200, 45600, "S15 (SNCF : 26 a 34 kEUR brut apres formation) ; estime 3 100 EUR/mois a 40 ans"),
    "T54": v3(72800, 81600, "S55 (BLS : 3 615 CHF/mois en formation) + S22 ; estime 7 000 CHF x 13 x 0,80", h=H_CH),
    "T55": sal(1830 * 12, 31000 / 26400, H_NT,
               "SDES 2019 (S105) : ouvriers qualifiés du transport routier de marchandises, 1 830 €/mois net en EQTP (non actualisé)", "officielle ancienne"),
    # --- Public, droit, finance -----------------------------------------------------------------
    "T56": grille(2950 * 12, "43 h médiane déclarée (DEPP 2018) ; 41,8 h moyenne (2022-2023), S101",
                  "DEPP 2024 (S101) : professeurs des écoles à temps complet, 2 950 €/mois net moyen ; moyenne = médiane (grille)", "officielle"),
    "T57": grille(3220 * 12, "42 h médiane déclarée, second degré (DEPP 2018, S101)",
                  "DEPP 2024 (S101) : professeurs certifiés à temps complet, 3 220 €/mois net moyen ; moyenne = médiane (grille)", "officielle"),
    "T58": v3(34200, 39600, "S13 (grille brigadier-chef 2 550 a 2 678 EUR brut + ISSP 28,5 %) ; aucune moyenne officielle trouvee", h="cycles de 12 h 08 ; durée moyenne non mesurée (Cour des comptes)"),
    "T59": grille(3030 * 12, "gardes de 24 h ; au plus 2 256 h de présence par an, soit 1 607 h effectives (S102)",
                  "Insee 2023 (S102) : agents des SDIS, 3 030 €/mois net moyen en EQTP, sapeurs-pompiers et non-sapeurs-pompiers ; moyenne = médiane (grille)",
                  "officielle, champ plus large"),
    "T60": v3(33000, 42000, "estime : grille attache + IFSE ; ancrage S66 (DGAFP : cat. A 3 321 EUR moy. 2023, via secondaire)"),
    "T61": v3(38400, 48000, "estime : grille + primes DGFiP ; ancrage S67 (INSEE FPE 2024 : cat. A 3 543 EUR moy.)"),
    "T62": v3(30600, 36000, "estime : grille B + primes DGFiP ; ancrage S66 (DGAFP : cat. B 2 588 EUR moy. 2023)"),
    "T63": v3(66000, 78000, "estime : S68 (Cour des comptes 2010 via iFRAP : 5 000 EUR net/mois moy.), revalorise"),
    "T64": c(98780, 108780, "40 h (non mesurée)", "grilles officielles du statut (S31) : AD7 à mi-carrière + indemnité de dépaysement 16 % ; avant impôt de l'UE", "estimé (v3)", "officielle (grille)"),
    "T65": c(45910, 57070, "40 h (non mesurée)", "grilles officielles du statut (S31) : GF III + 16 %", "estimé (v3)", "officielle (grille)"),
    "T66": v3(33000, 40000, "estime : grille de solde non recuperee"),
    "T67": c(((0.43 * 65378 + 0.57 * 49491) * NET_BNC), p80_ln(0.43 * 65378 + 0.57 * 49491, (0.43 * 120198 + 0.57 * 66812) / (0.43 * 65378 + 0.57 * 49491)) * NET_BNC, H_NT,
             "CNBF, rapport 2024 (S107) : médianes nettes 65 378 € (hommes) et 49 491 € (femmes), pondérées 43/57 (part des femmes estimée) ; × 0,96",
             "log-normale (moyennes CNBF 120 198 € et 66 812 €)", "relayée"),
    "T68": lib(8240 * 12 * NET_INSEE * MED_MOY_LIB, H_NT,
               "Insee 2024 (S106) : activités juridiques et comptables, 8 240 €/mois moy. (proxy) ; × 0,874 × 0,85 ; UNASA 2024 (S20) : 87 024 € moy.",
               "relayée, proxy"),
    "T69": v3(28800, 34000, "S08 (PI) ; estime 2 400 EUR/mois"),
    "T70": v3(54250, 65625, "S30 (STATEC 2022 : mediane 58 126 EUR) ; estime 62 000 EUR x 0,875"),
    "T71": v3(51600, 60000, "estime : grille magistrats + primes non recuperee"),
    "T46": v3(52000, 66000, "estime : enquete de l'Institut des actuaires non recuperee"),
    # --- Commerce et autres -----------------------------------------------------------------------
    "T72": v3(38400, 55000, "S08 (PI et cadres) ; estime 3 200 EUR/mois variable inclus"),
    "T73": lib(2480 * 12 * NET_INSEE * MED_MOY_LIB, H_NT,
               "Insee 2024 (S106) : activités immobilières, 2 480 €/mois moy. (proxy), 27 % de revenus nuls ou déficitaires ; × 0,874 × 0,85",
               "relayée, proxy"),
    "T74": v3(84000, 110000, "estime : aucune serie officielle recuperee", h="limites de temps de vol ; non mesurée"),
    "T75": sal(1800 * 12, 25000 / 21000, H_FR,
               "Insee 2023 (S08) : employés, médiane 1 800 €/mois net", "officielle"),
}

A_RESOURCER = [i for i, r in REV.items() if r["fiab"] in ("non re-sourcée", "sans source fiable", "non officielle")]
