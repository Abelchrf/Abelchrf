# Classement de triplets métier × statut × pays

Sujet de référence : 24 ans, nationalité française, bac général, aucun diplôme du supérieur, quelques années d'emploi peu qualifié, aptitudes moyennes, ni réseau ni capital, sans charge de famille. Date de l'analyse : 11 octobre 2026. Version 3 du 13 octobre 2026 : critère lieu (télétravail) et nouveaux pays, Suisse en résident, Irlande, États-Unis (section 1.10). Version 4 du 28 octobre 2026 : classement par qualité de vie une fois installé, sans aucune barrière d'entrée dans le score, cellules revenu re-sourcées une par une (section 1.11). Version 5 du 28 octobre 2026 : grille de qualité de l'emploi d'Eurofound, 7 dimensions à poids égaux, revenu en équivalent temps plein, robustesse testée sur 8 pondérations (section 1.12) ; elle remplace la pondération personnelle. Les notes hors revenu y sont confrontées aux statistiques publiées (DARES, DREES, Insee, SSMSI, DEPP, Eurofound, OFS, BLS) selon des règles déclarées (section 1.13).

Reproductibilité : tout le calcul est dans `modele.py` (entrées) et `tableaux.py` (sorties). Changer une entrée et relancer `python3 assembler.py` régénère les tableaux et le rapport.

## 0. Limites d'accès aux données (à lire avant les chiffres)

| Limite | Effet |
|---|---|
| La politique réseau de cet environnement bloque insee.fr, drees, dares.travail-emploi.gouv.fr (données ouvertes comprises), bfs.admin.ch, statistiques.public.lu ; l'outil de lecture de pages échoue sur tous les hôtes. | Aucun tableau primaire n'a été ouvert. Les chiffres viennent de résumés de moteur de recherche citant ces sources, avec un risque de transcription. Les codes S renvoient aux pages citées. |
| Peu de médianes et de percentiles publiés par profession. | Depuis la v4, le revenu est celui d'un professionnel installé : médiane de la profession quand elle est publiée, sinon moyenne convertie par une règle déclarée (1.4). Chaque cellule porte sa source, sa conversion et un niveau de fiabilité. |
| Quota de 200 recherches web par tour, partagé entre les recherches parallèles (atteint en v4). | v5 : 18 des 35 cellules non re-sourcées en v4 l'ont été, dont le dentiste en Suisse ; 17 gardent leur valeur v3, signalées « non re-sourcée » (section 8). |
| Notes hors revenu : peu de statistiques par métier (DARES, DREES, SSMSI, DEPP en France ; Eurofound par grand groupe de professions ; OFS par branche ; rien sur les conditions de travail des dentistes, orthophonistes et kinésithérapeutes, sauf leurs heures). | Sur 558 notes : 9 sourcées, 239 mixtes (dont les 93 notes CA), 310 estimées (section 3, partie C) ; 3 notes modifiées par un chiffre, 18 tensions signalées (règles en 1.13). |

## 1. Entrées déclarées avant tout calcul

### 1.1 Calendrier et trajectoire de référence

| Entrée | Valeur |
|---|---|
| Début de formation | Rentrée 2027, à 25 ans, pour les cursus Parcoursup et les concours. L'année des 24 ans est l'emploi actuel. |
| Trajectoire de référence (emploi immédiat) | 18 000 € net à 24 ans (SMIC 2026 = 1 823,03 € brut, S43) puis montée linéaire à 21 000 € à 40 ans (médiane des employés 1 800 €/mois, S08), +0,5 %/an ensuite. |
| Revenus en formation | 0 € pour les études à temps plein ; stipendiums d'externat, salaire d'interne, apprentissage (53 % puis 100 % du SMIC, S43), traitements de stagiaire selon les règles de chaque voie. Frais de scolarité élevés comptés en négatif (ostéopathie, pilote, podologie). |
| Après l'entrée | Montée linéaire du revenu de début vers le médian à 40 ans, puis +0,5 %/an réel. |

### 1.2 Poids des versions 1 à 4 (opinion, pas consensus chiffré), remplacés en version 5 par la grille Eurofound (1.12)

| Critère | Poids v3 | Poids v2 | Poids v1 | Appui |
|---|---|---|---|---|
| Contrôle (autonomie de temps et de méthode) | 22 | 24 | 22 | Humphrey et al. 2007 (autonomie fortement liée à la satisfaction, ρ environ 0,48, valeur citée de mémoire, non revérifiée ici) ; modèle demande-latitude de Karasek |
| Charge et rythme | 19 | 21 | 20 | Karasek ; DARES sur l'intensité et les exigences émotionnelles (S58) |
| Relations et soutien | 15 | 16 | 15 | Soutien social du modèle de Karasek-Theorell |
| Sécurité et retour à l'emploi | 15 | 16 | 15 | Sverke et al. 2002 (insécurité et satisfaction, ρ environ -0,41, cité de mémoire, non revérifié) |
| Sens et utilité perçue | 6 | 7 | 13 | Humphrey et al. 2007 (significativité de la tâche) ; poids divisé par deux en v2, voir 1.8 |
| Revenu | 15 | 16 | 15 | Judge et al. 2010 : corrélation niveau de salaire et satisfaction r = 0,15 (vérifié, S57) |
| Lieu (télétravail) | 8 | 0 | 0 | Gajendran et Harrison 2007 : 46 études, effets faibles mais favorables sur l'autonomie perçue, le conflit travail-famille et la satisfaction, en partie via l'autonomie (S91) ; poids modéré car en partie redondant avec le contrôle, voir 1.10 |

### 1.3 Grilles de notation normatives (1 à 5)

| Critère | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|
| Contrôle | Fixe ses horaires et ses méthodes (libéral avec clientèle propre) | Choisit l'essentiel du temps ou de la méthode (libéral sous pression de la demande, cadre autonome, enseignant) | Méthode autonome dans des protocoles, horaires imposés mais prévisibles | Horaires imposés (roulements) et méthodes prescrites | Rythme dicté par la hiérarchie ou le flux, sans marge |
| Affectation géographique | Non notée depuis la v2 (hors de la définition « temps et méthode ») ; contrainte signalée pour certifiés, police, attachés issus des IRA, DGFiP, magistrats, ICNA, militaires | | | | |
| Charge | 5 moins le nombre de facteurs marqués, plancher 1 : F1 plus de 45 h/semaine ; F2 forte intensité ou exigence émotionnelle ou décisionnelle (soignants, médecins et assimilés, enseignants, cadres, police, secours, commerciaux) ; F3 nuits, week-ends ou astreintes réguliers ; F4 pénibilité physique ; F5 trajet d'au moins 1 h par sens ou découchés (frontaliers, routiers, pilotes) | | | | |
| Relations | Soutien fort et clientèle reconnaissante, peu de conflits | Bonnes relations, conflits ponctuels | Soutien présent mais tensions fréquentes ou isolement | Conflits fréquents avec le public ou faible soutien (barrière de langue comprise) | Environnement hostile |
| Sécurité | Statut protégé ou profession réglementée en pénurie structurelle (retour à l'emploi quasi certain) | Forte demande sans statut (v4 : la clause « expatriation avec intégration à faire » est retirée, c'est une étape d'entrée) | Marché moyen, cyclique, ou indépendant à demande stable | Revenus ou contrats volatils | Très précaire |
| Sens (utilité de la tâche elle-même, indépendante de l'employeur ; moins 1 si la DARES documente des conflits de valeurs fréquents) | Soin direct, enseignement, secours, justice | Utilité claire mais moins directe (paramédical technique, artisans de l'énergie, transport public, police) | Utilité indirecte (ingénierie, administration, numérique, comptabilité) | Utilité perçue faible (vente, immobilier, finance) | Perçu comme inutile |
| Lieu (depuis la v3 ; usage courant du métier, pas le maximum légal) | Lieu largement libre (indépendant qui choisit des missions à distance) | Télétravail régulier d'environ 2 à 3 jours par semaine | Environ 1 jour par semaine, ou part importante du travail faisable chez soi (préparation, rédaction), ou frontalier au Luxembourg (34 jours par an) | Télétravail rare, ou lieu fixe mais choisi par le travailleur (cabinet libéral, zone d'un artisan) | Présence physique sur un lieu imposé, sans télétravail |

### 1.4 Revenu

| Entrée | Valeur |
|---|---|
| Définition (v4) | Revenu net annuel d'un professionnel installé : médiane de la profession, tous âges, au temps de travail réel indiqué, sans décote pour l'entrée tardive du sujet. Net = après cotisations et contributions sociales (CSG et CRDS comprises en France), avant impôt sur le revenu (convention INSEE). Limite : l'impôt n'est pas déduit, ce qui favorise relativement les pays à impôt élevé (Allemagne, Luxembourg, Québec) et la fonction publique européenne. |
| Libéraux français (v4) | Revenus Insee (cotisations déduites, CSG et CRDS non déduites, S97) × 0,874 = 1 - 9,7 % × 1,3 (assiette = revenu + cotisations, environ 1,3 fois le revenu ; × 0,864 pour les artisans, cotisations plus lourdes). Bénéfices fiscaux DREES, CARMF, CARCDSF, CNBF, UNASA (CSG déductible déjà retirée) × 0,96. |
| Moyenne seule publiée (v4) | Non-salariés : médiane = moyenne × 0,85 (rapports publiés : ADA 2023, 185 360 / 218 710 = 0,85 ; OFS 2019, premier recours, 172 000 / 199 975 = 0,86). Grilles statutaires : médiane = moyenne (fonction publique de l'État 2024 : moyenne 3 018 €, S67 ; médiane relayée 3 044 €, S104). |
| Passage brut vers net | Indépendants suisses (v4) : revenu OFS net d'AVS et de 2e pilier moins la prime LAMal moyenne d'un adulte (449,20 CHF par mois en 2025, S112). Propriétaires américains (v4, ADA) : moins la cotisation des indépendants (15,3 % sur 92,35 % du revenu jusqu'à 176 100 USD, 2,9 % au-delà, 0,9 % au-delà de 200 000 USD) et 7 000 USD d'assurance santé individuelle (estimé). Suisse × 0,80 (AVS, AC, LPP, AANP et prime maladie LAMal, estimé) ; médecins suisses × 0,83 à 0,85 ; Luxembourg × 0,875 ; Allemagne × 0,78 ; Québec × 0,918 (RRQ, AE, RQAP ; la santé y est financée par l'impôt, donc net surestimé) ; libéraux français × 0,94 (CSG et CRDS non déductibles, estimé). Irlande : PRSI 4,2 % et USC, prélèvement comparable à la CSG, soit × 0,94 à 60 000 € et × 0,91 à 110 000 € brut (S85). États-Unis × 0,91 : FICA 7,65 % et part salariale d'une assurance santé individuelle, estimée à 1,5 % (seule la part familiale, 6 296 USD, a pu être lue dans l'enquête KFF 2024, S96) ; appliqué aussi au dentiste libéral, car la médiane BLS ne couvre que les salariés. |
| Change (valeur non ajustée) | Août à décembre 2025, Banque de France, référence BCE : 1 € = 0,933 CHF = 1,619 CAD = 1,16 USD (septembre 1,1732, octobre 1,1630, novembre 1,1560 ; S38). |
| Parité de pouvoir d'achat | Indices de niveau de prix Eurostat 2024, consommation des ménages, UE27 = 100 : France 111, Allemagne 109, Luxembourg 133, Irlande 138, Suisse 174 (S36). Canada 123 et États-Unis 147, estimés par le ratio OCDE des niveaux de prix 2024 (Canada 105, États-Unis 126, France 95, S37). Valeur PPA exprimée en euros au niveau de prix français. Change moyen 2024 de la BCE utilisé pour la cohérence avec les indices : 0,9526 CHF, 1,4821 CAD (valeurs connues avant cette analyse, non revérifiées ici), 1,0824 USD (S84). |
| Limites propres aux États-Unis | Ni l'impôt fédéral ni l'impôt d'État ne sont déduits (comme partout). Non comptés : l'absence de minimum fédéral de congés payés, les franchises d'assurance santé, la protection sociale plus faible. Seul l'écart de prix est corrigé : données BLS à transférabilité limitée. |
| Frontaliers | Dépense en France au change courant, avec un surcoût régional estimé (pas de série officielle) : Genevois français 10 %, nord lorrain 5 %. |
| P80 (v4) | Interpolation linéaire entre P75 et P90 quand ils sont publiés (BLS). Sinon loi log-normale : écart type tiré du rapport moyenne / médiane de la même source, ou celui des libéraux (rapport 0,85, soit P80 = 1,62 × médiane). Grilles statutaires sans dispersion publiée : 1,2 × médiane (amplitude de grille, estimé). Autres salariés : rapport P80 / médian de la v3 (estimé). |
| Cumul 24 à 45 ans | Somme des 22 revenus annuels nets de la trajectoire, en euros PPA, sans actualisation. Depuis la v4 : colonne informative, hors score (il dépend surtout de la durée des études). |
| Score revenu (v4) | Sur les valeurs ajustées en PPA uniquement : pour le médian et le P80 installés, 1 + 4 × (ln x - ln min) / (ln max - ln min), bornes du pool ; score revenu = moyenne des deux. Bornes v4 : médian 21 600 à 111 568 € (employé, médecin généraliste en Suisse) ; P80 25 700 à 183 613 € (employé, dentiste aux États-Unis). |

### 1.5 Agrégation, paliers, égalités, barrière

| Entrée | Valeur |
|---|---|
| Score interne | Moyenne pondérée des sept notes (revenu continu, autres entières). Seul le palier est affiché. |
| Paliers | S ≥ 4,2 ; A ≥ 3,6 ; B ≥ 3,0 ; C en dessous. Frontières arbitraires (fixées par la consigne). Astérisque = à moins de 0,1 d'une frontière. |
| Égalités (v4) | Deux triplets sont à égalité si leurs scores diffèrent de moins de 0,03 : c'est la moitié du plus petit pas de note (une note de sens vaut 0,06) et l'effet d'une erreur de 10 % sur les deux revenus. Groupes formés depuis le meilleur score : chaque groupe réunit les triplets à moins de 0,03 de son premier membre ; ils partagent le même rang (« 7= »). |
| Barrière (hors score, informative depuis la v4) | Colonnes affichées : âge d'entrée, formation et financement, sélectivité et p, années de revenu perdues, cumul 24-45 ans. Elle n'entre ni dans le score, ni dans le classement. |
| Probabilité p | Estimation personnelle pour un candidat moyen de 24 ans, ancrée sur les taux d'admission publiés quand ils existent (PASS 33,8 % en un an, IFSI 25 000 places pour 116 000 candidats, orthophonie 3,29 %, EPSO environ 3 %, ENM environ 10,5 %, CRFPA 25 à 35 %). |
| Élimination (v4) | Aucune : l'élimination de la v3 utilisait la barrière. Les 93 triplets sont classés ; la colonne « dominé par » signale, pour information, ceux qu'un autre triplet égale ou dépasse sur les sept critères. La frontière de Pareto et le classement en deux temps, fondés sur la barrière, sont retirés (versions précédentes dans l'historique du dépôt). |

### 1.6 Intelligence artificielle : deux scénarios bornés, poids de preuve faible

| Scénario | Hypothèse | Effet appliqué |
|---|---|---|
| IA faible | Complémentarité, pas d'effet mesurable sur l'emploi d'ici 45 ans | Aucun changement (scénario de base) |
| IA fort | Substitution partielle des tâches exposées (OIT 2025 : 1 emploi sur 4 exposé dans le monde, 34 % dans les pays riches, 3,3 % au gradient le plus élevé, surtout employés administratifs, S56) | Exposition moyenne : sécurité moins 1, revenus × 0,9. Exposition élevée : sécurité moins 2, revenus × 0,8. Fonctionnaires : choc de sécurité réduit d'un cran. |

Ces multiplicateurs sont des bornes de scénario, pas une prévision. L'exposition est classée faible, moyenne ou élevée par groupe de métiers (soins et métiers manuels faible ; ingénierie, enseignement, droit, administration publique, vente moyenne ; développement logiciel, comptabilité, actuariat, emplois administratifs élevée).

### 1.7 Règles d'accès réelles vérifiées à 24 ans

| Voie | Règle | Conséquence pour le sujet | Source |
|---|---|---|---|
| Médecine, dentaire, pharmacie, maïeutique, kiné | PASS et LAS supprimés à la rentrée 2027, remplacés par une « licence portail santé » sur Parcoursup ; une candidature en fin de L1, une seconde en fin de L2 ; places inchangées ; décret non publié au Journal officiel fin septembre 2026. Aucune limite d'âge trouvée. Règle actuelle : 2 candidatures, PASS 33,8 % d'admis en un an en 2024, LAS 19,5 %. | Entrée possible à 25 ans sous le nouveau régime, dont les modalités fines restent à confirmer. | S39, S40 |
| Vétérinaire | Voie post-bac réservée aux élèves passant le bac l'année du concours. Autres voies : L2 ou licence (58 places), BUT (46), BTS (52), deux tentatives. | Voie post-bac fermée ; voies bac+2 très étroites ; écoles de l'UE payantes possibles. | S51 |
| Infirmier | Parcoursup 2025 : 116 000 candidats, 25 000 places. Voie formation professionnelle continue avec 3 ans de cotisations (écrit et oral), quota de 25 à 33 % selon les sources ; Transition Pro et Régions financent parfois. | Les années d'emploi du sujet ouvrent la voie FPC. | S41, S42 |
| Orthophonie | 3,29 % d'admis en 2025, 1 025 places en 2026. | Très faible probabilité. | S42 |
| Apprentissage | 29 ans révolus à la signature ; dérogation jusqu'à 35 ans pour un diplôme supérieur enchaîné ; 100 % du SMIC à partir de 26 ans. | BUT puis école d'ingénieurs en apprentissage faisable jusqu'à 30 ans environ. | S43 |
| Enseignement | Concours à bac+3 depuis 2026, puis deux ans de master rémunérés (environ 1 400 puis 1 800 € net), engagement de 4 ans. | Titularisation vers 30 ans. | S44 |
| Contrôleur aérien ICNA | Moins de 26 ans au 1er janvier de l'année du concours ; épreuves de niveau CPGE scientifique. | Fenêtre 2027 et peut-être 2028 seulement, sans préparation possible à temps : p environ 1 %. | S45 |
| Avocat | Master 1 en droit, trois tentatives au CRFPA, 25 à 35 % de réussite. | Entrée vers 32 ans. | S46 |
| Magistrat | 271 places au premier concours 2025, environ 10,5 % de réussite ; limite d'âge non vérifiée. | Entrée vers 33 ans. | S52 |
| Fonction publique européenne | AD5 : licence, C1 et B2, 50 000 à 60 000 candidats pour 1 490 lauréats en 2026. Agents contractuels GF II-III : bac et 3 ans d'expérience, inscription continue. | AD hors de portée probable ; agent contractuel accessible sur le papier dès maintenant. | S47, S48 |
| Sous-officier (Terre) | Moins de 32 ans à la signature, bac. | Accessible. | S49 |
| Gardien de la paix | Formation de 12 mois rémunérée (1 570 à 1 617 € net) ; limite d'âge officielle non vérifiée. | Accessible. | S50 |
| Infirmier au Luxembourg | Diplôme français exempté de reconnaissance ; connaissances linguistiques « nécessaires », luxembourgeois non exigé à l'embauche. | Accès direct après l'IFSI. | S53 |
| Infirmier en Suisse | Reconnaissance par la Croix-Rouge suisse, plusieurs mois, mesures de compensation possibles. | Accès quelques mois après l'IFSI. | S61 |
| Infirmier au Québec | Arrangement de reconnaissance mutuelle : stage d'adaptation de 75 jours ; 500 h de pratique sur 4 ans si diplôme de plus de 4 ans ; immigration à obtenir. | Accès vers 29 ans. | S54 |
| Médecin en cabinet en Suisse | Trois ans d'activité dans un établissement suisse reconnu pour facturer à la LAMal. | Cabinet vers 38 ans. Règle connue avant cette analyse, non revérifiée ici. | |
| Pilote de ligne | Filière EPL P : 18 à 30 ans avec licence CPL ; condition d'âge EPL/S non vérifiée ; voie privée environ 100 k€. | Barrière de capital maximale. | |
| Résidence en Suisse | Ressortissant de l'UE : permis B de droit avec un contrat de travail d'au moins un an ou à durée indéterminée (accord sur la libre circulation, annexe I, art. 6). Diplôme dentaire français reconnu au titre de l'accord (règle connue avant cette analyse, non revérifiée ici). | Accès dès l'embauche. | S90 |
| Irlande | Libre circulation de l'UE, aucun permis. | Accès dès l'embauche ; anglais courant requis. | |
| États-Unis, métiers tech | Visa H-1B : tirage pondéré par niveau de salaire depuis le 27 février 2026 (projection USCIS : environ 15 % de chances au niveau 1, 31 % au niveau 2) ; depuis le 21 septembre 2025, 100 000 USD à payer par l'employeur pour un nouveau dossier d'un candidat hors des États-Unis. | Accès surtout par mutation interne dans un groupe international ; p estimé 3 %. | S88 |
| États-Unis, dentiste | Diplôme étranger : programme « advanced standing » de 2 à 3 ans dans une école accréditée (28 mois et environ 250 000 USD de frais à Ohio State), examen INBDE, examen clinique et licence d'État, puis un visa. | Entrée vers 34 ans, capital maximal ; p estimé 2 %. | S86 |
| États-Unis, orthophoniste | Formation évaluée par l'ASHA comme équivalente à un master, examen Praxis, 36 semaines (1 260 h) de clinical fellowship, licence d'État, puis un visa. | Entrée vers 33 ans, exercice en anglais ; p estimé 2 %. | S89 |

### 1.8 Changements de la version 2 (12 octobre 2026), déclarés avant recalcul

| Changement | Justification | Triplets touchés |
|---|---|---|
| Poids du sens 13 vers 7 ; 6 points redistribués au prorata (24/21/16/16/7/16) | Au niveau d'un triplet, seule l'utilité de la tâche est prévisible ; l'adhésion à la mission dépend de l'employeur, de l'équipe et du projet. Les notes de sens de la v1 (5 pour tout le soin, 3 pour tout le numérique) surestimaient l'écart prévisible entre métiers. Le sens reste important pour le bien-être : seul son poids discriminant est réduit. | Tous |
| Retrait du malus « affectation géographique imposée » en contrôle | Hors de la définition donnée (autonomie sur le temps et la méthode). | T57, T58, T60, T61, T62, T63, T66, T71 |
| Sens moins 1 pour les soignants hospitaliers salariés | Conflits de valeurs fréquents documentés par la DARES pour aides-soignants, infirmiers et sages-femmes (S58). | T08, T12, T14, T21 |
| Non changé : relations | Même faiblesse en théorie (dépend de l'équipe), mais les notes y varient peu (2 à 4) : effet faible sur le classement. | |
| Non changé : contrôle, charge, sécurité, revenu | Surtout déterminés par le statut, le temps de travail réglementé et le marché, donc prévisibles au niveau du triplet. | |

### 1.9 Changements de la version 2.1 (12 octobre 2026)

| Changement | Justification |
|---|---|
| T41 à T43 précisés en « ingénieur méthodes-industrialisation » | « Ingénieur » n'est pas un métier précis. Leur revenu reste la médiane IESF toutes spécialités, signalée comme proxy. |
| Ajout de 6 triplets IT précis : T80 ingénieur cloud et DevOps salarié (France), T81 le même en freelance, T82 le même frontalier en Suisse, T83 ingénieur cybersécurité hors SOC, T84 analyste SOC, T85 data engineer | Le pool ne contenait que « développeur » et « technicien réseaux ». Notes avec les mêmes grilles : astreintes fréquentes en exploitation cloud (facteur F3, estimé), travail posté 24 h/24 en SOC, demande documentée en cybersécurité (offres +49 % de 2019 à 2024 selon l'observatoire de l'ANSSI, 25 000 postes à pourvoir d'ici 2028 selon l'OPIIEC, S78) donc sécurité 4, mission de protection donc sens 4 comme la police. Revenus issus de sources privées (Robert Half, Free-Work, sites salariaux), signalés comme tels. |

### 1.10 Changements de la version 3 (13 octobre 2026), déclarés avant recalcul

| Changement | Justification | Triplets touchés |
|---|---|---|
| Nouveau critère « lieu » (télétravail), poids 8 ; les six poids v2 réduits au prorata (22/19/15/15/6/15) | Le télétravail n'était capté nulle part : le contrôle porte sur le temps et la méthode. Méta-analyse de Gajendran et Harrison 2007 : effets faibles mais favorables, en partie via l'autonomie perçue ; au-delà de 2,5 jours par semaine, relations avec les collègues dégradées (S91). En 2023, 26 % des salariés télétravaillent au moins occasionnellement, et 91 % des ingénieurs informatiques selon la DARES relayée par la presse (S92). Poids modéré parce que le critère recoupe en partie le contrôle. | Tous |
| Notes de lieu fixées par la grille 1.3 et par les règles en vigueur | Fonction publique française : 3 jours de télétravail par semaine au plus (S94). Institutions de l'UE : de 20 % à 60 % du temps avec accord du supérieur (S95). Frontaliers en Suisse : 40 % du temps par an sans changement d'imposition depuis 2023, prolongation au-delà de 2025 non vérifiée ; frontaliers au Luxembourg : 34 jours par an (S93). | Tous |
| 8 nouveaux triplets à l'étranger : T86 ingénieur cloud et DevOps résident en Suisse, T87 le même en Irlande, T88 aux États-Unis ; T89 ingénieur cybersécurité résident en Suisse, T90 le même aux États-Unis ; T91 chirurgien-dentiste libéral résident en Suisse, T92 le même aux États-Unis ; T93 orthophoniste salarié aux États-Unis | La consigne vise tous les pays accessibles à un Français. Ajout des métiers du haut du classement et des métiers tech cités, dans les pays où ils paient le plus (Suisse, États-Unis) et dans le principal pôle tech anglophone de l'UE (Irlande). Mêmes grilles qu'en France. | T86 à T93 |
| Relations moins 1 quand le travail se fait dans une autre langue que le français | Règle déjà appliquée à l'Allemagne (T27, T31, T38). | T87, T88, T90, T92, T93 |
| Sécurité aux États-Unis et en Irlande : 3 pour le cloud (licenciement à volonté aux États-Unis, suppressions de postes dans la tech) ; 4 pour la cybersécurité aux États-Unis (emploi projeté +29 % de 2024 à 2034, contre +3,1 % tous métiers, S87) ; 5 pour les professions de santé réglementées | Mêmes grilles que la France. | T87, T88, T90, T92, T93 |
| Revenu du dentiste aux États-Unis | La médiane BLS (179 210 USD) ne couvre que les dentistes salariés : proxy prudent pour un libéral, converti comme un salaire. | T92 |

### 1.11 Changements de la version 4 (28 octobre 2026), déclarés avant recalcul

| Changement | Justification | Triplets touchés |
|---|---|---|
| Objectif : qualité de vie professionnelle une fois installé ; la barrière d'entrée n'est plus qu'une colonne informative | Consigne du 28 octobre. | Tous |
| Revenu : médian et P80 d'un professionnel installé, en PPA ; cumul 24-45 ans retiré du score | La v3 mesurait le revenu du sujet à 40 ans, décoté pour son entrée tardive, et le cumul 24-45 ans, qui dépend surtout de la durée des études : deux barrières cachées dans le score. | Tous |
| Chaque cellule revenu re-sourcée une par une, avec sa conversion, son temps de travail réel et un niveau de fiabilité | Consigne du 28 octobre. Sources visées : DREES, CARMF, CARCDSF, Insee, DEPP pour la France ; OFS, FMH pour la Suisse ; BLS, ADA pour les États-Unis. Aucune statistique de la SSO sur le revenu des dentistes suisses n'a été trouvée. | Tous |
| Sécurité : clause « expatriation avec intégration à faire » retirée de la note 4 | L'intégration est une étape d'entrée. Infirmiers en Allemagne et au Québec : profession réglementée en pénurie, donc 5 comme en Suisse et au Luxembourg. | T27, T28 |
| Égalité sous un écart de 0,03 (section 1.5) | Un écart plus petit ne peut venir que du revenu, dont l'incertitude est d'au moins 10 % : départager serait artificiel. | Tous |
| Plus d'élimination, de frontière de Pareto ni de classement en deux temps | Ils utilisaient la barrière. | Tous |
| Poids inchangés : contrôle 22, charge 19, relations 15, sécurité 15, revenu 15, lieu 8, sens 6 | Consigne. Le revenu est 3e à égalité avec les relations et la sécurité ; le dernier critère est le sens. | Aucun |

### 1.12 Changements de la version 5 (28 octobre 2026), déclarés avant recalcul

| Changement | Justification | Triplets touchés |
|---|---|---|
| Critères : les 7 dimensions de qualité de l'emploi d'Eurofound (environnement physique EP, intensité du travail IT, qualité du temps de travail QT, environnement social ES, compétences et autonomie CA, perspectives et sécurité PS, revenu RE), à poids égaux (1/7 chacune). La pondération personnelle est supprimée. | Consigne du 28 octobre. Eurofound a retenu ces dimensions pour leur effet démontré sur la santé et le bien-être des travailleurs (S116). Des poids égaux restent un choix : d'où le test de robustesse. | Tous |
| EP : grille par groupe de métiers (5 bureau ou cabinet ; 4 contraintes légères ; 3 postures contraignantes ou risques biologiques, chimiques, rayonnements ; 2 manutention de personnes ou de charges, postures pénibles ; 1 cumul fort) | Reprend et gradue le facteur F4 (pénibilité) de l'ancienne charge. | Tous |
| IT : grille par groupe de métiers (5 rythme libre ; 4 pression modérée ; 3 forte exigence de délais, d'objectifs ou de patients ; 2 urgence, vigilance de sécurité ou tension forte et fréquente ; 1 cumul extrême) | Reprend et gradue le facteur F2 (intensité, exigences émotionnelles). | Tous |
| QT = 5 - F1 (plus de 45 h) - F3 (nuits, week-ends, astreintes) - H (horaires imposés, contrôle v4 de 3 ou moins), plancher 1 | Composantes de l'indice Eurofound : durée, horaires atypiques, aménagement des horaires. | Tous |
| ES = relations v4 ; PS = sécurité v4, sauf contradiction avec un chiffre de statut S (1.13) | Même contenu ; les perspectives de carrière ne sont pas notées à part (limite). | Tous |
| CA = moyenne du contrôle v4 (latitude de décision) et du niveau de compétence CITP-08 de l'OIT (niveau 4 : 5 ; 3 : 3,67 ; 2 : 2,33 ; 1 : 1) | Eurofound réunit la latitude de décision et l'usage des compétences ; le niveau CITP-08 est une classification publiée (S115). | Tous |
| Facteurs F1 à F5 explicités pour chaque triplet (section 3, tableau de conversion) | 5 moins leur nombre redonne les 93 notes de charge v4 (contrôle automatique) : la conversion est traçable. | Tous |
| Sortis du score : sens, lieu (télétravail), trajet (F5) | Absents des 7 indices d'Eurofound. Ils restent visibles dans le tableau de conversion. | Tous |
| RE : revenu en équivalent temps plein, ajusté en PPA ; quotité = heures réelles / 35, plafonnée à 1 | Consigne. 35 h = seuil du temps plein retenu par le BLS et durée légale française. Source déjà en équivalent temps plein (EQTP, temps complet, salaire horaire × durée à temps plein) : quotité 1. Heures non trouvées : quotité 1 et cellule signalée. | Tous |
| Robustesse : 8 configurations (poids égaux, puis chacune des 7 dimensions doublée) ; haut du classement = 10 premiers, rangs partagés compris ; classement final = triplets présents dans le haut du classement dans toutes les configurations | Consigne (au moins 3 variantes). Doubler chaque dimension à tour de rôle évite de choisir celles à favoriser ; les 3 variantes citées (revenu, autonomie, sécurité) en font partie. | Tous |
| Paliers calculés sur le score à poids égaux ; égalité sous un écart de 0,03 | Inchangé : 0,03 correspond toujours à l'effet d'une erreur de 10 % sur le revenu. | Tous |

### 1.13 Ancrage des notes hors revenu (version 5, déclaré avant recalcul)

| Règle | Contenu |
|---|---|
| Statut S, sourcée | Chiffre d'une source officielle, chiffré (rapport à la moyenne de tous les actifs, ou bande ci-dessous), pour le métier lui-même ou le métier dans son type d'établissement (par exemple les infirmiers à l'hôpital), dans le pays du triplet. |
| Statut M, mixte | Chiffre pour un groupe plus large (catégorie socioprofessionnelle, grand groupe CITP, secteur), pour un autre pays ou un autre statut, sans ampleur publiée (rang, « plus exposé que »), issu d'une enquête non officielle (syndicat, échantillon de volontaires), ou ne couvrant qu'une partie de la dimension. QT et CA sont au mieux M : la composante « horaires imposés » de QT et la latitude de décision de CA restent estimées. |
| Statut E, estimée | Aucun chiffre trouvé : note de la grille normative (1.3, 1.12). |
| Conversion EP | Part des salariés déclarant au moins 3 contraintes physiques (DARES, enquête Conditions de travail 2019 ; ensemble 35 %) : moins de 10 % = 5 ; 10 à 29 % = 4 ; 30 à 49 % = 3 ; 50 à 64 % = 2 ; 65 % ou plus = 1. Bandes centrées sur la moyenne nationale, limites arbitraires. Pour un chiffre de groupe, seul le côté de la note est vérifié (1 ou 2, 3, 4 ou 5). |
| Conversion des autres indicateurs | Rapport r du chiffre du métier à celui de l'ensemble des actifs. Indicateur défavorable (exposition, agression, crainte pour l'emploi) : r ≥ 1,5 donne 1 ou 2 ; r ≤ 2/3 donne 4 ou 5 ; sinon 3. Indicateur favorable (créations d'emplois) : l'inverse. Indice Eurofound sur 100 : 5 points ou plus sous la moyenne de l'UE donnent 1 ou 2. Indicateur sans ampleur : seule une note du côté opposé est en tension (4 ou 5 pour un métier « plus exposé »). |
| Conversion QT | F1 si la durée moyenne publiée dépasse 45 h ou si au moins 40 % des membres du métier font 48 h ou plus. F3 si au moins 40 % travaillent la nuit ou le dimanche au moins une fois par mois (moyennes nationales : nuit 10 %, dimanche 23 %, S140, S151). |
| Conversion PS | Grille 1.3 appliquée au chiffre : métier en tension ou forte création d'emplois = forte demande = 4 pour un salarié sans statut, 3 pour un indépendant (« indépendant à demande stable ») ; profession réglementée en pénurie = 5. |
| Contradiction | Un chiffre de statut S qui contredit la note la remplace par la valeur compatible la plus proche (liste en section 3). Un chiffre de statut M qui la contredit est signalé « tension » sans changer la note : une moyenne de groupe ou d'un autre pays ne fixe pas la note d'un métier précis. L'effet des tensions est montré à part (section 4). |
| Groupes exclus | Trop hétérogènes pour un métier précis : l'ensemble des professions intermédiaires, le grand groupe CITP 5 (services et vente), la branche suisse « santé et action sociale ». |
| Non appliqué | Écarts entre la Suisse et l'Europe de l'enquête EWCTS 2021 (cadence plus élevée, moins de contraintes physiques, plus de latitude en Suisse) : moyennes nationales sans détail par métier, et le SECO juge l'enquête insuffisante pour une analyse détaillée (S149). Résultats Eurofound par statut (employeurs et indépendants stables au-dessus des indépendants dépendants, S148) : qualité globale, pas une dimension. |
| Recherche | 40 recherches sur les conditions de travail par métier (DARES, DREES, Insee, SSMSI, DEPP, SDES, DGAFP, Eurofound, OFS, SECO), puis 6 sur les heures, la demande et l'exposition des métiers du haut du classement. Rien trouvé sur les conditions de travail des dentistes (sauf une enquête sur les orthodontistes), des orthophonistes (sauf la saturation des agendas) et des kinésithérapeutes (sauf leurs heures). |

## 2. Pool (93 triplets)

| ID | Triplet | ID | Triplet |
|---|---|---|---|
| T01 | Médecin généraliste × libéral × France | T48 | Électricien × artisan × France |
| T02 | Médecin généraliste × salarié (centre de santé) × France | T49 | Électricien × salarié × Suisse (frontalier) |
| T03 | Médecin spécialiste (rang médian) × libéral × France | T50 | Électricien × salarié × Canada (Québec) |
| T04 | Praticien hospitalier × statut PH (public) × France | T51 | Plombier-chauffagiste × artisan × France |
| T05 | Chirurgien-dentiste × libéral × France | T52 | Frigoriste (CVC) × salarié × France |
| T06 | Pharmacien adjoint × salarié × France | T53 | Conducteur de train × salarié (SNCF) × France |
| T07 | Pharmacien titulaire × indépendant × France | T54 | Conducteur de train × salarié × Suisse (résident) |
| T08 | Sage-femme × fonctionnaire FPH × France | T55 | Conducteur poids lourd × salarié × France |
| T09 | Sage-femme × libéral × France | T56 | Professeur des écoles × fonctionnaire × France |
| T10 | Masseur-kinésithérapeute × libéral × France | T57 | Professeur certifié × fonctionnaire × France |
| T11 | Masseur-kinésithérapeute × fonctionnaire FPH × France | T58 | Gardien de la paix × fonctionnaire × France |
| T12 | Infirmier × fonctionnaire FPH × France | T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France |
| T13 | Infirmier × libéral × France | T60 | Attaché d'administration × fonctionnaire × France |
| T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | T61 | Inspecteur des finances publiques × fonctionnaire × France |
| T15 | Orthophoniste × libéral × France | T62 | Contrôleur des finances publiques × fonctionnaire × France |
| T16 | Orthoptiste × salarié × France | T63 | Contrôleur aérien (ICNA) × fonctionnaire × France |
| T17 | Manipulateur radio (MERM) × fonctionnaire FPH × France | T64 | Administrateur UE (AD) × fonctionnaire européen × Luxembourg (résident) |
| T18 | Audioprothésiste × salarié × France | T65 | Agent contractuel UE (GF II-III) × contractuel × Luxembourg (frontalier) |
| T19 | Vétérinaire × libéral × France | T66 | Sous-officier × militaire × France |
| T20 | Psychologue × contractuel FPH × France | T67 | Avocat × libéral × France |
| T21 | Aide-soignant × fonctionnaire FPH × France | T68 | Expert-comptable × libéral × France |
| T22 | Ostéopathe × libéral × France | T69 | Comptable × salarié × France |
| T23 | Infirmier × salarié × Suisse (résident) | T70 | Comptable × salarié × Luxembourg (frontalier) |
| T24 | Infirmier × salarié × Suisse (frontalier) | T71 | Magistrat × fonctionnaire × France |
| T25 | Infirmier × salarié × Luxembourg (frontalier) | T76 | Pédicure-podologue × libéral × France |
| T26 | Infirmier × salarié × Luxembourg (résident) | T77 | Ergothérapeute × fonctionnaire FPH × France |
| T27 | Infirmier × salarié × Allemagne | T78 | Diététicien × libéral × France |
| T28 | Infirmier × salarié × Canada (Québec) | T79 | Opticien × salarié × France |
| T29 | Médecin × salarié (hôpital) × Suisse (résident) | T80 | Ingénieur cloud et DevOps × salarié × France |
| T30 | Médecin généraliste × indépendant × Suisse (résident) | T81 | Ingénieur cloud et DevOps × indépendant (freelance) × France |
| T31 | Médecin × salarié (hôpital) × Allemagne | T82 | Ingénieur cloud et DevOps × salarié × Suisse (frontalier) |
| T32 | Médecin de famille × libéral (RAMQ) × Canada (Québec) | T83 | Ingénieur cybersécurité (hors SOC) × salarié × France |
| T33 | Aide-soignant (ASSC) × salarié × Suisse (frontalier) | T84 | Analyste SOC (cybersécurité) × salarié × France |
| T34 | Masseur-kinésithérapeute × salarié × Suisse (frontalier) | T85 | Data engineer × salarié × France |
| T35 | Développeur × salarié × France | T86 | Ingénieur cloud et DevOps × salarié × Suisse (résident) |
| T36 | Développeur × indépendant (freelance) × France | T87 | Ingénieur cloud et DevOps × salarié × Irlande |
| T37 | Développeur × salarié × Suisse (frontalier) | T88 | Ingénieur cloud et DevOps × salarié × États-Unis |
| T38 | Développeur × salarié × Allemagne | T89 | Ingénieur cybersécurité (hors SOC) × salarié × Suisse (résident) |
| T39 | Développeur × salarié × Luxembourg (frontalier) | T90 | Ingénieur cybersécurité (hors SOC) × salarié × États-Unis |
| T40 | Développeur × salarié × Canada (Québec) | T91 | Chirurgien-dentiste × libéral × Suisse (résident) |
| T41 | Ingénieur méthodes-industrialisation × salarié × France | T92 | Chirurgien-dentiste × libéral × États-Unis |
| T42 | Ingénieur méthodes-industrialisation × salarié × Suisse (frontalier) | T93 | Orthophoniste × salarié × États-Unis |
| T43 | Ingénieur méthodes-industrialisation × salarié × Allemagne | T72 | Commercial B2B × salarié × France |
| T44 | Technicien de maintenance industrielle × salarié × France | T73 | Agent immobilier × indépendant (mandataire) × France |
| T45 | Technicien réseaux et cybersécurité × salarié × France | T74 | Pilote de ligne × salarié × France |
| T46 | Actuaire × salarié × France | T75 | Employé commerce ou accueil (référence) × salarié × France |
| T47 | Électricien × salarié × France |  |  |

## 3. Classement v5 (93 triplets, grille Eurofound à poids égaux)

Lecture des colonnes : EP environnement physique, IT intensité du travail, QT qualité du temps de travail, ES environnement social, CA compétences et autonomie, PS perspectives et sécurité, RE revenu ; notes de 1 (mauvais) à 5 (bon), poids égaux. CA et RE sont des notes continues (moyenne ou échelle logarithmique), les autres sont entières. Palier : S ≥ 4,2, A ≥ 3,6, B ≥ 3,0, C en dessous ; * = à moins de 0,1 d'une frontière. « 7= » : rang partagé (écart inférieur à 0,03). « X / Y k€ » : revenu net annuel en milliers d'euros, X au change 2025 sans ajustement, Y en parité de pouvoir d'achat ; le score utilise Y en équivalent temps plein.

### Classement v5, partie A : notes des 7 dimensions Eurofound, puis palier

| Rang | ID | Triplet | EP | IT | QT | ES | CA | PS | RE | Palier | Top 10 (sur 8 configurations) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | T30 | Médecin généraliste × indépendant × Suisse (résident) | 4 | 3 | 5 | 4 | 4,5 | 5 | 5,0 | S | 8 |
| 2= | T05 | Chirurgien-dentiste × libéral × France | 3 | 3 | 5 | 4 | 5 | 5 | 4,6 | S* | 7 |
| 2= | T91 | Chirurgien-dentiste × libéral × Suisse (résident) | 3 | 3 | 5 | 4 | 5 | 5 | 4,5 | S* | 7 |
| 2= | T15 | Orthophoniste × libéral × France | 5 | 4 | 5 | 4 | 5 | 5 | 1,5 | S* | 7 |
| 5= | T92 | Chirurgien-dentiste × libéral × États-Unis | 3 | 3 | 5 | 3 | 5 | 5 | 4,9 | A* | 6 |
| 5= | T89 | Ingénieur cybersécurité (hors SOC) × salarié × Suisse (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,3 | A* | 8 |
| 5= | T01 | Médecin généraliste × libéral × France | 4 | 3 | 4 | 4 | 4,5 | 5 | 4,3 | A* | 6 |
| 8= | T37 | Développeur × salarié × Suisse (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 3 | 4,2 | A | 6 |
| 8= | T82 | Ingénieur cloud et DevOps × salarié × Suisse (frontalier) | 5 | 3 | 4 | 4 | 4,5 | 4 | 4,1 | A | 5 |
| 8= | T03 | Médecin spécialiste (rang médian) × libéral × France | 4 | 3 | 4 | 4 | 4,5 | 5 | 4,1 | A | 5 |
| 8= | T46 | Actuaire × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,1 | A | 5 |
| 8= | T90 | Ingénieur cybersécurité (hors SOC) × salarié × États-Unis | 5 | 3 | 5 | 3 | 4,5 | 4 | 4,1 | A | 5 |
| 8= | T83 | Ingénieur cybersécurité (hors SOC) × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,0 | A | 5 |
| 14= | T09 | Sage-femme × libéral × France | 4 | 3 | 5 | 4 | 5 | 5 | 2,4 | A | 3 |
| 14= | T93 | Orthophoniste × salarié × États-Unis | 5 | 4 | 4 | 3 | 4 | 5 | 3,4 | A | 3 |
| 16= | T85 | Data engineer × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,5 | A | 1 |
| 16= | T64 | Administrateur UE (AD) × fonctionnaire européen × Luxembourg (résident) | 5 | 3 | 4 | 3 | 4 | 5 | 4,0 | A | 3 |
| 16= | T39 | Développeur × salarié × Luxembourg (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 3 | 3,5 | A | 1 |
| 16= | T71 | Magistrat × fonctionnaire × France | 5 | 3 | 4 | 3 | 4,5 | 5 | 3,4 | A | 2 |
| 16= | T16 | Orthoptiste × salarié × France | 5 | 4 | 4 | 4 | 4 | 5 | 1,8 | A | 3 |
| 21= | T35 | Développeur × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,3 | A | 1 |
| 21= | T10 | Masseur-kinésithérapeute × libéral × France | 2 | 4 | 5 | 4 | 5 | 5 | 2,8 | A | 2 |
| 21= | T86 | Ingénieur cloud et DevOps × salarié × Suisse (résident) | 5 | 3 | 4 | 4 | 4,5 | 4 | 3,3 | A | 1 |
| 21= | T81 | Ingénieur cloud et DevOps × indépendant (freelance) × France | 5 | 3 | 5 | 3 | 5 | 3 | 3,7 | A | 0 |
| 25= | T42 | Ingénieur méthodes-industrialisation × salarié × Suisse (frontalier) | 4 | 3 | 5 | 4 | 4,5 | 3 | 4,1 | A | 0 |
| 25= | T68 | Expert-comptable × libéral × France | 5 | 3 | 4 | 3 | 4,5 | 4 | 4,1 | A | 0 |
| 25= | T41 | Ingénieur méthodes-industrialisation × salarié × France | 4 | 3 | 5 | 4 | 4,5 | 4 | 3,1 | A | 0 |
| 25= | T40 | Développeur × salarié × Canada (Québec) | 5 | 3 | 5 | 4 | 4,5 | 3 | 2,9 | A | 0 |
| 29= | T43 | Ingénieur méthodes-industrialisation × salarié × Allemagne | 4 | 3 | 5 | 3 | 4,5 | 4 | 3,8 | A | 0 |
| 29= | T02 | Médecin généraliste × salarié (centre de santé) × France | 4 | 3 | 4 | 4 | 4 | 5 | 3,2 | A | 0 |
| 29= | T76 | Pédicure-podologue × libéral × France | 3 | 4 | 5 | 4 | 5 | 4 | 2,1 | A | 0 |
| 29= | T80 | Ingénieur cloud et DevOps × salarié × France | 5 | 3 | 4 | 4 | 4,5 | 4 | 2,6 | A | 0 |
| 33= | T38 | Développeur × salarié × Allemagne | 5 | 3 | 5 | 3 | 4,5 | 3 | 3,3 | A | 0 |
| 33= | T77 | Ergothérapeute × fonctionnaire FPH × France | 4 | 4 | 4 | 4 | 4 | 5 | 1,7 | A | 0 |
| 33= | T56 | Professeur des écoles × fonctionnaire × France | 4 | 3 | 5 | 3 | 4,5 | 5 | 2,2 | A | 0 |
| 33= | T88 | Ingénieur cloud et DevOps × salarié × États-Unis | 5 | 3 | 4 | 3 | 4,5 | 3 | 4,1 | A | 0 |
| 37= | T34 | Masseur-kinésithérapeute × salarié × Suisse (frontalier) | 2 | 4 | 4 | 4 | 4 | 5 | 3,6 | A | 0 |
| 37= | T60 | Attaché d'administration × fonctionnaire × France | 5 | 3 | 4 | 3 | 4 | 5 | 2,5 | A | 0 |
| 37= | T61 | Inspecteur des finances publiques × fonctionnaire × France | 5 | 3 | 4 | 3 | 4 | 5 | 2,5 | A | 0 |
| 40= | T36 | Développeur × indépendant (freelance) × France | 5 | 3 | 5 | 3 | 5 | 2 | 3,3 | A | 0 |
| 40= | T62 | Contrôleur des finances publiques × fonctionnaire × France | 5 | 4 | 4 | 3 | 3,3 | 5 | 2,0 | A | 0 |
| 40= | T20 | Psychologue × contractuel FPH × France | 5 | 3 | 5 | 4 | 4,5 | 3 | 1,8 | A | 0 |
| 40= | T63 | Contrôleur aérien (ICNA) × fonctionnaire × France | 5 | 2 | 3 | 4 | 2,8 | 5 | 4,3 | A | 0 |
| 44= | T78 | Diététicien × libéral × France | 5 | 4 | 5 | 4 | 4,5 | 2 | 1,4 | A | 0 |
| 44= | T32 | Médecin de famille × libéral (RAMQ) × Canada (Québec) | 4 | 3 | 2 | 3 | 4 | 5 | 4,9 | A* | 0 |
| 44= | T57 | Professeur certifié × fonctionnaire × France | 4 | 3 | 5 | 2 | 4,5 | 5 | 2,4 | A* | 0 |
| 44= | T87 | Ingénieur cloud et DevOps × salarié × Irlande | 5 | 3 | 4 | 3 | 4,5 | 3 | 3,4 | A* | 0 |
| 48= | T70 | Comptable × salarié × Luxembourg (frontalier) | 5 | 4 | 4 | 3 | 3,3 | 3 | 3,0 | A* | 0 |
| 48= | T18 | Audioprothésiste × salarié × France | 4 | 4 | 3 | 4 | 4 | 4 | 2,2 | A* | 0 |
| 50= | T11 | Masseur-kinésithérapeute × fonctionnaire FPH × France | 2 | 4 | 4 | 4 | 4 | 5 | 1,9 | B* | 0 |
| 50= | T67 | Avocat × libéral × France | 5 | 3 | 3 | 3 | 4 | 3 | 3,7 | B* | 0 |
| 52= | T65 | Agent contractuel UE (GF II-III) × contractuel × Luxembourg (frontalier) | 5 | 4 | 4 | 3 | 2,8 | 3 | 2,8 | B* | 0 |
| 52= | T13 | Infirmier × libéral × France | 2 | 3 | 3 | 4 | 4,5 | 5 | 3,1 | B* | 0 |
| 54= | T72 | Commercial B2B × salarié × France | 4 | 3 | 5 | 3 | 3,8 | 3 | 2,5 | B | 0 |
| 54= | T22 | Ostéopathe × libéral × France | 3 | 4 | 5 | 4 | 5 | 2 | 1,2 | B | 0 |
| 56= | T69 | Comptable × salarié × France | 5 | 4 | 4 | 3 | 3,3 | 3 | 1,7 | B | 0 |
| 56= | T19 | Vétérinaire × libéral × France | 2 | 3 | 3 | 3 | 4,5 | 5 | 3,5 | B | 0 |
| 58= | T06 | Pharmacien adjoint × salarié × France | 4 | 3 | 3 | 3 | 3,5 | 5 | 2,3 | B | 0 |
| 58= | T29 | Médecin × salarié (hôpital) × Suisse (résident) | 3 | 2 | 2 | 3 | 4 | 5 | 4,7 | B | 0 |
| 60 | T45 | Technicien réseaux et cybersécurité × salarié × France | 4 | 4 | 3 | 3 | 3,3 | 4 | 2,1 | B | 0 |
| 61= | T74 | Pilote de ligne × salarié × France | 4 | 3 | 3 | 3 | 2,8 | 3 | 4,4 | B | 0 |
| 61= | T04 | Praticien hospitalier × statut PH (public) × France | 3 | 2 | 2 | 3 | 4 | 5 | 4,0 | B | 0 |
| 63 | T84 | Analyste SOC (cybersécurité) × salarié × France | 5 | 2 | 3 | 3 | 3,5 | 4 | 2,2 | B | 0 |
| 64= | T31 | Médecin × salarié (hôpital) × Allemagne | 3 | 2 | 2 | 2 | 4 | 5 | 4,5 | B | 0 |
| 64= | T07 | Pharmacien titulaire × indépendant × France | 4 | 3 | 2 | 3 | 4 | 3 | 3,5 | B | 0 |
| 64= | T08 | Sage-femme × fonctionnaire FPH × France | 3 | 2 | 3 | 3 | 4 | 5 | 2,5 | B | 0 |
| 64= | T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | 3 | 2 | 3 | 3 | 4 | 5 | 2,5 | B | 0 |
| 64= | T79 | Opticien × salarié × France | 4 | 4 | 3 | 3 | 2,8 | 4 | 1,6 | B | 0 |
| 69= | T24 | Infirmier × salarié × Suisse (frontalier) | 2 | 2 | 3 | 3 | 3,5 | 5 | 3,8 | B | 0 |
| 69= | T50 | Électricien × salarié × Canada (Québec) | 2 | 4 | 4 | 3 | 2,7 | 4 | 2,6 | B | 0 |
| 69= | T25 | Infirmier × salarié × Luxembourg (frontalier) | 2 | 2 | 3 | 3 | 3,5 | 5 | 3,7 | B | 0 |
| 72= | T54 | Conducteur de train × salarié × Suisse (résident) | 4 | 3 | 3 | 3 | 2,2 | 4 | 2,9 | B | 0 |
| 72= | T26 | Infirmier × salarié × Luxembourg (résident) | 2 | 2 | 3 | 3 | 3,5 | 5 | 3,4 | B | 0 |
| 72= | T49 | Électricien × salarié × Suisse (frontalier) | 2 | 4 | 4 | 3 | 2,7 | 3 | 3,2 | B | 0 |
| 72= | T17 | Manipulateur radio (MERM) × fonctionnaire FPH × France | 3 | 3 | 3 | 3 | 2,8 | 5 | 2,0 | B | 0 |
| 76= | T53 | Conducteur de train × salarié (SNCF) × France | 4 | 3 | 3 | 3 | 2,2 | 4 | 2,3 | B* | 0 |
| 76= | T23 | Infirmier × salarié × Suisse (résident) | 2 | 2 | 3 | 3 | 3,5 | 5 | 2,9 | B* | 0 |
| 78= | T47 | Électricien × salarié × France | 2 | 4 | 4 | 3 | 2,7 | 4 | 1,5 | B* | 0 |
| 78= | T28 | Infirmier × salarié × Canada (Québec) | 2 | 2 | 3 | 3 | 3,5 | 5 | 2,6 | B* | 0 |
| 80= | T12 | Infirmier × fonctionnaire FPH × France | 2 | 2 | 3 | 3 | 3,5 | 5 | 2,0 | C* | 0 |
| 80= | T52 | Frigoriste (CVC) × salarié × France | 2 | 4 | 3 | 3 | 2,7 | 4 | 1,8 | C* | 0 |
| 82= | T73 | Agent immobilier × indépendant (mandataire) × France | 4 | 3 | 4 | 3 | 3,8 | 1 | 1,4 | C | 0 |
| 82= | T27 | Infirmier × salarié × Allemagne | 2 | 2 | 3 | 2 | 3,5 | 5 | 2,6 | C | 0 |
| 82= | T66 | Sous-officier × militaire × France | 2 | 3 | 3 | 4 | 2,2 | 4 | 1,9 | C | 0 |
| 85= | T48 | Électricien × artisan × France | 2 | 3 | 4 | 3 | 3,2 | 3 | 1,9 | C | 0 |
| 85= | T51 | Plombier-chauffagiste × artisan × France | 2 | 3 | 4 | 3 | 3,2 | 3 | 1,9 | C | 0 |
| 85= | T44 | Technicien de maintenance industrielle × salarié × France | 2 | 3 | 3 | 3 | 3,3 | 4 | 1,7 | C | 0 |
| 88 | T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France | 1 | 2 | 3 | 4 | 2,2 | 5 | 2,2 | C | 0 |
| 89 | T58 | Gardien de la paix × fonctionnaire × France | 2 | 2 | 3 | 2 | 2,2 | 5 | 2,1 | C | 0 |
| 90 | T33 | Aide-soignant (ASSC) × salarié × Suisse (frontalier) | 1 | 2 | 3 | 3 | 1,7 | 4 | 3,0 | C | 0 |
| 91= | T75 | Employé commerce ou accueil (référence) × salarié × France | 3 | 3 | 3 | 2 | 2,2 | 3 | 1,1 | C | 0 |
| 91= | T21 | Aide-soignant × fonctionnaire FPH × France | 1 | 2 | 3 | 3 | 1,7 | 5 | 1,5 | C | 0 |
| 93 | T55 | Conducteur poids lourd × salarié × France | 2 | 3 | 2 | 2 | 2,2 | 4 | 1,1 | C | 0 |

### Classement v5, partie B : revenu net en équivalent temps plein

| Rang | ID | Médian au temps réel nom./PPA k€ | Temps de travail et quotité | Médian ETP nom./PPA k€ | P80 ETP nom./PPA k€ | Source du médian | Source du P80 | Fiabilité |
|---|---|---|---|---|---|---|---|---|
| 1 | T30 | 179 / 112 | 43 h par semaine (médecins de famille, 2020), au moins 35 h (quotité 1,00) | 179 / 112 | 287 / 179 | OFS 2019 (S24, S108) : premier recours, médiane 172 000 CHF nets d'AVS et de 2e pilier (relayée par la presse) ; moins la prime LAMal | log-normale (moyenne OFS 199 975 CHF) | relayée |
| 2= | T05 | 94 / 94 | temps de travail non trouvé (quotité 1,00) | 94 / 94 | 152 / 152 | CARCDSF 2023 (S04) : médiane 97 672 € ; × 0,96 ; recoupement Insee (S99) : dentistes 10 300 €/mois moy. | estimé : log-normale des libéraux (× 1,62) | relayée |
| 2= | T91 | 145 / 91 | environ 42 h par semaine, au moins 35 h (quotité 1,00) | 145 / 91 | 235 / 147 | OFS, ESPA 2014-2017, exploitée par la ZHAW pour la FMH (S111) : dentistes de plus de 34 ans, revenu annuel médian 166 000 CHF brut standardisé, tous statuts (indépendants : 84 CHF/h, salariés : 68 CHF/h) ; × 0,85 (AVS et prévoyance des indépendants, estimé) moins la prime LAMal ; aucune statistique de la SSO | estimé : log-normale des libéraux (× 1,62) | relayée |
| 2= | T15 | 22 / 22 | 38 à 39 actes par semaine et 10 h de tâches administratives (FNO) ; durée totale non trouvée (quotité 1,00) | 22 / 22 | 36 / 36 | UNASA 2022 (S06) : 27 550 € moy. ; × 0,96 × 0,85 ; aucun chiffre de la DREES, dont le jeu de données 2026 ne couvre pas les orthophonistes (S136) ; FNO : chiffre d'affaires moyen 2022 de 51 266 € avant charges (S136) | estimé : log-normale des libéraux (× 1,62) | non officielle |
| 5= | T92 | 131 / 106 | 36,1 h par semaine, au moins 35 h (quotité 1,00) | 131 / 106 | 227 / 184 | ADA HPI 2023 (S114) : médiane 185 360 USD, généralistes en cabinet privé ; moins cotisation des indépendants et assurance santé | log-normale (moyenne ADA 218 710 USD) | officielle (ordre professionnel) |
| 5= | T89 | 98 / 61 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 98 / 61 | 114 / 71 | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre à la cybersécurité) ; × 12 × 0,80 | estimé : rapport P80/médian de la v3 (× 1,17) | relayée, proxy |
| 5= | T01 | 80 / 80 | 46 h par semaine, au moins 35 h (quotité 1,00) | 80 / 80 | 130 / 130 | DREES 2021 (S02) : omnipraticiens, revenu d'activité moyen 98 300 € ; × 0,96 × 0,85 ; recoupement CARMF 2024 (S98) : 97 099 € moy. | estimé : log-normale des libéraux (× 1,62) | relayée |
| 8= | T37 | 98 / 89 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 98 / 89 | 116 / 105 | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois ; × 12 × 0,80 | estimé : rapport P80/médian de la v3 (× 1,18) | relayée |
| 8= | T82 | 98 / 89 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 98 / 89 | 113 / 103 | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre au cloud) ; × 12 × 0,80 | estimé : rapport P80/médian de la v3 (× 1,16) | relayée, proxy |
| 8= | T03 | 74 / 74 | temps de travail non trouvé (quotité 1,00) | 74 / 74 | 120 / 120 | DREES 2021 (S02) : pédiatres 88 400 €, psychiatres 92 800 € moy. (spécialités du rang médian) ; × 0,96 × 0,85 ; CARMF 2022 (S98), part libérale seule : 74 884 € et 73 014 € | estimé : log-normale des libéraux (× 1,62) | relayée |
| 8= | T46 | 52 / 52 | temps de travail non trouvé (quotité 1,00) | 52 / 52 | 66 / 66 | non re-sourcé, valeur v3 : estimé : enquete de l'Institut des actuaires non récupérée | estimé (v3) | non re-sourcée |
| 8= | T90 | 98 / 79 | source en équivalent temps plein (salaire horaire × 2 080 h) (quotité 1,00) | 98 / 79 | 132 / 107 | BLS OEWS mai 2024 (S113) : analystes en sécurité de l'information (15-1212), médiane 124 910 USD ; × 0,91 | interpolé entre P75 159 600 et P90 186 420 USD (S113) | officielle |
| 8= | T83 | 50 / 50 | source en équivalent temps plein (salariés à temps plein) (quotité 1,00) | 50 / 50 | 63 / 63 | APEC 2025 (S17, S103) : famille « sécurité informatique », médiane 60 k€ + 4 k€ de variable, brut ; × 0,78 | estimé : rapport P80/médian de la v3 (× 1,26) | relayée |
| 14= | T09 | 34 / 34 | temps de travail non trouvé (quotité 1,00) | 34 / 34 | 56 / 56 | DREES 2021 (S03) : sages-femmes libérales, 42 200 € moy. ; × 0,96 × 0,85 | estimé : log-normale des libéraux (× 1,62) | officielle |
| 14= | T93 | 75 / 61 | source en équivalent temps plein (salaire horaire × 2 080 h) (quotité 1,00) | 75 / 61 | 94 / 76 | BLS OEWS mai 2024 (S113) : orthophonistes, médiane 95 410 USD ; × 0,91 | interpolé entre P75 112 510 et P90 132 850 USD (S113) | officielle |
| 16= | T85 | 42 / 42 | source en équivalent temps plein (salariés à temps plein) (quotité 1,00) | 42 / 42 | 51 / 51 | APEC 2025 (S17, S103) : famille « business intelligence », médiane 50 k€ + 4 k€ de variable, brut (proxy) ; × 0,78 | estimé : rapport P80/médian de la v3 (× 1,20) | relayée, proxy |
| 16= | T64 | 103 / 86 | source en équivalent temps plein (grille à temps plein) (quotité 1,00) | 103 / 86 | 111 / 93 | grille au 1er juillet 2025 (S119, relayée) : AD7 échelon 2 = 8 207,25 € + indemnité de dépaysement 16 %, moins pension 10,1 % et maladie 1,7 % (taux estimés) ; avant impôt de l'UE | AD8 échelon 1 = 8 911,48 € (S119) | relayée (grille) |
| 16= | T39 | 66 / 62 | temps de travail non trouvé (quotité 1,00) | 66 / 62 | 83 / 79 | non re-sourcé, valeur v3 : S30 (STATEC 2022 : médiane nationale 58 126 € brut, aucune médiane par metier) ; estimé TIC 75 000 € × 0,875 | estimé (v3) | non re-sourcée |
| 16= | T71 | 61 / 61 | source en équivalent temps plein (EQTP) (quotité 1,00) | 61 / 61 | 73 / 73 | ministère de la Justice (S126, relayé) : 5 083 €/mois net moyen après six ans d'exercice, primes comprises (3 884 € au début, 8 480 € en fin de carrière) | estimé : amplitude de grille (× 1,2) | relayée |
| 16= | T16 | 31 / 31 | temps de travail non trouvé (quotité 1,00) | 31 / 31 | 36 / 36 | non re-sourcé, valeur v3 : estimé : aucune série officielle récupérée | estimé (v3) | non re-sourcée |
| 21= | T35 | 37 / 37 | champ temps complet non précisé (DARES) (quotité 1,00) | 37 / 37 | 47 / 47 | DARES, portraits statistiques des métiers, données ouvertes (S133) : ingénieurs de l'informatique (M2Z), salaire médian 3 120 € par mois en 2017-2019, net probable (non actualisé) | estimé : rapport P80/médian de la v3 (× 1,25) | relayée |
| 21= | T10 | 42 / 42 | 43,07 h par semaine (Ordre des kinésithérapeutes 2026), au moins 35 h (quotité 1,00) | 42 / 42 | 67 / 67 | DREES 2021 (S03) : masseurs-kinésithérapeutes libéraux, 51 100 € moy. ; × 0,96 × 0,85 | estimé : log-normale des libéraux (× 1,62) | officielle |
| 21= | T86 | 98 / 61 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 98 / 61 | 113 / 71 | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre au cloud) ; × 12 × 0,80 | estimé : rapport P80/médian de la v3 (× 1,16) | relayée, proxy |
| 21= | T81 | 69 / 69 | estimation à temps plein (170 à 180 jours facturés) (quotité 1,00) | 69 / 69 | 90 / 90 | non officielle : TJM Free-Work et Morgan Philips (S74, S75) 650 € × 180 jours × 0,59 ; Insee 2024 (S106) : 4 190 €/mois moy., champ plus large | estimé (v3) | non officielle |
| 25= | T42 | 93 / 84 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 93 / 84 | 114 / 103 | OFS, ESS 2022 (S28) : diplômés HES, médiane 9 000 CHF/mois (proxy) ; × 12 × 0,80 | estimé : rapport P80/médian de la v3 (× 1,23) | relayée, proxy |
| 25= | T68 | 73 / 73 | temps de travail non trouvé (quotité 1,00) | 73 / 73 | 119 / 119 | Insee 2024 (S106) : activités juridiques et comptables, 8 240 €/mois moy. (proxy) ; × 0,874 × 0,85 ; UNASA 2024 (S20) : 87 024 € moy. | estimé : log-normale des libéraux (× 1,62) | relayée, proxy |
| 25= | T41 | 52 / 52 | source en équivalent temps plein (salariés à temps plein) (quotité 1,00) | 52 / 52 | 65 / 65 | IESF 2025 (S16) : médiane 67 000 € brut, tous ingénieurs (proxy) ; × 0,78 | estimé : rapport P80/médian de la v3 (× 1,24) | relayée, proxy |
| 25= | T40 | 51 / 50 | source en équivalent temps plein (salaire horaire × durée à temps plein) (quotité 1,00) | 51 / 50 | 61 / 60 | Guichet-Emplois, Québec 2024 (S35) : médiane 45,67 CAD/h ; × 1 950 h × 0,918 | estimé : rapport P80/médian de la v3 (× 1,20) | officielle |
| 29= | T43 | 72 / 73 | source en équivalent temps plein (EQTP) (quotité 1,00) | 72 / 73 | 86 / 88 | Bundesagentur für Arbeit, Entgeltatlas (S118) : ingénieurs de production, médiane 7 367 €/mois brut à temps plein ; × 12 ; cotisations plafonnées | estimé : rapport P80/médian de la v3 (× 1,20) | relayée |
| 29= | T02 | 57 / 57 | source en équivalent temps plein (EQTP) (quotité 1,00) | 57 / 57 | 67 / 67 | non officielle : 60 000 à 85 000 € brut par an en centre de santé (S129) ; milieu de fourchette × 0,78 | estimé : rapport P80/médian de la v3 (× 1,19) | non officielle |
| 29= | T76 | 33 / 33 | temps de travail non trouvé (quotité 1,00) | 33 / 33 | 45 / 45 | non re-sourcé, valeur v3 : sources en conflit : ONPP 2014, 25 012 € moy. ; UNASA 2024 via JDN, 43 500 € brut (S137) | estimé (v3) | non re-sourcée |
| 29= | T80 | 43 / 43 | source en équivalent temps plein (salariés à temps plein) (quotité 1,00) | 43 / 43 | 53 / 53 | APEC 2025 (S17, S103) : famille « systèmes, réseaux et télécoms », médiane 51 k€ + 4 k€ de variable, brut (proxy) ; × 0,78 | estimé : rapport P80/médian de la v3 (× 1,23) | relayée, proxy |
| 33= | T38 | 58 / 59 | source en équivalent temps plein (salariés à temps plein) (quotité 1,00) | 58 / 59 | 72 / 73 | Bundesagentur für Arbeit 2024 (S33) : informatique, médiane 6 114 €/mois brut ; × 12 ; cotisations plafonnées | estimé : rapport P80/médian de la v3 (× 1,23) | relayée |
| 33= | T77 | 30 / 30 | source en équivalent temps plein (grille à temps plein) (quotité 1,00) | 30 / 30 | 34 / 34 | grille officielle FPH (S65) : IM 395 à 727 + CTI 183 € net/mois ; calcul à 10 ans d'exercice | estimé (v3) | officielle (grille) |
| 33= | T56 | 35 / 35 | source en équivalent temps plein (temps complet) ; 42 à 43 h déclarées (quotité 1,00) | 35 / 35 | 42 / 42 | DEPP 2024 (S101) : professeurs des écoles à temps complet, 2 950 €/mois net moyen ; moyenne = médiane (grille) | estimé : amplitude de grille (× 1,2) | officielle |
| 33= | T88 | 102 / 83 | source en équivalent temps plein (salaire horaire × 2 080 h) (quotité 1,00) | 102 / 83 | 138 / 111 | BLS OEWS mai 2024 (S113) : architectes réseaux et cloud (15-1241), médiane 130 390 USD ; × 0,91 | interpolé entre P75 164 440 et P90 198 030 USD (S113) | officielle, proxy |
| 37= | T34 | 77 / 70 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 77 / 70 | 86 / 78 | OFS, ESS 2024 (S22) : niveau de compétence 3, médiane 7 523 CHF/mois (proxy) ; × 12 × 0,80 | estimé : rapport P80/médian de la v3 (× 1,11) | officielle, proxy |
| 37= | T60 | 40 / 40 | source en équivalent temps plein (EQTP) (quotité 1,00) | 40 / 40 | 49 / 49 | Insee et DGAFP 2023 (S67) : fonctionnaires de catégorie A, 3 373 €/mois net moyen (enseignants compris, proxy) | estimé : amplitude de grille (× 1,2) | officielle, proxy |
| 37= | T61 | 40 / 40 | source en équivalent temps plein (EQTP) (quotité 1,00) | 40 / 40 | 49 / 49 | Insee et DGAFP 2023 (S67) : catégorie A, 3 373 €/mois net moyen (proxy) ; DGFiP (S120) : 2 378 € net à la titularisation | estimé : amplitude de grille (× 1,2) | officielle, proxy |
| 40= | T36 | 58 / 58 | estimation à temps plein (170 à 180 jours facturés) (quotité 1,00) | 58 / 58 | 76 / 76 | non officielle : TJM Malt (S19) 576 € × 170 jours × 0,59 ; Insee 2024 (S106), information et communication : 4 190 €/mois moy., champ plus large | estimé (v3) | non officielle |
| 40= | T62 | 33 / 33 | source en équivalent temps plein (EQTP) (quotité 1,00) | 33 / 33 | 39 / 39 | Insee et DGAFP 2023 (S67) : catégorie B, 2 720 €/mois net moyen (proxy) ; DGFiP : 2 120 € net à la titularisation | estimé : amplitude de grille (× 1,2) | officielle, proxy |
| 40= | T20 | 30 / 30 | temps de travail non trouvé (quotité 1,00) | 30 / 30 | 35 / 35 | non re-sourcé, valeur v3 : estimé : grille psychologues FPH ; aucune série récupérée | estimé (v3) | non re-sourcée |
| 40= | T63 | 94 / 94 | source en équivalent temps plein (EQTP) (quotité 1,00) | 94 / 94 | 113 / 113 | Cour des comptes 2026 (S124) : environ 110 000 € brut annuel moyen, dont 61 % de primes ; net calculé (pension sur le traitement, CSG et CRDS) | estimé : amplitude de grille (× 1,2) | officielle |
| 44= | T78 | 24 / 24 | temps de travail non trouvé (quotité 1,00) | 24 / 24 | 32 / 32 | non re-sourcé, valeur v3 : estimé : aucune série récupérée | estimé (v3) | non re-sourcée |
| 44= | T32 | 110 / 109 | source en équivalent temps plein (EQTP) (quotité 1,00) | 110 / 109 | 170 / 167 | Guichet-Emplois 2023-2024 (S122) : médiane 268 808 CAD, avant frais de cabinet ; moins 30 % de frais (taux conventionnel du gouvernement du Québec) ; - RRQ et RQAP des travailleurs autonomes (9 900 CAD, estimé) | log-normale (haut de fourchette 505 024 CAD lu comme P90) | officielle |
| 44= | T57 | 39 / 39 | source en équivalent temps plein (temps complet) ; 42 à 43 h déclarées (quotité 1,00) | 39 / 39 | 46 / 46 | DEPP 2024 (S101) : professeurs certifiés à temps complet, 3 220 €/mois net moyen ; moyenne = médiane (grille) | estimé : amplitude de grille (× 1,2) | officielle |
| 44= | T87 | 70 / 56 | source en équivalent temps plein (salaire annuel à temps plein) (quotité 1,00) | 70 / 56 | 100 / 80 | CSO 2024 (S123) : secteur information et communication, médiane 1 440,36 €/semaine brut (proxy) ; × 52 ; moins PRSI et USC (S85) | estimé : rapport P80/médian des guides privés (× 1,44, S79) | officielle, proxy |
| 48= | T70 | 54 / 52 | temps de travail non trouvé (quotité 1,00) | 54 / 52 | 66 / 62 | non re-sourcé, valeur v3 : S30 (STATEC 2022 : médiane nationale 58 126 € brut, aucune médiane par metier) ; estimé 62 000 € × 0,875 | estimé (v3) | non re-sourcée |
| 48= | T18 | 36 / 36 | temps de travail non trouvé (quotité 1,00) | 36 / 36 | 45 / 45 | non re-sourcé, valeur v3 : S21 (APEC : offres 36 600 € brut moy. ; confirme 2 300-3 100 € net/mois) | estimé (v3) | non re-sourcée |
| 50= | T11 | 31 / 31 | source en équivalent temps plein (EQTP) (quotité 1,00) | 31 / 31 | 37 / 37 | DGAFP 2025 (S128) : FPH, personnels des services de soins, 2 565 €/mois net moyen en 2023 (proxy) | estimé : amplitude de grille (× 1,2) | officielle, proxy |
| 50= | T67 | 54 / 54 | temps de travail non trouvé (quotité 1,00) | 54 / 54 | 122 / 122 | CNBF, rapport 2024 (S107) : médianes nettes 65 378 € (hommes) et 49 491 € (femmes), pondérées 43/57 (part des femmes estimée) ; × 0,96 | log-normale (moyennes CNBF 120 198 € et 66 812 €) | relayée |
| 52= | T65 | 51 / 49 | source en équivalent temps plein (grille à temps plein) (quotité 1,00) | 51 / 49 | 56 / 53 | grille des agents contractuels 2025 (S119) : GF III grade 8 = 3 475,62 € (officiel), grade 9 de 3 932,44 à 4 449,30 € ; mi-carrière 4 100 € estimé + 16 %, moins cotisations | GF III grade 10, échelon 1 = 4 449,30 € | relayée (grille) |
| 52= | T13 | 47 / 47 | temps de travail non trouvé (quotité 1,00) | 47 / 47 | 75 / 75 | DREES 2021 (S03) : infirmiers libéraux, 57 100 € moy. ; × 0,96 × 0,85 | estimé : log-normale des libéraux (× 1,62) | officielle |
| 54= | T72 | 38 / 38 | temps de travail non trouvé (quotité 1,00) | 38 / 38 | 55 / 55 | non re-sourcé, valeur v3 : S08 (PI et cadres) ; estimé 3 200 €/mois variable inclus | estimé (v3) | non re-sourcée |
| 54= | T22 | 20 / 20 | temps de travail non trouvé (quotité 1,00) | 20 / 20 | 33 / 33 | Registre des ostéopathes de France, rapport 2026 (S135) : revenu mensuel moyen 1 987 € en 2024, définition non précisée ; × 0,85 | estimé : log-normale des libéraux (× 1,62) | non officielle |
| 56= | T69 | 29 / 29 | temps de travail non trouvé (quotité 1,00) | 29 / 29 | 34 / 34 | non re-sourcé, valeur v3 : S08 (PI) ; estimé 2 400 €/mois | estimé (v3) | non re-sourcée |
| 56= | T19 | 57 / 57 | temps de travail non trouvé (quotité 1,00) | 57 / 57 | 92 / 92 | Insee 2024 (S01) : vétérinaires, 6 370 €/mois moy. ; × 0,874 × 0,85 | estimé : log-normale des libéraux (× 1,62) | relayée |
| 58= | T06 | 38 / 38 | source en équivalent temps plein (EQTP) (quotité 1,00) | 38 / 38 | 45 / 45 | convention collective de l'officine 2026 (S127) : point 5,278 €, coefficient 500 (mi-carrière, estimé), 151,67 h par mois ; minimum conventionnel × 0,78 ; salaires réels non trouvés | estimé : rapport P80/médian de la v3 (× 1,20) | officielle (grille) |
| 58= | T29 | 175 / 110 | 56 à 58 h par semaine (médecins assistants et chefs de clinique, ASMAC 2022-2023) (quotité 1,00) | 175 / 110 | 227 / 142 | BASS pour l'OFSP (S110) : revenu AVS médian des médecins salariés 197 100 CHF, 2014 ; × 0,83 | estimé : rapport P80/médian de la v3 (× 1,29) | officielle ancienne |
| 60 | T45 | 34 / 34 | temps de travail non trouvé (quotité 1,00) | 34 / 34 | 42 / 42 | non re-sourcé, valeur v3 : S08 (PI médiane 2 440 €, D9 3 680 €) ; estimé 2 800 €/mois | estimé (v3) | non re-sourcée |
| 61= | T74 | 93 / 93 | source en équivalent temps plein (EQTP) (quotité 1,00) | 93 / 93 | 121 / 121 | non officielle : sites spécialisés (S129), environ 118 700 € brut annuel moyen à Air France, toutes anciennetés ; × 0,78 | estimé : rapport P80/médian de la v3 (× 1,31) | non officielle |
| 61= | T04 | 83 / 83 | source en équivalent temps plein (EQTP) (quotité 1,00) | 83 / 83 | 100 / 100 | Insee FPH 2024 (S09) : personnels médicaux, 6 926 €/mois net moyen en EQTP ; moyenne = médiane (grille) | estimé : amplitude de grille (× 1,2) | officielle, champ plus large |
| 63 | T84 | 37 / 37 | source en équivalent temps plein (offres d'emploi à temps plein) (quotité 1,00) | 37 / 37 | 43 / 43 | APEC (S134, relayée) : offres d'emploi en cybersécurité, salaire moyen proposé 48 000 € brut (proxy pour le SOC) ; × 0,78 | log-normale avec P90 = 60 000 € (80 % des offres entre 37 000 et 60 000 €) | relayée, proxy |
| 64= | T31 | 104 / 105 | source en équivalent temps plein (grille à temps plein) (quotité 1,00) | 104 / 105 | 120 / 122 | grille TV-Ärzte VKA 2026 (S118) : Ä2 échelon 3 = 8 741,40 €/mois ; + gardes, total estimé 121 000 € brut ; cotisations plafonnées ; Entgeltatlas : médiane des médecins plafonnée à 7 450 € | estimé : rapport P80/médian de la v3 (× 1,16) | officielle (grille) |
| 64= | T07 | 57 / 57 | temps de travail non trouvé (quotité 1,00) | 57 / 57 | 92 / 92 | Insee 2024 (S99) : pharmaciens non salariés, 6 390 €/mois moy. ; × 0,874 × 0,85 | estimé : log-normale des libéraux (× 1,62) | relayée |
| 64= | T08 | 41 / 41 | source en équivalent temps plein (EQTP) (quotité 1,00) | 41 / 41 | 50 / 50 | DREES 2022 (S10) : sages-femmes salariées des hôpitaux, 3 442 €/mois net moyen (3 487 € dans le tableau) ; moyenne = médiane (grille) | estimé : amplitude de grille (× 1,2) | officielle |
| 64= | T14 | 42 / 42 | temps de travail non trouvé (quotité 1,00) | 42 / 42 | 48 / 48 | non re-sourcé, valeur v3 : estimé : grille IADE FPH ; ancrage S09 | estimé (v3) | non re-sourcée |
| 64= | T79 | 27 / 27 | temps de travail non trouvé (quotité 1,00) | 27 / 27 | 32 / 32 | non re-sourcé, valeur v3 : S08 (PI médiane 2 440 €) ; estimé 2 250 €/mois | estimé (v3) | non re-sourcée |
| 69= | T24 | 82 / 74 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 82 / 74 | 96 / 87 | OFSP (S23) : médiane des infirmiers diplômés 7 400 CHF/mois à temps plein, 13e compris (2018) ; × 1,074 × 0,80 | OFSP (S23) : environ 8 700 CHF/mois après plus de 20 ans | officielle ancienne |
| 69= | T50 | 44 / 44 | source en équivalent temps plein (salaire horaire × durée à temps plein) (quotité 1,00) | 44 / 44 | 52 / 51 | Guichet-Emplois, Québec 2024 (S35) : électriciens en construction, médiane 41 CAD/h ; × 1 900 h × 0,918 | estimé : rapport P80/médian de la v3 (× 1,17) | officielle |
| 69= | T25 | 75 / 72 | source en équivalent temps plein (grille à temps plein) (quotité 1,00) | 75 / 72 | 91 / 87 | grille officielle FHL (S29) : carrière CS7, 227 à 443 points, soit 5 056 à 9 867 € brut par mois (point d'avril 2023) ; mi-carrière estimée 6 600 €/mois × 13 ; × 0,875 | estimé (v3) | officielle (grille) |
| 72= | T54 | 79 / 49 | source en équivalent temps plein (grille à 100 %) (quotité 1,00) | 79 / 49 | 91 / 57 | modèle de calcul des CFF 2026 (S121, relayé) : 5 726 à 8 190 CHF/mois à 100 %, 13 salaires ; mi-carrière estimée 7 100 CHF ; × 0,80 | maximum de la grille, 8 190 CHF/mois × 13 | relayée (grille d'entreprise) |
| 72= | T26 | 75 / 63 | source en équivalent temps plein (grille à temps plein) (quotité 1,00) | 75 / 63 | 91 / 76 | grille officielle FHL (S29) : carrière CS7, 227 à 443 points, soit 5 056 à 9 867 € brut par mois (point d'avril 2023) ; mi-carrière estimée 6 600 €/mois × 13 ; × 0,875 | estimé (v3) | officielle (grille) |
| 72= | T49 | 64 / 58 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 64 / 58 | 74 / 68 | OFS, ESS 2022 (S28) : titulaires d'un CFC, médiane 6 190 CHF/mois (proxy) ; × 12 × 0,80 | estimé : rapport P80/médian de la v3 (× 1,17) | relayée, proxy |
| 72= | T17 | 33 / 33 | source en équivalent temps plein (EQTP) (quotité 1,00) | 33 / 33 | 40 / 40 | DGAFP 2025 (S128) : FPH, filière médico-technique, 2 749 €/mois net moyen en 2023 (proxy) | estimé : amplitude de grille (× 1,2) | officielle, proxy |
| 76= | T53 | 37 / 37 | temps de travail non trouvé (quotité 1,00) | 37 / 37 | 46 / 46 | non re-sourcé, valeur v3 : aucune source officielle ; reperes non officiels : 4 214 € brut par mois variables compris en 2023 (S129) | estimé (v3) | non re-sourcée |
| 76= | T23 | 82 / 51 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 82 / 51 | 96 / 60 | OFSP (S23) : médiane des infirmiers diplômés 7 400 CHF/mois à temps plein, 13e compris, estimation OFS 2018 ; × 1,074 (hausse de la médiane ESS 2018-2024) × 0,80 | OFSP (S23) : environ 8 700 CHF/mois après plus de 20 ans, même ajustement | officielle ancienne |
| 78= | T47 | 26 / 26 | temps de travail non trouvé (quotité 1,00) | 26 / 26 | 31 / 31 | non re-sourcé, valeur v3 : S08 (INSEE 2023 : ouvriers médiane 1 920 €/mois) ; estimé ouvrier qualifie 2 200 € | estimé (v3) | non re-sourcée |
| 78= | T28 | 44 / 44 | source en équivalent temps plein (salaire horaire × durée à temps plein) (quotité 1,00) | 44 / 44 | 51 / 50 | Guichet-Emplois, Québec 2024 (S35) : médiane 40 CAD/h ; × 1 950 h × 0,918 | log-normale entre la médiane et le salaire élevé (45 CAD/h, lu comme Q3) | officielle |
| 80= | T12 | 33 / 33 | source en équivalent temps plein (EQTP) (quotité 1,00) | 33 / 33 | 40 / 40 | DREES 2022 (S10) : infirmiers, 2 755 €/mois net moyen en EQTP, toutes structures ; moyenne = médiane (grille) ; FPH 2024, tous agents : moyenne 2 896 €, médiane 2 474 € (S100) | estimé : amplitude de grille (× 1,2) | officielle |
| 80= | T52 | 30 / 30 | temps de travail non trouvé (quotité 1,00) | 30 / 30 | 36 / 36 | non re-sourcé, valeur v3 : S08 (ouvriers et PI) ; estimé 2 500 €/mois | estimé (v3) | non re-sourcée |
| 82= | T73 | 22 / 22 | temps de travail non trouvé (quotité 1,00) | 22 / 22 | 36 / 36 | Insee 2024 (S106) : activités immobilières, 2 480 €/mois moy. (proxy), 27 % de revenus nuls ou déficitaires ; × 0,874 × 0,85 | estimé : log-normale des libéraux (× 1,62) | relayée, proxy |
| 82= | T27 | 43 / 44 | source en équivalent temps plein (salariés à temps plein) (quotité 1,00) | 43 / 44 | 49 / 50 | Destatis avril 2024 (S32) : 4 310 €/mois brut ; × 12,8 (primes annuelles, estimé) ; cotisations 2025 plafonnées | estimé : rapport P80/médian de la v3 (× 1,14) | relayée |
| 82= | T66 | 32 / 32 | source en équivalent temps plein (EQTP) (quotité 1,00) | 32 / 32 | 38 / 38 | ministère des Armées, EcoDef n° 266 (S125) : solde nette médiane des sous-officiers 2 637 €/mois en 2023, toutes armées hors gendarmerie | estimé : amplitude de grille (× 1,2) | officielle |
| 85= | T48 | 27 / 27 | temps de travail non trouvé (quotité 1,00) | 27 / 27 | 43 / 43 | Insee 2024 (S01) : construction, non-salariés classiques, 3 050 €/mois moy. (proxy) ; × 0,864 × 0,85 | estimé : log-normale des libéraux (× 1,62) | relayée, proxy |
| 85= | T51 | 27 / 27 | temps de travail non trouvé (quotité 1,00) | 27 / 27 | 43 / 43 | Insee 2024 (S01) : construction, non-salariés classiques, 3 050 €/mois moy. (proxy) ; × 0,864 × 0,85 | estimé : log-normale des libéraux (× 1,62) | relayée, proxy |
| 85= | T44 | 29 / 29 | temps de travail non trouvé (quotité 1,00) | 29 / 29 | 34 / 34 | non re-sourcé, valeur v3 : S08 (INSEE 2023 : professions intermediaires médiane 2 440 €/mois) ; estimé 2 400 € | estimé (v3) | non re-sourcée |
| 88 | T59 | 36 / 36 | source en équivalent temps plein (EQTP) (quotité 1,00) | 36 / 36 | 44 / 44 | Insee 2023 (S102) : agents des SDIS, 3 030 €/mois net moyen en EQTP, sapeurs-pompiers et non-sapeurs-pompiers ; moyenne = médiane (grille) | estimé : amplitude de grille (× 1,2) | officielle, champ plus large |
| 89 | T58 | 34 / 34 | source en équivalent temps plein (EQTP) (quotité 1,00) | 34 / 34 | 41 / 41 | catégorie B de la police, 2 870 €/mois net moyen (DGAFP 2025, relayé par un site tiers, proxy) ; grille 2026 : 2 162 à 3 917 € net/mois (S120) | estimé : amplitude de grille (× 1,2) | relayée, proxy |
| 90 | T33 | 60 / 55 | source en équivalent temps plein (salaire standardisé de l'ESS) (quotité 1,00) | 60 / 55 | 66 / 60 | OFS, ESS 2024 (S22) : niveau de compétence 2, médiane 5 866 CHF/mois (proxy) ; × 12 × 0,80 | estimé : rapport P80/médian de la v3 (× 1,09) | officielle, proxy |
| 91= | T75 | 22 / 22 | source en équivalent temps plein (EQTP) (quotité 1,00) | 22 / 22 | 26 / 26 | Insee 2023 (S08) : employés, médiane 1 800 €/mois net | estimé : rapport P80/médian de la v3 (× 1,19) | officielle |
| 91= | T21 | 26 / 26 | source en équivalent temps plein (EQTP) (quotité 1,00) | 26 / 26 | 31 / 31 | DREES 2022 (S10) : aides-soignants et ASH, 2 184 €/mois net moyen ; moyenne = médiane (grille) | estimé : amplitude de grille (× 1,2) | officielle, champ plus large |
| 93 | T55 | 22 / 22 | source en équivalent temps plein (EQTP) (quotité 1,00) | 22 / 22 | 26 / 26 | SDES 2019 (S105) : ouvriers qualifiés du transport routier de marchandises, 1 830 €/mois net en EQTP (non actualisé) | estimé : rapport P80/médian de la v3 (× 1,17) | officielle ancienne |

### Classement v5, partie C : provenance des notes hors revenu

S = sourcée : chiffre officiel et chiffré pour le métier lui-même, dans le pays du triplet. M = mixte : chiffre pour un groupe plus large, un autre pays ou un autre statut, sans ampleur publiée, issu d'une enquête non officielle, ou ne couvrant qu'une partie de la dimension (QT et CA sont au mieux M). E = estimée : aucun chiffre trouvé, note de la grille normative. Ancrages : codes de la partie C2. Tensions : note maintenue alors qu'un chiffre de statut M indique une autre valeur.

| Rang | ID | EP | IT | QT | ES | CA | PS | Ancrages | Tensions |
|---|---|---|---|---|---|---|---|---|---|
| 1 | T30 | E | E | M | E | M | E | QT Q10 | aucune |
| 2= | T05 | M | E | E | E | M | E | EP E8 | aucune |
| 2= | T91 | M | E | M | E | M | E | EP E8 ; QT Q12 | aucune |
| 2= | T15 | E | E | E | M | M | M | ES S2 ; PS P7 | ES (S2) |
| 5= | T92 | M | E | M | E | M | E | EP E8 ; QT Q13 | aucune |
| 5= | T89 | M | E | E | E | M | M | EP E1 ; PS P4 | aucune |
| 5= | T01 | E | E | M | E | M | M | QT Q1, Q2 ; PS P6 | aucune |
| 8= | T37 | M | E | E | E | M | E | EP E1 | aucune |
| 8= | T82 | M | E | E | E | M | E | EP E1 | aucune |
| 8= | T03 | E | E | M | E | M | M | QT Q2 ; PS P6 | aucune |
| 8= | T46 | M | E | E | E | M | M | EP E1 ; PS P2 | aucune |
| 8= | T90 | M | E | E | E | M | S | EP E1 ; PS P5 | aucune |
| 8= | T83 | M | E | E | E | M | S | EP E1 ; PS P2, P3, P4 | aucune |
| 14= | T09 | E | E | E | M | M | E | ES S2 | ES (S2) |
| 14= | T93 | E | E | E | M | M | E | ES S2 | ES (S2) |
| 16= | T85 | M | E | E | E | M | S | EP E1 ; PS P2, P3 | aucune |
| 16= | T64 | M | E | E | E | M | E | EP E1 | aucune |
| 16= | T39 | M | E | E | E | M | E | EP E1 | aucune |
| 16= | T71 | M | E | E | E | M | M | EP E1 ; PS P1 | aucune |
| 16= | T16 | E | E | E | M | M | E | ES S2 | ES (S2) |
| 21= | T35 | M | E | E | E | M | S | EP E1 ; PS P2, P3 | aucune |
| 21= | T10 | E | E | M | M | M | E | QT Q9 ; ES S2 | ES (S2) |
| 21= | T86 | M | E | E | E | M | E | EP E1 | aucune |
| 21= | T81 | E | E | E | E | M | M | PS P3 | aucune |
| 25= | T42 | M | E | E | E | M | E | EP E1 | aucune |
| 25= | T68 | E | E | E | E | M | E | aucun | aucune |
| 25= | T41 | M | E | E | E | M | M | EP E1 ; PS P2 | aucune |
| 25= | T40 | M | E | E | E | M | E | EP E1 | aucune |
| 29= | T43 | M | E | E | E | M | E | EP E1 | aucune |
| 29= | T02 | E | E | M | E | M | M | QT Q2 ; PS P2, P6 | aucune |
| 29= | T76 | E | E | E | M | M | E | ES S2 | ES (S2) |
| 29= | T80 | M | E | E | E | M | S | EP E1 ; PS P2, P3 | aucune |
| 33= | T38 | M | E | E | E | M | E | EP E1 | aucune |
| 33= | T77 | E | E | E | M | M | M | ES S2 ; PS P1 | ES (S2) |
| 33= | T56 | M | M | M | S | M | M | EP E7 ; IT I3 ; QT Q14 ; ES S3 ; PS P1 | aucune |
| 33= | T88 | M | E | E | E | M | E | EP E1 | aucune |
| 37= | T34 | E | E | E | M | M | E | ES S2 | ES (S2) |
| 37= | T60 | M | E | E | E | M | M | EP E1 ; PS P1 | aucune |
| 37= | T61 | M | E | E | E | M | M | EP E1 ; PS P1 | aucune |
| 40= | T36 | E | E | E | E | M | M | PS P3 | PS (P3) |
| 40= | T62 | E | E | E | E | M | M | PS P1 | aucune |
| 40= | T20 | E | E | E | E | M | E | aucun | aucune |
| 40= | T63 | M | E | E | E | M | M | EP E1 ; PS P1 | aucune |
| 44= | T78 | E | E | E | M | M | E | ES S2 | ES (S2) |
| 44= | T32 | E | E | E | E | M | E | aucun | aucune |
| 44= | T57 | M | M | M | S | M | M | EP E7 ; IT I3 ; QT Q14 ; ES S3 ; PS P1 | aucune |
| 44= | T87 | M | E | E | E | M | E | EP E1 | aucune |
| 48= | T70 | E | E | E | E | M | E | aucun | aucune |
| 48= | T18 | E | E | E | M | M | E | ES S2 | ES (S2) |
| 50= | T11 | E | E | E | M | M | M | ES S2 ; PS P1 | ES (S2) |
| 50= | T67 | E | E | E | E | M | E | aucun | aucune |
| 52= | T65 | E | E | E | E | M | E | aucun | aucune |
| 52= | T13 | E | E | E | M | M | E | ES S2 | ES (S2) |
| 54= | T72 | E | E | E | E | M | E | aucun | aucune |
| 54= | T22 | E | E | E | E | M | E | aucun | aucune |
| 56= | T69 | E | E | E | E | M | E | aucun | aucune |
| 56= | T19 | E | E | E | E | M | E | aucun | aucune |
| 58= | T06 | E | E | E | E | M | M | PS P2 | aucune |
| 58= | T29 | E | M | M | E | M | E | IT I2 ; QT Q3, Q11 | aucune |
| 60 | T45 | E | E | E | E | M | M | PS P4 | aucune |
| 61= | T74 | E | E | E | M | M | E | ES S4 | aucune |
| 61= | T04 | E | M | M | E | M | M | IT I2 ; QT Q3 ; PS P1, P6 | aucune |
| 63 | T84 | M | E | E | E | M | S | EP E1 ; PS P2, P4 | aucune |
| 64= | T31 | E | M | M | E | M | E | IT I2 ; QT Q3 | aucune |
| 64= | T07 | E | E | E | E | M | E | aucun | aucune |
| 64= | T08 | M | M | M | M | M | M | EP E6 ; IT I1 ; QT Q4 ; ES S2 ; PS P1 | EP (E6) |
| 64= | T14 | M | M | M | M | M | M | EP E6 ; IT I1 ; QT Q4 ; ES S2 ; PS P1 | EP (E6) |
| 64= | T79 | E | E | E | M | M | E | ES S2 | aucune |
| 69= | T24 | M | M | M | M | M | E | EP E6 ; IT I1 ; QT Q4 ; ES S2 | aucune |
| 69= | T50 | M | E | E | E | M | E | EP E2, E4 | aucune |
| 69= | T25 | M | M | M | M | M | E | EP E6 ; IT I1 ; QT Q4 ; ES S2 | aucune |
| 72= | T54 | M | E | E | M | M | E | EP E5 ; ES S4 | EP (E5) |
| 72= | T26 | M | M | M | M | M | E | EP E6 ; IT I1 ; QT Q4 ; ES S2 | aucune |
| 72= | T49 | M | E | E | E | M | E | EP E2, E3, E4 | aucune |
| 72= | T17 | E | E | E | M | M | M | ES S2 ; PS P1 | aucune |
| 76= | T53 | M | E | E | M | M | E | EP E5 ; ES S4 | EP (E5) |
| 76= | T23 | M | M | M | M | M | E | EP E6 ; IT I1 ; QT Q4 ; ES S2 | aucune |
| 78= | T47 | M | E | E | E | M | E | EP E2, E4 | aucune |
| 78= | T28 | M | M | M | M | M | E | EP E6 ; IT I1 ; QT Q4 ; ES S2 | aucune |
| 80= | T12 | M | M | M | M | M | M | EP E6 ; IT I1 ; QT Q4 ; ES S2 ; PS P1 | aucune |
| 80= | T52 | M | E | E | E | M | E | EP E2, E4 | aucune |
| 82= | T73 | E | E | E | E | M | E | aucun | aucune |
| 82= | T27 | M | M | M | M | M | E | EP E6 ; IT I1 ; QT Q4 ; ES S2 | aucune |
| 82= | T66 | E | E | M | E | M | E | QT Q6 | aucune |
| 85= | T48 | M | E | E | E | M | E | EP E2, E4 | aucune |
| 85= | T51 | M | E | E | E | M | E | EP E2, E4 | aucune |
| 85= | T44 | E | E | E | E | M | E | aucun | aucune |
| 88 | T59 | E | E | M | E | M | M | QT Q6 ; PS P1 | aucune |
| 89 | T58 | E | E | M | S | M | M | QT Q6 ; ES S1 ; PS P1 | aucune |
| 90 | T33 | M | E | M | E | M | E | EP E6 ; QT Q5 | aucune |
| 91= | T75 | E | E | M | E | M | E | QT Q8 | QT (Q8) |
| 91= | T21 | M | E | M | E | M | M | EP E6 ; QT Q5 ; PS P1 | aucune |
| 93 | T55 | M | E | M | M | M | E | EP E2, E5 ; QT Q7 ; ES S4 | aucune |

| Dimension | Sourcées | Mixtes | Estimées |
|---|---|---|---|
| EP | 0 | 49 | 44 |
| IT | 0 | 14 | 79 |
| QT | 0 | 28 | 65 |
| ES | 3 | 27 | 63 |
| CA | 0 | 93 | 0 |
| PS | 6 | 28 | 59 |
| Total (558 notes) | 9 | 239 | 310 |

### Classement v5, partie C2 : ancrages utilisés

Règles de conversion et de statut : section 1.13. Notes compatibles : valeurs que le chiffre autorise (pour QT, présence ou absence des facteurs F1 et F3).

| Code | Dim. | Chiffre publié | Source | Statut | Notes compatibles | Triplets couverts | Tensions |
|---|---|---|---|---|---|---|---|
| E1 | EP | cadres salariés, France : 7 % déclarent au moins 3 contraintes physiques (ensemble 35 %), bande 5 | S58 | M | 4 ou 5 | T35, T37, T38, T39, T40, T41, T42, T43, T46, T60, T61, T63, T64, T71, T80, T82, T83, T84, T85, T86, T87, T88, T89, T90 | aucune |
| E2 | EP | ouvriers qualifiés, France : 61 % (bande 2) ; bruit 67,5 % ; produits cancérogènes 34,8 % (ensemble 11 %, rapport 3,2) | S58, S144 | M | 1 ou 2 | T47, T48, T49, T50, T51, T52, T55 | aucune |
| E3 | EP | construction, Suisse : plus de 80 % des actifs exposés à au moins 3 risques physiques sur 10 (ensemble 45 %, rapport supérieur à 1,8) | S149 | M | 1 ou 2 | T49 | aucune |
| E4 | EP | Eurofound, artisanat et bâtiment (CITP 7) : indice d'environnement physique 70, moyenne de l'UE 84 | S146 | M | 1 ou 2 | T47, T48, T49, T50, T51, T52 | aucune |
| E5 | EP | Eurofound, conducteurs de machines et de véhicules (CITP 8) : indice 75, moyenne de l'UE 84 | S146 | M | 1 ou 2 | T53, T54, T55 | T53, T54 |
| E6 | EP | hôpital, France : contraintes physiques au 1er rang chez les aides-soignants, au 3e chez les infirmiers et sages-femmes ; secteur : station debout prolongée 66 % (ensemble 48 %), charges lourdes 61 % (41 %) ; fonction publique hospitalière : 54 % avec au moins 3 contraintes (bande 2) | S138, S58 | M | 1 ou 2 | T21, T33, T08, T12, T14, T23, T24, T25, T26, T27, T28 | T08, T14 |
| E7 | EP | enseignants, France : plus exposés que les autres cadres pour la posture (sans ampleur publiée) | S145 | M | 1 à 4 | T56, T57 | aucune |
| E8 | EP | orthodontistes, France (enquête 2020, 506 volontaires) : 84 % de troubles musculosquelettiques sur 12 mois (18-64 ans : 51 à 58 %, rapport 1,4 à 1,6) | S153 | M | 2 ou 3 | T05, T91, T92 | aucune |
| I1 | IT | infirmiers et sages-femmes à l'hôpital, France : 72 % doivent toujours ou souvent se dépêcher (secteur hospitalier 62 %) ; exigences émotionnelles 54 % | S138 | M | 1 à 3 | T08, T12, T14, T23, T24, T25, T26, T27, T28 | aucune |
| I2 | IT | médecins hospitaliers, France : exigences émotionnelles 74 % | S138 | M | 1 à 3 | T04, T29, T31 | aucune |
| I3 | IT | enseignants, France : plus exposés que les autres cadres à l'intensité et aux exigences émotionnelles, sans ampleur publiée ; les cadres ont eux-mêmes une forte demande psychologique (S70) | S145, S70 | M | 1 à 3 | T56, T57 | aucune |
| Q1 | QT | généralistes libéraux, France : 46 h par semaine en 2025, donc F1 (seuil 45 h, à 1 h près) | S07 | M | F1 présent | T01 | aucune |
| Q2 | QT | médecins hors hôpital, France : moins de 20 % travaillent de nuit, donc pas de F3 | S138 | M | F3 absent | T01, T02, T03 | aucune |
| Q3 | QT | médecins hospitaliers, France : nuit 62 %, dimanche 72 %, donc F3 | S138 | M | F3 présent | T04, T29, T31 | aucune |
| Q4 | QT | infirmiers et sages-femmes à l'hôpital, France : nuit 47 %, dimanche 75 %, donc F3 | S138 | M | F3 présent | T08, T12, T14, T23, T24, T25, T26, T27, T28 | aucune |
| Q5 | QT | aides-soignants à l'hôpital, France : nuit 39 %, dimanche 87 %, donc F3 | S138 | M | F3 présent | T21, T33 | aucune |
| Q6 | QT | policiers, militaires et pompiers, France : samedi 69 %, dimanche 61 %, nuit 54 %, donc F3 | S141 | M | F3 présent | T58, T59, T66 | aucune |
| Q7 | QT | conducteurs routiers de fret, France : 4 sur 10 font au moins 48 h de service par semaine, donc F1 ; transport et entreposage : 56 % en horaires atypiques | S143, S140 | M | F1 présent ; F3 présent | T55 | aucune |
| Q8 | QT | employés peu qualifiés, France : samedi 49 %, dimanche 32 %, sous le seuil de 40 %, donc F3 non établi ; commerce : 59 % en horaires atypiques | S140 | M | F3 absent | T75 | T75 |
| Q9 | QT | kinésithérapeutes libéraux, France : 43,07 h par semaine, donc pas de F1 | S132 | M | F1 absent | T10 | aucune |
| Q10 | QT | médecins de famille, Suisse : 43 h par semaine (étude Workforce 2020), donc pas de F1 | S131 | M | F1 absent | T30 | aucune |
| Q11 | QT | médecins assistants et chefs de clinique, Suisse : 56 à 58 h par semaine (enquête syndicale ASMAC), donc F1 | S130 | M | F1 présent | T29 | aucune |
| Q12 | QT | dentistes, Suisse : environ 42 h par semaine, donc pas de F1 | S111 | M | F1 absent | T91 | aucune |
| Q13 | QT | dentistes, États-Unis : 36,1 h par semaine, donc pas de F1 | S114 | M | F1 absent | T92 | aucune |
| Q14 | QT | enseignants, France : 42 à 43 h par semaine déclarées, donc pas de F1 | S101 | M | F1 absent | T56, T57 | aucune |
| S1 | ES | policiers et gendarmes, France : 31,2 % victimes d'agressions verbales (ensemble 14,3 %, rapport 2,2) ; agressions physiques près de 7 fois plus fréquentes | S142 | S | 1 ou 2 | T58 | aucune |
| S2 | ES | professions intermédiaires de la santé et du travail social, France : 20,9 % victimes d'agressions verbales (ensemble 14,3 %, rapport 1,46) | S142 | M | 3 | T08, T09, T10, T11, T12, T13, T14, T15, T16, T17, T18, T23, T24, T25, T26, T27, T28, T34, T76, T77, T78, T79, T93 | T09, T10, T11, T13, T15, T16, T18, T34, T76, T77, T78, T93 |
| S3 | ES | France, menaces ou insultes : professeurs des écoles 10,1 % (rapport 1,44), enseignants du second degré 12,5 % (rapport 1,79), ensemble des actifs 7,0 % ; second degré : tensions avec le public deux fois plus fréquentes que chez les autres cadres | S145 | S | 3 (T56) ; 1 ou 2 (T57) | T56, T57 | aucune |
| S4 | ES | transports, UE : part la plus élevée de soutien rare ou absent de la hiérarchie et des collègues | S147 | M | 1 à 3 | T53, T54, T55, T74 | aucune |
| P1 | PS | agents publics sans limite de durée, France : 12 % craignent pour leur emploi dans l'année (ensemble des salariés : un sur cinq, rapport 0,6) | S139 | M | 4 ou 5 | T04, T08, T11, T12, T14, T17, T21, T56, T57, T58, T59, T60, T61, T62, T63, T71, T77 | aucune |
| P2 | PS | cadres, France : 13 % craignent pour leur emploi (rapport 0,65, à la limite du seuil de 2/3) | S139 | M | 4 ou 5 | T02, T06, T35, T41, T46, T80, T83, T84, T85 | aucune |
| P3 | PS | ingénieurs de l'informatique, France : 115 000 créations nettes d'emplois de 2019 à 2030, soit +26 % (ensemble des métiers : environ 1 million, près de 4 %) ; pénurie citée en cybersécurité et en développement ; grille 1.3 : forte demande = 4 pour un salarié, 3 pour un indépendant | S117 | M : T36, T81 ; S : T35, T80, T83, T85 | 4 (T35, T80, T83, T85) ; 3 (T36, T81) | T35, T80, T83, T85, T36, T81 | T36 |
| P4 | PS | cybersécurité, France : offres +49 % de 2019 à 2024 (observatoire de l'ANSSI), 25 000 postes à pourvoir d'ici 2028 (OPIIEC) ; forte demande = 4 | S78 | M : T45, T89 ; S : T83, T84 | 4 | T83, T84, T45, T89 | aucune |
| P5 | PS | analystes en sécurité de l'information, États-Unis : emploi projeté +29 % de 2024 à 2034 (tous métiers +3,1 %) ; forte demande = 4 | S87 | S | 4 | T90 | aucune |
| P6 | PS | médecins, France : tension de recrutement « particulièrement élevée » en 2024 (indicateur de la DARES, déclinaison régionale) ; profession réglementée en pénurie = 5 | S152 | M | 5 | T01, T02, T03, T04 | aucune |
| P7 | PS | orthophonistes libéraux, France : 90 % ne peuvent pas proposer de nouveau bilan (enquête de la FNO citée dans une question parlementaire) ; pénurie = 5 | S154 | M | 5 | T15 | aucune |

### Notes modifiées par un ancrage de statut S

- T35 Développeur × salarié × France : PS 3 → 4 (P3).
- T57 Professeur certifié × fonctionnaire × France : ES 3 → 2 (S3).
- T85 Data engineer × salarié × France : PS 3 → 4 (P3).

### Classement v5, partie D : barrière d'entrée, risque IA et dominance (informatif, hors score)

| Rang | ID | Âge d'entrée | Formation et financement | Sélectivité | Années de revenu perdues | Cumul 24-45 ans PPA k€ | IA : exposition, palier si IA fort | Dominé sur les 7 dimensions par |
|---|---|---|---|---|---|---|---|---|
| 1 | T30 | 38 ans | Médecine en France + 3 ans en établissement suisse (admission LAMal) | p estimé 7 % | 5,4 | 1057 | faible, S | aucun |
| 2= | T05 | 31 ans | Licence portail santé + 5 ans ; prêt d'installation après collaboration | Places d'odontologie rares ; p estimé 5 % | 5,7 | 1226 | faible, S* | aucun |
| 2= | T91 | 33 ans | Dentaire en France + reconnaissance automatique UE + rachat ou création de cabinet | p estimé 4 % | 5,7 | 1315 | faible, S* | T05 |
| 2= | T15 | 30 ans | CFUO 5 ans (grade master) | 2025 : 3,29 % d'admis ; p estimé 3 % | 5,0 | 478 | faible, S* | aucun |
| 5= | T92 | 34 ans | Dentaire en France + 2 à 3 ans d'advanced standing (environ 250 000 USD à Ohio State, S86) + INBDE + licence d'État + visa | p estimé 2 % | 16,6 | 1173 | faible, A* | aucun |
| 5= | T89 | 31 ans | Comme T83 + 1 an d'expérience + permis B (S90) | p estimé 15 % | 0,5 | 1026 | moyenne, A | aucun |
| 5= | T01 | 35 ans | Licence portail santé (rentrée 2027) puis 9 ans ; internat rémunéré ; bourses | 2 candidatures ; PASS 2024 : 33,8 % admis en 1 an ; p estimé 10 % | 5,4 | 932 | faible, A* | T30 |
| 8= | T37 | 30 ans | Idem T35 + 3 ans d'expérience ; permis G | p estimé 25 % | 0,5 | 1488 | élevée, A | aucun |
| 8= | T82 | 31 ans | Comme T80 + 2 ans d'expérience ; permis G | p estimé 20 % | 0,5 | 1558 | moyenne, A | aucun |
| 8= | T03 | 38 ans | Idem T01 + internat 5 ans + clinicat 2 ans | Spécialité selon rang EDN ; p estimé 9 % | 5,4 | 897 | faible, A | T01, T30 |
| 8= | T46 | 30 ans | Licence de mathématiques + master d'actuariat | p estimé 6 % | 4,0 | 795 | élevée, A | T89 |
| 8= | T90 | 31 ans | Comme T83 + visa de travail (S88) | p estimé 3 % | 0,5 | 1270 | moyenne, A | aucun |
| 8= | T83 | 30 ans | BTS SIO option SISR puis bachelor ou mastère cybersécurité, tout en alternance | Offres cyber +49 % de 2019 à 2024 (ANSSI), 25 000 postes à pourvoir d'ici 2028 (OPIIEC) ; p estimé 25 % | 0,5 | 807 | moyenne, A | T46, T89 |
| 14= | T09 | 31 ans | Licence portail santé + 5 ans (maïeutique en 6 ans) | p estimé 16 % | 5,8 | 586 | faible, A | aucun |
| 14= | T93 | 33 ans | Orthophonie en France + équivalence de master ASHA, Praxis, 36 semaines de clinical fellowship (S89) + visa | p estimé 2 % | 7,4 | 805 | faible, A | aucun |
| 16= | T85 | 28 ans | BUT informatique ou science des données en alternance | p estimé 30 % | 1,1 | 809 | élevée, A* | T46, T83, T89 |
| 16= | T64 | 29 ans | Licence + concours EPSO AD5 (C1 + B2) | 2026 : environ 3 % de réussite ; p estimé 3 % | 3,0 | 1335 | moyenne, A | aucun |
| 16= | T39 | 29 ans | Idem T35 + mobilité | p estimé 25 % | 0,5 | 1075 | élevée, A* | T37 |
| 16= | T71 | 33 ans | Licence + M1 + concours ENM + 31 mois rémunérés | Environ 10,5 % de réussite ; p estimé 8 % | 5,0 | 711 | faible, A | aucun |
| 16= | T16 | 28 ans | Certificat de capacité 3 ans | Sélectif ; p estimé 10 % | 3,0 | 535 | moyenne, A | aucun |
| 21= | T35 | 27 ans | BTS SIO ou BUT en alternance (rémunéré) | Marché junior tendu 2024-2026 ; p estimé 45 % | 0,5 | 745 | élevée, A* | T46, T83, T85, T89 |
| 21= | T10 | 30 ans | Licence portail santé ou STAPS accès kiné + IFMK 4 ans ; IFMK privés 5 à 9 k€/an | Très sélectif ; p estimé 7 % | 5,0 | 659 | faible, A | aucun |
| 21= | T86 | 31 ans | Comme T80 + 2 ans d'expérience + permis B de droit avec un contrat d'au moins un an (S90) | p estimé 15 % | 0,5 | 1102 | moyenne, A | T82, T89 |
| 21= | T81 | 34 ans | Comme T80 + 5 ans salarié | p estimé 25 % | 0,5 | 1107 | moyenne, A | aucun |
| 25= | T42 | 31 ans | Idem T41 + permis G | p estimé 20 % | 1,2 | 1354 | moyenne, A | T30, T37 |
| 25= | T68 | 33 ans | DCG + DSCG en alternance + stage 3 ans + DEC | p estimé 20 % | 0,6 | 946 | moyenne, A | T82 |
| 25= | T41 | 31 ans | BUT puis école d'ingénieurs en apprentissage (29 ans révolus ; dérogation jusqu'à 35 ans en enchaînement) | p estimé 30 % | 1,2 | 736 | moyenne, A | T30, T46, T89 |
| 25= | T40 | 29 ans | Idem T35 + immigration | p estimé 25 % | 0,5 | 940 | élevée, B* | T37, T39, T46, T83, T89 |
| 29= | T43 | 31 ans | Idem T41 + allemand | p estimé 15 % | 1,2 | 927 | moyenne, A | T30, T90 |
| 29= | T02 | 35 ans | Idem T01 | p estimé 10 % | 5,4 | 829 | faible, A | T01, T03, T30 |
| 29= | T76 | 28 ans | DE 3 ans (instituts surtout privés, 6 à 8 k€/an) | p estimé 25 % | 3,8 | 528 | faible, A | aucun |
| 29= | T80 | 29 ans | BTS SIO option SISR en alternance + 2 ans d'administration systèmes + certifications cloud | p estimé 35 % | 0,5 | 897 | moyenne, A* | T46, T82, T83, T86, T89 |
| 33= | T38 | 28 ans | Idem T35 + allemand | p estimé 20 % | 0,5 | 995 | élevée, B | T37, T39, T81, T89, T90 |
| 33= | T77 | 28 ans | DE 3 ans (Parcoursup ou après année santé) | Sélectif ; p estimé 8 % | 3,0 | 515 | faible, A | T16 |
| 33= | T56 | 30 ans | Licence puis CRPE à bac+3 + 2 ans de master rémunérés (1 400 puis 1 800 € net) | p estimé 40 % | 3,1 | 484 | moyenne, A | T09, T30 |
| 33= | T88 | 31 ans | Comme T80 + visa de travail (loterie H-1B pondérée, 100 000 USD à la charge de l'employeur pour un candidat à l'étranger, S88) | p estimé 3 % | 0,5 | 1431 | moyenne, A* | T37, T82 |
| 37= | T34 | 30 ans | Kiné en France + reconnaissance | p estimé 6 % | 5,0 | 1124 | faible, A | aucun |
| 37= | T60 | 29 ans | Licence + concours IRA + 1 an rémunéré | p estimé 10 % | 3,0 | 571 | moyenne, A | T64, T71, T93 |
| 37= | T61 | 29 ans | Licence + concours + ENFiP rémunérée | p estimé 15 % | 3,0 | 646 | moyenne, A | T64, T71, T93 |
| 40= | T36 | 32 ans | Idem T35 + 5 ans salarié | p estimé 30 % | 0,5 | 969 | élevée, B* | T81 |
| 40= | T62 | 26 ans | Concours de niveau bac + formation rémunérée | p estimé 30 % | 0,0 | 603 | moyenne, A | T93 |
| 40= | T20 | 30 ans | Licence + master sélectif | p estimé 20 % | 5,0 | 467 | faible, A | T35, T37, T39, T40, T46, T83, T85, T89 |
| 40= | T63 | 30 ans | Concours externe : moins de 26 ans au 1er janvier, niveau CPGE ; formation rémunérée | Fenêtre 2027-2028 seulement ; p estimé 1 % | 0,0 | 1105 | faible, A | aucun |
| 44= | T78 | 27 ans | BTS diététique ou BUT 2 à 3 ans | p estimé 50 % | 2,0 | 413 | moyenne, B* | T15 |
| 44= | T32 | 35 ans | Médecine en France (DES MG) + ARM + immigration | p estimé 7 % | 5,4 | 1298 | faible, A* | T30 |
| 44= | T57 | 30 ans | Licence puis CAPES à bac+3 + 2 ans rémunérés | p estimé 35 % | 3,1 | 509 | moyenne, A* | T09, T30 |
| 44= | T87 | 31 ans | Comme T80 + anglais courant | p estimé 15 % | 0,5 | 1085 | moyenne, B* | T37, T39, T68, T71, T81, T82, T88, T90 |
| 48= | T70 | 27 ans | BTS CG + emploi au Luxembourg | p estimé 45 % | 0,5 | 915 | élevée, B | T93 |
| 48= | T18 | 28 ans | DE 3 ans | Peu de places ; p estimé 10 % | 3,0 | 604 | faible, A* | aucun |
| 50= | T11 | 30 ans | Idem T10 | p estimé 7 % | 5,0 | 473 | faible, B* | T10, T34 |
| 50= | T67 | 32 ans | Licence + M1 + CRFPA (3 tentatives) + 18 mois | Réussite 25 à 35 % ; p estimé 25 % | 6,5 | 652 | moyenne, B | T37, T64, T68, T82, T88, T90 |
| 52= | T65 | 26 ans | CAST permanent (bac + 3 ans d'expérience, C1 + B2), inscription continue | p estimé 15 % | 0,0 | 827 | élevée, B | T70, T93 |
| 52= | T13 | 30 ans | IFSI + 24 mois d'exercice salarié avant installation | p estimé 22 % | 2,8 | 825 | faible, B* | T01, T03, T05, T30, T91 |
| 54= | T72 | 27 ans | Embauche directe ou BTS NDRC en alternance | p estimé 80 % | 0,5 | 706 | moyenne, B | T30, T37, T38, T39, T40, T41, T42, T43, T46, T81, T83, T85, T89, T90 |
| 54= | T22 | 30 ans | École privée 5 ans, 7 à 10 k€/an (prêt) | Peu sélectif ; marché saturé ; p estimé 65 % | 7,2 | 415 | faible, B | T15, T76 |
| 56= | T69 | 27 ans | BTS CG en alternance | p estimé 75 % | 0,5 | 554 | élevée, B* | T16, T62, T70, T93 |
| 56= | T19 | 32 ans | L2 ou BUT + concours (2 tentatives) + 5 ans ; ou école UE payante | Voie post-bac réservée aux néo-bacheliers ; 46 à 58 places par voie ; p estimé 5 % | 7,0 | 687 | faible, B | T01, T03, T05, T30, T91, T92 |
| 58= | T06 | 31 ans | Licence portail santé + 5 ans | Places de pharmacie souvent non pourvues ; p estimé 25 % | 5,8 | 599 | faible, B | T01, T02, T03, T09, T30, T60, T61, T64, T71, T93 |
| 58= | T29 | 35 ans | Médecine en France + autorisation MEBEKO | p estimé 8 % | 5,4 | 1102 | faible, B | T30, T32, T92 |
| 60 | T45 | 27 ans | BTS SIO ou BUT R&T en alternance | p estimé 60 % | 0,5 | 634 | moyenne, B | T18, T93 |
| 61= | T74 | 28 ans | ATPL intégré (environ 100 k€) ou EPL (condition d'âge non vérifiée) | p estimé 10 % | 8,5 | 1183 | faible, B | T30 |
| 61= | T04 | 38 ans | Idem T03 | p estimé 9 % | 5,4 | 786 | faible, B | T01, T03, T05, T29, T30, T32, T91, T92 |
| 63 | T84 | 27 ans | BTS SIO option SISR en alternance | p estimé 45 % | 0,5 | 708 | élevée, C | T35, T46, T60, T61, T64, T68, T71, T80, T82, T83, T85, T86, T89, T90, T93 |
| 64= | T31 | 35 ans | Médecine en France + allemand C1 (Fachsprachprüfung) | p estimé 6 % | 5,4 | 1244 | faible, B | T05, T29, T30, T32, T91, T92 |
| 64= | T07 | 35 ans | Idem T06 + rachat d'officine (prêt, apport) | p estimé 12 % (financement sans capital) | 5,8 | 769 | faible, B | T01, T03, T30, T32, T37, T42, T43, T64, T67, T68, T81, T82, T88, T90 |
| 64= | T08 | 31 ans | Licence portail santé + 5 ans (maïeutique en 6 ans) | p estimé 18 % | 5,8 | 571 | faible, B | T01, T02, T03, T05, T30, T64, T71, T91, T92, T93 |
| 64= | T14 | 32 ans | IFSI + 2 ans d'exercice + concours + 2 ans (promotion professionnelle rémunérée) | p estimé 9 % | 2,8 | 699 | faible, B | T01, T02, T03, T05, T08, T30, T64, T71, T91, T92, T93 |
| 64= | T79 | 27 ans | BTS OL en alternance | p estimé 70 % | 0,5 | 523 | faible, B | T16, T18, T45, T62, T77, T93 |
| 69= | T24 | 28 ans | IFSI + reconnaissance + permis G | p estimé 22 % | 2,8 | 1312 | faible, B | T01, T03, T05, T30, T64, T91, T92 |
| 69= | T50 | 28 ans | Idem T47 + certificat CCQ + immigration | p estimé 35 % | 0,5 | 832 | faible, B | T10, T34, T93 |
| 69= | T25 | 28 ans | IFSI + autorisation d'exercer (diplôme exempté de reconnaissance) | p estimé 22 % | 2,8 | 1233 | faible, B | T01, T03, T05, T24, T30, T64, T91, T92 |
| 72= | T54 | 26 ans | Formation 14 à 16 mois rémunérée ; résidence près du dépôt | p estimé 15 % | 0,0 | 958 | faible, B | T01, T02, T03, T30, T41, T43, T46, T64, T68, T71, T82, T83, T86, T89, T90, T93 |
| 72= | T26 | 28 ans | IFSI + autorisation d'exercer (diplôme exempté de reconnaissance) | p estimé 22 % | 2,8 | 1083 | faible, B | T01, T03, T05, T19, T24, T25, T30, T34, T64, T91, T92 |
| 72= | T49 | 28 ans | Idem T47 + reconnaissance SEFRI ; permis G | p estimé 45 % | 0,5 | 1103 | faible, B | T34, T93 |
| 72= | T17 | 28 ans | DE ou DTS 3 ans | p estimé 30 % | 3,0 | 576 | faible, B | T01, T02, T03, T05, T06, T09, T30, T56, T60, T61, T64, T71, T91, T92, T93 |
| 76= | T53 | 26 ans | Recrutement + 12 mois de formation rémunérée | Tests psychotechniques ; p estimé 30 % | 0,0 | 685 | faible, B* | T01, T02, T03, T09, T30, T35, T41, T43, T46, T54, T60, T61, T64, T68, T71, T80, T82, T83, T85, T86, T89, T90, T93 |
| 76= | T23 | 28 ans | IFSI + reconnaissance Croix-Rouge suisse (mois) + permis B | p estimé 22 % | 2,8 | 909 | faible, B* | T01, T02, T03, T05, T13, T19, T24, T25, T26, T30, T34, T64, T71, T91, T92, T93 |
| 78= | T47 | 26 ans | Titre professionnel ou CAP adulte en moins d'un an (France Travail, CPF) | p estimé 85 % | 0,5 | 514 | faible, B* | T10, T11, T16, T34, T50, T62, T76, T77, T93 |
| 78= | T28 | 29 ans | IFSI + ARM (stage d'adaptation 75 jours) + immigration | p estimé 18 % | 2,8 | 808 | faible, B* | T01, T02, T03, T05, T10, T13, T19, T23, T24, T25, T26, T30, T34, T64, T71, T91, T92, T93 |
| 80= | T12 | 28 ans | IFSI 3 ans (Parcoursup, ou voie FPC avec 3 ans de cotisations ; Transition Pro possible) | 2025 : 116 000 candidats pour 25 000 places ; p estimé 25 % | 2,8 | 600 | faible, C* | T01, T02, T03, T05, T06, T08, T09, T10, T13, T14, T19, T23, T24, T25, T26, T28, T30, T34, T56, T60, T61, T64, T71, T91, T92, T93 |
| 80= | T52 | 27 ans | CAP ou BTS froid en alternance | p estimé 70 % | 0,5 | 570 | faible, C* | T10, T11, T16, T18, T34, T45, T50, T62, T76, T93 |
| 82= | T73 | 26 ans | Statut d'agent commercial, formation courte | p estimé 50 % (survie) | 0,5 | 465 | moyenne, C | T01, T02, T03, T09, T15, T16, T20, T30, T35, T36, T37, T38, T39, T40, T41, T42, T43, T46, T56, T60, T61, T64, T68, T71, T77, T80, T81, T82, T83, T85, T86, T87, T88, T89, T90, T93, T72 |
| 82= | T27 | 29 ans | IFSI + allemand B2 + Anerkennung | p estimé 12 % | 2,8 | 773 | faible, C | T01, T02, T03, T05, T10, T13, T19, T23, T24, T25, T26, T30, T34, T64, T71, T91, T92, T93 |
| 82= | T66 | 26 ans | École de sous-officiers 8 mois (moins de 32 ans, bac) | p estimé 70 % | 0,0 | 622 | faible, C | T01, T02, T03, T05, T09, T10, T13, T18, T30, T34, T35, T41, T46, T76, T80, T82, T83, T85, T86, T89, T91 |
| 85= | T48 | 31 ans | Idem T47 + 5 ans salarié + création (outillage, véhicule) | p estimé 45 % (survie à 5 ans) | 0,5 | 581 | faible, C | T01, T02, T03, T05, T09, T10, T30, T34, T35, T37, T38, T39, T40, T41, T42, T43, T46, T56, T60, T61, T62, T64, T68, T70, T71, T76, T80, T81, T82, T83, T85, T86, T87, T88, T89, T90, T91, T92, T93, T72 |
| 85= | T51 | 31 ans | CAP adulte + 5 ans salarié + création | p estimé 45 % | 0,5 | 581 | faible, C | T01, T02, T03, T05, T09, T10, T30, T34, T35, T37, T38, T39, T40, T41, T42, T43, T46, T56, T60, T61, T62, T64, T68, T70, T71, T76, T80, T81, T82, T83, T85, T86, T87, T88, T89, T90, T91, T92, T93, T72 |
| 85= | T44 | 27 ans | BTS MS en alternance | p estimé 70 % | 0,5 | 562 | faible, C | T01, T02, T03, T05, T06, T09, T10, T11, T13, T16, T18, T19, T30, T34, T35, T41, T43, T45, T46, T56, T60, T61, T62, T64, T68, T71, T76, T77, T80, T82, T83, T85, T86, T89, T90, T91, T92, T93 |
| 88 | T59 | 27 ans | Volontariat + concours + recrutement par un SDIS | p estimé 8 % | 0,0 | 592 | faible, C | T01, T02, T03, T05, T09, T10, T13, T30, T34, T63, T91 |
| 89 | T58 | 26 ans | Concours (bac) + 12 mois rémunérés (1 570 à 1 617 € net) | p estimé 30 % | 0,0 | 665 | faible, C | T01, T02, T03, T05, T06, T08, T09, T10, T13, T14, T19, T23, T24, T25, T26, T27, T28, T30, T34, T56, T57, T60, T61, T63, T64, T71, T91, T92, T93 |
| 90 | T33 | 26 ans | IFAS + reconnaissance Croix-Rouge suisse | p estimé 55 % | 1,0 | 1084 | faible, C | T01, T02, T03, T05, T13, T19, T24, T25, T26, T30, T34, T41, T43, T46, T63, T64, T68, T71, T82, T86, T89, T90, T91, T92, T93 |
| 91= | T75 | 24 ans | Aucune | p 100 % | 0,0 | 438 | moyenne, C | T01, T02, T03, T05, T06, T09, T15, T16, T17, T18, T20, T30, T35, T37, T38, T39, T40, T41, T42, T43, T45, T46, T53, T54, T56, T57, T60, T61, T62, T64, T65, T67, T68, T69, T70, T71, T76, T77, T79, T80, T81, T82, T83, T85, T86, T87, T88, T89, T90, T91, T92, T93, T72, T74 |
| 91= | T21 | 26 ans | IFAS 1 an (apprentissage possible) | p estimé 75 % | 1,0 | 523 | faible, C | T01, T02, T03, T05, T06, T08, T09, T10, T11, T12, T13, T14, T16, T17, T19, T23, T24, T25, T26, T28, T30, T34, T56, T59, T60, T61, T62, T63, T64, T71, T77, T91, T92, T93 |
| 93 | T55 | 25 ans | Permis C/CE + FIMO (3 mois, financés) | p estimé 85 % | 0,0 | 539 | moyenne, C | T01, T02, T03, T05, T06, T09, T10, T11, T13, T15, T16, T17, T18, T19, T30, T32, T34, T35, T41, T43, T44, T45, T46, T47, T50, T52, T53, T54, T56, T57, T60, T61, T62, T64, T66, T68, T71, T76, T77, T79, T80, T82, T83, T85, T86, T89, T90, T91, T92, T93 |

## 4. Robustesse aux pondérations

### Robustesse : rang dans chacune des 8 configurations de poids

Configurations : poids égaux, puis chaque dimension doublée à son tour. Haut du classement = 10 premiers, rangs partagés compris. Sont listés les triplets présents au moins une fois dans le haut du classement.

| ID | Triplet | égaux | EP×2 | IT×2 | QT×2 | ES×2 | CA×2 | PS×2 | RE×2 | Top 10 (sur 8) |
|---|---|---|---|---|---|---|---|---|---|---|
| T30 | Médecin généraliste × indépendant × Suisse (résident) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 8 |
| T89 | Ingénieur cybersécurité (hors SOC) × salarié × Suisse (résident) | 5 | 3 | 6 | 5 | 5 | 6 | 10 | 10 | 8 |
| T05 | Chirurgien-dentiste × libéral × France | 2 | 17 | 3 | 2 | 2 | 2 | 2 | 2 | 7 |
| T15 | Orthophoniste × libéral × France | 2 | 1 | 1 | 2 | 2 | 2 | 2 | 20 | 7 |
| T91 | Chirurgien-dentiste × libéral × Suisse (résident) | 2 | 17 | 3 | 2 | 2 | 2 | 2 | 2 | 7 |
| T01 | Médecin généraliste × libéral × France | 5 | 17 | 6 | 16 | 5 | 6 | 5 | 5 | 6 |
| T92 | Chirurgien-dentiste × libéral × États-Unis | 5 | 25 | 6 | 5 | 13 | 5 | 5 | 4 | 6 |
| T37 | Développeur × salarié × Suisse (frontalier) | 8 | 3 | 11 | 7 | 5 | 6 | 21 | 5 | 6 |
| T03 | Médecin spécialiste (rang médian) × libéral × France | 8 | 17 | 11 | 16 | 9 | 10 | 7 | 8 | 5 |
| T46 | Actuaire × salarié × France | 8 | 6 | 11 | 7 | 9 | 10 | 15 | 12 | 5 |
| T82 | Ingénieur cloud et DevOps × salarié × Suisse (frontalier) | 8 | 3 | 11 | 16 | 5 | 10 | 15 | 5 | 5 |
| T83 | Ingénieur cybersécurité (hors SOC) × salarié × France | 8 | 6 | 11 | 7 | 9 | 10 | 15 | 16 | 5 |
| T90 | Ingénieur cybersécurité (hors SOC) × salarié × États-Unis | 8 | 6 | 11 | 7 | 20 | 10 | 15 | 8 | 5 |
| T09 | Sage-femme × libéral × France | 14 | 23 | 17 | 11 | 9 | 6 | 7 | 23 | 3 |
| T93 | Orthophoniste × salarié × États-Unis | 14 | 6 | 3 | 22 | 20 | 17 | 7 | 12 | 3 |
| T16 | Orthoptiste × salarié × France | 16 | 10 | 6 | 27 | 13 | 29 | 10 | 35 | 3 |
| T64 | Administrateur UE (AD) × fonctionnaire européen × Luxembourg (résident) | 16 | 10 | 18 | 25 | 25 | 23 | 10 | 10 | 3 |
| T71 | Magistrat × fonctionnaire × France | 16 | 10 | 22 | 27 | 29 | 17 | 10 | 16 | 2 |
| T10 | Masseur-kinésithérapeute × libéral × France | 21 | 45 | 6 | 12 | 13 | 15 | 10 | 23 | 2 |
| T39 | Développeur × salarié × Luxembourg (frontalier) | 16 | 10 | 18 | 12 | 13 | 17 | 36 | 16 | 1 |
| T85 | Data engineer × salarié × France | 16 | 10 | 18 | 12 | 13 | 17 | 19 | 23 | 1 |
| T35 | Développeur × salarié × France | 21 | 10 | 22 | 12 | 13 | 17 | 21 | 32 | 1 |
| T86 | Ingénieur cloud et DevOps × salarié × Suisse (résident) | 21 | 10 | 22 | 27 | 13 | 17 | 21 | 20 | 1 |

### Noyau robuste et triplets fragiles

- Dans le haut du classement dans les 8 configurations : T30 Médecin généraliste × indépendant × Suisse (résident), T89 Ingénieur cybersécurité (hors SOC) × salarié × Suisse (résident).
- Dans le haut du classement dans les 4 configurations citées dans la demande (poids égaux, revenu, autonomie et sécurité doublés) : T30 Médecin généraliste × indépendant × Suisse (résident), T05 Chirurgien-dentiste × libéral × France, T91 Chirurgien-dentiste × libéral × Suisse (résident), T92 Chirurgien-dentiste × libéral × États-Unis, T89 Ingénieur cybersécurité (hors SOC) × salarié × Suisse (résident), T01 Médecin généraliste × libéral × France, T03 Médecin spécialiste (rang médian) × libéral × France.
- Dans le haut du classement dans une seule configuration : T85 Data engineer × salarié × France (EP×2), T39 Développeur × salarié × Luxembourg (frontalier) (EP×2), T35 Développeur × salarié × France (EP×2), T86 Ingénieur cloud et DevOps × salarié × Suisse (résident) (EP×2).

### Sensibilité aux notes en tension (informatif, hors classement)

Poids égaux ; chaque note en tension avec un chiffre de statut M prend la valeur compatible avec ce chiffre (partie C2). Les autres triplets gardent leur score.

| ID | Triplet | Note en tension | Rang v5 | Rang si chiffre appliqué | Palier v5 | Palier si chiffre appliqué |
|---|---|---|---|---|---|---|
| T15 | Orthophoniste × libéral × France | ES (S2) | 2= | 7= | S* | A |
| T09 | Sage-femme × libéral × France | ES (S2) | 14= | 21= | A | A |
| T93 | Orthophoniste × salarié × États-Unis | ES (S2) | 14= | 21= | A | A |
| T16 | Orthoptiste × salarié × France | ES (S2) | 16= | 31= | A | A |
| T10 | Masseur-kinésithérapeute × libéral × France | ES (S2) | 21= | 31= | A | A |
| T76 | Pédicure-podologue × libéral × France | ES (S2) | 29= | 40= | A | A |
| T77 | Ergothérapeute × fonctionnaire FPH × France | ES (S2) | 33= | 42= | A | A |
| T34 | Masseur-kinésithérapeute × salarié × Suisse (frontalier) | ES (S2) | 37= | 46 | A | A |
| T36 | Développeur × indépendant (freelance) × France | PS (P3) | 40= | 27= | A | A |
| T78 | Diététicien × libéral × France | ES (S2) | 44= | 48= | A | B |
| T18 | Audioprothésiste × salarié × France | ES (S2) | 48= | 51= | A* | B |
| T11 | Masseur-kinésithérapeute × fonctionnaire FPH × France | ES (S2) | 50= | 54= | B* | B |
| T13 | Infirmier × libéral × France | ES (S2) | 52= | 59= | B* | B |
| T08 | Sage-femme × fonctionnaire FPH × France | EP (E6) | 64= | 73= | B | B |
| T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | EP (E6) | 64= | 73= | B | B |
| T54 | Conducteur de train × salarié × Suisse (résident) | EP (E5) | 72= | 83= | B | C |
| T53 | Conducteur de train × salarié (SNCF) × France | EP (E5) | 76= | 87= | B* | C |
| T75 | Employé commerce ou accueil (référence) × salarié × France | QT (Q8) | 91= | 89= | C | C |

## 5. Égalités et frontières de palier

### Égalités déclarées (écart inférieur à 0,03 avec le premier du groupe)

rang 2 : T05 = T91 = T15 ; rang 5 : T92 = T89 = T01 ; rang 8 : T37 = T82 = T03 = T46 = T90 = T83 ; rang 14 : T09 = T93 ; rang 16 : T85 = T64 = T39 = T71 = T16 ; rang 21 : T35 = T10 = T86 = T81 ; rang 25 : T42 = T68 = T41 = T40 ; rang 29 : T43 = T02 = T76 = T80 ; rang 33 : T38 = T77 = T56 = T88 ; rang 37 : T34 = T60 = T61 ; rang 40 : T36 = T62 = T20 = T63 ; rang 44 : T78 = T32 = T57 = T87 ; rang 48 : T70 = T18 ; rang 50 : T11 = T67 ; rang 52 : T65 = T13 ; rang 54 : T72 = T22 ; rang 56 : T69 = T19 ; rang 58 : T06 = T29 ; rang 61 : T74 = T04 ; rang 64 : T31 = T07 = T08 = T14 = T79 ; rang 69 : T24 = T50 = T25 ; rang 72 : T54 = T26 = T49 = T17 ; rang 76 : T53 = T23 ; rang 78 : T47 = T28 ; rang 80 : T12 = T52 ; rang 82 : T73 = T27 = T66 ; rang 85 : T48 = T51 = T44 ; rang 91 : T75 = T21

### À moins de 0,1 d'une frontière de palier

T05 (S), T91 (S), T15 (S), T92 (A), T89 (A), T01 (A), T32 (A), T57 (A), T87 (A), T70 (A), T18 (A), T11 (B), T67 (B), T65 (B), T13 (B), T53 (B), T23 (B), T47 (B), T28 (B), T12 (C), T52 (C)

## 6. Conversion des notes v4 vers les dimensions Eurofound, triplet par triplet

Facteurs de l'ancienne charge : F1 plus de 45 h, F2 intensité ou exigences émotionnelles, F3 nuits, week-ends ou astreintes, F4 pénibilité physique, F5 trajet (hors grille). H = horaires imposés (contrôle v4 de 3 ou moins).

ES reprend les relations v4 et PS la sécurité v4, sauf note modifiée par un ancrage de statut S (code entre parenthèses).

| ID | Groupe de métiers | Facteurs | Charge v4 | Contrôle v4 | H | CITP-08 (niveau) | EP | IT | QT | CA | Relations v4 → ES | Sécurité v4 → PS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T01 | médecin cabinet | F1 F2 | 3 | 4 | 0 | 2211 (4) | 4 | 3 | 4 | 4,5 | 4 → 4 | 5 → 5 |
| T02 | médecin cabinet | F2 | 4 | 3 | 1 | 2211 (4) | 4 | 3 | 4 | 4 | 4 → 4 | 5 → 5 |
| T03 | médecin cabinet | F1 F2 | 3 | 4 | 0 | 2212 (4) | 4 | 3 | 4 | 4,5 | 4 → 4 | 5 → 5 |
| T04 | médecin hôpital | F1 F2 F3 | 2 | 3 | 1 | 2212 (4) | 3 | 2 | 2 | 4 | 3 → 3 | 5 → 5 |
| T05 | dentiste | F2 F4 | 3 | 5 | 0 | 2261 (4) | 3 | 3 | 5 | 5 | 4 → 4 | 5 → 5 |
| T06 | pharmacien | F2 F3 F4 | 2 | 2 | 1 | 2262 (4) | 4 | 3 | 3 | 3,5 | 3 → 3 | 5 → 5 |
| T07 | pharmacien | F1 F2 F3 | 2 | 3 | 1 | 2262 (4) | 4 | 3 | 2 | 4 | 3 → 3 | 3 → 3 |
| T08 | sage femme hôpital | F2 F3 | 3 | 3 | 1 | 2222 (4) | 3 | 2 | 3 | 4 | 3 → 3 | 5 → 5 |
| T09 | sage femme cabinet | F2 | 4 | 5 | 0 | 2222 (4) | 4 | 3 | 5 | 5 | 4 → 4 | 5 → 5 |
| T10 | kine | F4 | 3 | 5 | 0 | 2264 (4) | 2 | 4 | 5 | 5 | 4 → 4 | 5 → 5 |
| T11 | kine | F4 | 4 | 3 | 1 | 2264 (4) | 2 | 4 | 4 | 4 | 4 → 4 | 5 → 5 |
| T12 | infirmier hôpital | F2 F3 F4 | 2 | 2 | 1 | 2221 (4) | 2 | 2 | 3 | 3,5 | 3 → 3 | 5 → 5 |
| T13 | infirmier domicile | F1 F2 F3 | 2 | 4 | 0 | 2221 (4) | 2 | 3 | 3 | 4,5 | 4 → 4 | 5 → 5 |
| T14 | iade | F2 F3 | 3 | 3 | 1 | 2221 (4) | 3 | 2 | 3 | 4 | 3 → 3 | 5 → 5 |
| T15 | orthophoniste | aucun | 5 | 5 | 0 | 2266 (4) | 5 | 4 | 5 | 5 | 4 → 4 | 5 → 5 |
| T16 | orthoptiste | F2 | 4 | 3 | 1 | 2267 (4) | 5 | 4 | 4 | 4 | 4 → 4 | 5 → 5 |
| T17 | manipulateur radio | F3 | 4 | 2 | 1 | 3211 (3) | 3 | 3 | 3 | 2,8 | 3 → 3 | 5 → 5 |
| T18 | audio optique | F3 | 4 | 3 | 1 | 2266 (4) | 4 | 4 | 3 | 4 | 4 → 4 | 4 → 4 |
| T19 | veterinaire | F1 F3 F4 | 2 | 4 | 0 | 2250 (4) | 2 | 3 | 3 | 4,5 | 3 → 3 | 5 → 5 |
| T20 | psychologue | F2 | 4 | 4 | 0 | 2634 (4) | 5 | 3 | 5 | 4,5 | 4 → 4 | 3 → 3 |
| T21 | aide soignant | F2 F3 F4 | 2 | 1 | 1 | 5321 (2) | 1 | 2 | 3 | 1,7 | 3 → 3 | 5 → 5 |
| T22 | osteo podologue | F4 | 4 | 5 | 0 | 2230 (4) | 3 | 4 | 5 | 5 | 4 → 4 | 2 → 2 |
| T23 | infirmier hôpital | F2 F3 F4 | 2 | 2 | 1 | 2221 (4) | 2 | 2 | 3 | 3,5 | 3 → 3 | 5 → 5 |
| T24 | infirmier hôpital | F2 F3 F4 F5 | 1 | 2 | 1 | 2221 (4) | 2 | 2 | 3 | 3,5 | 3 → 3 | 5 → 5 |
| T25 | infirmier hôpital | F2 F3 F4 F5 | 1 | 2 | 1 | 2221 (4) | 2 | 2 | 3 | 3,5 | 3 → 3 | 5 → 5 |
| T26 | infirmier hôpital | F2 F3 F4 | 2 | 2 | 1 | 2221 (4) | 2 | 2 | 3 | 3,5 | 3 → 3 | 5 → 5 |
| T27 | infirmier hôpital | F2 F3 F4 | 2 | 2 | 1 | 2221 (4) | 2 | 2 | 3 | 3,5 | 2 → 2 | 5 → 5 |
| T28 | infirmier hôpital | F2 F3 F4 | 2 | 2 | 1 | 2221 (4) | 2 | 2 | 3 | 3,5 | 3 → 3 | 5 → 5 |
| T29 | médecin hôpital | F1 F2 F3 | 2 | 3 | 1 | 2212 (4) | 3 | 2 | 2 | 4 | 3 → 3 | 5 → 5 |
| T30 | médecin cabinet | F2 | 3 | 4 | 0 | 2211 (4) | 4 | 3 | 5 | 4,5 | 4 → 4 | 5 → 5 |
| T31 | médecin hôpital | F1 F2 F3 | 2 | 3 | 1 | 2212 (4) | 3 | 2 | 2 | 4 | 2 → 2 | 5 → 5 |
| T32 | médecin cabinet | F1 F2 F3 | 2 | 3 | 1 | 2211 (4) | 4 | 3 | 2 | 4 | 3 → 3 | 5 → 5 |
| T33 | aide soignant | F2 F3 F4 F5 | 1 | 1 | 1 | 5321 (2) | 1 | 2 | 3 | 1,7 | 3 → 3 | 4 → 4 |
| T34 | kine | F4 F5 | 3 | 3 | 1 | 2264 (4) | 2 | 4 | 4 | 4 | 4 → 4 | 5 → 5 |
| T35 | informatique | F2 | 4 | 4 | 0 | 2512 (4) | 5 | 3 | 5 | 4,5 | 4 → 4 | 3 → 4 (P3) |
| T36 | informatique | F2 | 4 | 5 | 0 | 2512 (4) | 5 | 3 | 5 | 5 | 3 → 3 | 2 → 2 |
| T37 | informatique | F2 F5 | 3 | 4 | 0 | 2512 (4) | 5 | 3 | 5 | 4,5 | 4 → 4 | 3 → 3 |
| T38 | informatique | F2 | 4 | 4 | 0 | 2512 (4) | 5 | 3 | 5 | 4,5 | 3 → 3 | 3 → 3 |
| T39 | informatique | F2 F5 | 3 | 4 | 0 | 2512 (4) | 5 | 3 | 5 | 4,5 | 4 → 4 | 3 → 3 |
| T40 | informatique | F2 | 4 | 4 | 0 | 2512 (4) | 5 | 3 | 5 | 4,5 | 4 → 4 | 3 → 3 |
| T41 | ingenieur industrie | F2 | 4 | 4 | 0 | 2141 (4) | 4 | 3 | 5 | 4,5 | 4 → 4 | 4 → 4 |
| T42 | ingenieur industrie | F2 F5 | 3 | 4 | 0 | 2141 (4) | 4 | 3 | 5 | 4,5 | 4 → 4 | 3 → 3 |
| T43 | ingenieur industrie | F2 | 4 | 4 | 0 | 2141 (4) | 4 | 3 | 5 | 4,5 | 3 → 3 | 4 → 4 |
| T44 | technicien maintenance | F3 F4 | 3 | 3 | 1 | 3115 (3) | 2 | 3 | 3 | 3,3 | 3 → 3 | 4 → 4 |
| T45 | technicien réseaux | F3 | 4 | 3 | 1 | 3513 (3) | 4 | 4 | 3 | 3,3 | 3 → 3 | 4 → 4 |
| T46 | bureau cadre | F2 | 4 | 4 | 0 | 2120 (4) | 5 | 3 | 5 | 4,5 | 4 → 4 | 4 → 4 |
| T47 | batiment electricite | F4 | 4 | 3 | 1 | 7411 (2) | 2 | 4 | 4 | 2,7 | 3 → 3 | 4 → 4 |
| T48 | artisan batiment | F1 F2 F4 | 2 | 4 | 0 | 7411 (2) | 2 | 3 | 4 | 3,2 | 3 → 3 | 3 → 3 |
| T49 | batiment electricite | F4 F5 | 3 | 3 | 1 | 7411 (2) | 2 | 4 | 4 | 2,7 | 3 → 3 | 3 → 3 |
| T50 | batiment electricite | F4 | 4 | 3 | 1 | 7411 (2) | 2 | 4 | 4 | 2,7 | 3 → 3 | 4 → 4 |
| T51 | artisan batiment | F1 F2 F4 | 2 | 4 | 0 | 7126 (2) | 2 | 3 | 4 | 3,2 | 3 → 3 | 3 → 3 |
| T52 | batiment electricite | F3 F4 | 3 | 3 | 1 | 7127 (2) | 2 | 4 | 3 | 2,7 | 3 → 3 | 4 → 4 |
| T53 | conducteur train | F3 F5 | 3 | 2 | 1 | 8311 (2) | 4 | 3 | 3 | 2,2 | 3 → 3 | 4 → 4 |
| T54 | conducteur train | F2 F3 | 3 | 2 | 1 | 8311 (2) | 4 | 3 | 3 | 2,2 | 3 → 3 | 4 → 4 |
| T55 | conducteur routier | F1 F3 F4 F5 | 1 | 2 | 1 | 8332 (2) | 2 | 3 | 2 | 2,2 | 2 → 2 | 4 → 4 |
| T56 | enseignant | F2 | 4 | 4 | 0 | 2341 (4) | 4 | 3 | 5 | 4,5 | 3 → 3 | 5 → 5 |
| T57 | enseignant | F2 | 4 | 4 | 0 | 2330 (4) | 4 | 3 | 5 | 4,5 | 3 → 2 (S3) | 5 → 5 |
| T58 | police | F2 F3 F4 | 2 | 2 | 1 | 5412 (2) | 2 | 2 | 3 | 2,2 | 2 → 2 | 5 → 5 |
| T59 | pompier | F2 F3 F4 | 2 | 2 | 1 | 5411 (2) | 1 | 2 | 3 | 2,2 | 4 → 4 | 5 → 5 |
| T60 | bureau cadre | F2 | 4 | 3 | 1 | 2422 (4) | 5 | 3 | 4 | 4 | 3 → 3 | 5 → 5 |
| T61 | bureau cadre | F2 | 4 | 3 | 1 | 2411 (4) | 5 | 3 | 4 | 4 | 3 → 3 | 5 → 5 |
| T62 | bureau non cadre | aucun | 5 | 3 | 1 | 3352 (3) | 5 | 4 | 4 | 3,3 | 3 → 3 | 5 → 5 |
| T63 | contrôleur aérien | F2 F3 | 3 | 2 | 1 | 3154 (3) | 5 | 2 | 3 | 2,8 | 4 → 4 | 5 → 5 |
| T64 | bureau cadre | F2 | 4 | 3 | 1 | 2422 (4) | 5 | 3 | 4 | 4 | 3 → 3 | 5 → 5 |
| T65 | bureau non cadre | F5 | 4 | 2 | 1 | 3343 (3) | 5 | 4 | 4 | 2,8 | 3 → 3 | 3 → 3 |
| T66 | militaire | F3 F4 F5 | 2 | 2 | 1 | 0210 (2) | 2 | 3 | 3 | 2,2 | 4 → 4 | 4 → 4 |
| T67 | bureau cadre | F1 F2 | 3 | 3 | 1 | 2611 (4) | 5 | 3 | 3 | 4 | 3 → 3 | 3 → 3 |
| T68 | bureau cadre | F1 F2 | 3 | 4 | 0 | 2411 (4) | 5 | 3 | 4 | 4,5 | 3 → 3 | 4 → 4 |
| T69 | bureau non cadre | aucun | 5 | 3 | 1 | 3313 (3) | 5 | 4 | 4 | 3,3 | 3 → 3 | 3 → 3 |
| T70 | bureau non cadre | F5 | 4 | 3 | 1 | 3313 (3) | 5 | 4 | 4 | 3,3 | 3 → 3 | 3 → 3 |
| T71 | bureau cadre | F1 F2 | 3 | 4 | 0 | 2612 (4) | 5 | 3 | 4 | 4,5 | 3 → 3 | 5 → 5 |
| T76 | osteo podologue | F4 | 4 | 5 | 0 | 2269 (4) | 3 | 4 | 5 | 5 | 4 → 4 | 4 → 4 |
| T77 | ergothérapeute | aucun | 5 | 3 | 1 | 2269 (4) | 4 | 4 | 4 | 4 | 4 → 4 | 5 → 5 |
| T78 | dieteticien | aucun | 5 | 4 | 0 | 2265 (4) | 5 | 4 | 5 | 4,5 | 4 → 4 | 2 → 2 |
| T79 | audio optique | F3 | 4 | 2 | 1 | 3254 (3) | 4 | 4 | 3 | 2,8 | 3 → 3 | 4 → 4 |
| T80 | informatique | F2 F3 | 3 | 4 | 0 | 2522 (4) | 5 | 3 | 4 | 4,5 | 4 → 4 | 4 → 4 |
| T81 | informatique | F2 | 4 | 5 | 0 | 2522 (4) | 5 | 3 | 5 | 5 | 3 → 3 | 3 → 3 |
| T82 | informatique | F2 F3 F5 | 2 | 4 | 0 | 2522 (4) | 5 | 3 | 4 | 4,5 | 4 → 4 | 4 → 4 |
| T83 | informatique | F2 | 4 | 4 | 0 | 2529 (4) | 5 | 3 | 5 | 4,5 | 4 → 4 | 4 → 4 |
| T84 | soc | F2 F3 | 3 | 2 | 1 | 2529 (4) | 5 | 2 | 3 | 3,5 | 3 → 3 | 4 → 4 |
| T85 | informatique | F2 | 4 | 4 | 0 | 2521 (4) | 5 | 3 | 5 | 4,5 | 4 → 4 | 3 → 4 (P3) |
| T86 | informatique | F2 F3 | 3 | 4 | 0 | 2522 (4) | 5 | 3 | 4 | 4,5 | 4 → 4 | 4 → 4 |
| T87 | informatique | F2 F3 | 3 | 4 | 0 | 2522 (4) | 5 | 3 | 4 | 4,5 | 3 → 3 | 3 → 3 |
| T88 | informatique | F2 F3 | 3 | 4 | 0 | 2522 (4) | 5 | 3 | 4 | 4,5 | 3 → 3 | 3 → 3 |
| T89 | informatique | F2 | 4 | 4 | 0 | 2529 (4) | 5 | 3 | 5 | 4,5 | 4 → 4 | 4 → 4 |
| T90 | informatique | F2 | 4 | 4 | 0 | 2529 (4) | 5 | 3 | 5 | 4,5 | 3 → 3 | 4 → 4 |
| T91 | dentiste | F2 F4 | 3 | 5 | 0 | 2261 (4) | 3 | 3 | 5 | 5 | 4 → 4 | 5 → 5 |
| T92 | dentiste | F2 F4 | 3 | 5 | 0 | 2261 (4) | 3 | 3 | 5 | 5 | 3 → 3 | 5 → 5 |
| T93 | orthophoniste | aucun | 5 | 3 | 1 | 2266 (4) | 5 | 4 | 4 | 4 | 3 → 3 | 5 → 5 |
| T72 | commercial immobilier | F2 F5 | 3 | 4 | 0 | 3322 (3) | 4 | 3 | 5 | 3,8 | 3 → 3 | 3 → 3 |
| T73 | commercial immobilier | F2 F3 | 3 | 4 | 0 | 3334 (3) | 4 | 3 | 4 | 3,8 | 3 → 3 | 1 → 1 |
| T74 | pilote | F2 F3 F5 | 2 | 2 | 1 | 3153 (3) | 4 | 3 | 3 | 2,8 | 3 → 3 | 3 → 3 |
| T75 | employe commerce | F3 F4 | 3 | 2 | 1 | 5223 (2) | 3 | 3 | 3 | 2,2 | 2 → 2 | 3 → 3 |

## 7. Modifications de rang par rapport à la version 4

Chaque bloc compare la contribution d'un groupe de critères au score v5 et au score v4, par rapport à la moyenne des 93 triplets : un nombre positif fait monter le triplet. Les deux blocs les plus forts sont indiqués.

| ID | Triplet | Rang v4 | Rang v5 | Variation | Ce qui l'explique |
|---|---|---|---|---|---|
| T30 | Médecin généraliste × indépendant × Suisse (résident) | 5= | 1 | +4 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,24) ; sens retiré (-0,07) |
| T05 | Chirurgien-dentiste × libéral × France | 1= | 2= | -1 | autonomie et compétences (CA ; ancien contrôle) (-0,21) ; conditions de travail (EP, IT, QT ; ancienne charge) (+0,09) |
| T91 | Chirurgien-dentiste × libéral × Suisse (résident) | 1= | 2= | -1 | autonomie et compétences (CA ; ancien contrôle) (-0,21) ; conditions de travail (EP, IT, QT ; ancienne charge) (+0,09) |
| T15 | Orthophoniste × libéral × France | 3= | 2= | +1 | autonomie et compétences (CA ; ancien contrôle) (-0,21) ; conditions de travail (EP, IT, QT ; ancienne charge) (+0,14) |
| T92 | Chirurgien-dentiste × libéral × États-Unis | 3= | 5= | -2 | autonomie et compétences (CA ; ancien contrôle) (-0,21) ; conditions de travail (EP, IT, QT ; ancienne charge) (+0,09) |
| T89 | Ingénieur cybersécurité (hors SOC) × salarié × Suisse (résident) | 7= | 5= | +2 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; lieu (télétravail) retiré (-0,14) |
| T01 | Médecin généraliste × libéral × France | 7= | 5= | +2 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,09) ; sens retiré (-0,07) |
| T37 | Développeur × salarié × Suisse (frontalier) | 23= | 8= | +15 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,38) ; lieu (télétravail) retiré (-0,14) |
| T82 | Ingénieur cloud et DevOps × salarié × Suisse (frontalier) | 27= | 8= | +19 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,43) ; lieu (télétravail) retiré (-0,14) |
| T03 | Médecin spécialiste (rang médian) × libéral × France | 7= | 8= | -1 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,09) ; sens retiré (-0,07) |
| T46 | Actuaire × salarié × France | 16= | 8= | +8 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; lieu (télétravail) retiré (-0,14) |
| T90 | Ingénieur cybersécurité (hors SOC) × salarié × États-Unis | 12= | 8= | +4 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; lieu (télétravail) retiré (-0,14) |
| T83 | Ingénieur cybersécurité (hors SOC) × salarié × France | 12= | 8= | +4 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; lieu (télétravail) retiré (-0,14) |
| T09 | Sage-femme × libéral × France | 5= | 14= | -9 | autonomie et compétences (CA ; ancien contrôle) (-0,21) ; sens retiré (-0,07) |
| T85 | Data engineer × salarié × France | 27= | 16= | +11 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; perspectives et sécurité (PS) (+0,15) |
| T39 | Développeur × salarié × Luxembourg (frontalier) | 42= | 16= | +26 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,38) ; lieu (télétravail) retiré (-0,06) |
| T71 | Magistrat × fonctionnaire × France | 23= | 16= | +7 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,24) ; sens retiré (-0,07) |
| T16 | Orthoptiste × salarié × France | 48= | 16= | +32 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; lieu (télétravail) retiré (+0,10) |
| T35 | Développeur × salarié × France | 31= | 21= | +10 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; perspectives et sécurité (PS) (+0,15) |
| T10 | Masseur-kinésithérapeute × libéral × France | 7= | 21= | -14 | autonomie et compétences (CA ; ancien contrôle) (-0,21) ; conditions de travail (EP, IT, QT ; ancienne charge) (+0,09) |
| T81 | Ingénieur cloud et DevOps × indépendant (freelance) × France | 7= | 21= | -14 | lieu (télétravail) retiré (-0,22) ; autonomie et compétences (CA ; ancien contrôle) (-0,21) |
| T42 | Ingénieur méthodes-industrialisation × salarié × Suisse (frontalier) | 42= | 25= | +17 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,24) ; autonomie et compétences (CA ; ancien contrôle) (-0,06) |
| T68 | Expert-comptable × libéral × France | 33= | 25= | +8 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,24) ; lieu (télétravail) retiré (-0,06) |
| T41 | Ingénieur méthodes-industrialisation × salarié × France | 23= | 25= | -2 | autonomie et compétences (CA ; ancien contrôle) (-0,06) ; sens retiré (+0,05) |
| T40 | Développeur × salarié × Canada (Québec) | 23= | 25= | -2 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; lieu (télétravail) retiré (-0,14) |
| T43 | Ingénieur méthodes-industrialisation × salarié × Allemagne | 33= | 29= | +4 | autonomie et compétences (CA ; ancien contrôle) (-0,06) ; revenu (RE, équivalent temps plein) (+0,06) |
| T02 | Médecin généraliste × salarié (centre de santé) × France | 21= | 29= | -8 | lieu (télétravail) retiré (+0,10) ; conditions de travail (EP, IT, QT ; ancienne charge) (-0,10) |
| T76 | Pédicure-podologue × libéral × France | 14= | 29= | -15 | autonomie et compétences (CA ; ancien contrôle) (-0,21) ; conditions de travail (EP, IT, QT ; ancienne charge) (+0,05) |
| T80 | Ingénieur cloud et DevOps × salarié × France | 31= | 29= | +2 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,24) ; lieu (télétravail) retiré (-0,14) |
| T77 | Ergothérapeute × fonctionnaire FPH × France | 27= | 33= | -6 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,14) ; lieu (télétravail) retiré (+0,10) |
| T56 | Professeur des écoles × fonctionnaire × France | 19= | 33= | -14 | sens retiré (-0,07) ; lieu (télétravail) retiré (-0,06) |
| T88 | Ingénieur cloud et DevOps × salarié × États-Unis | 37= | 33= | +4 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,24) ; lieu (télétravail) retiré (-0,14) |
| T60 | Attaché d'administration × fonctionnaire × France | 42= | 37= | +5 | lieu (télétravail) retiré (-0,14) ; autonomie et compétences (CA ; ancien contrôle) (+0,09) |
| T36 | Développeur × indépendant (freelance) × France | 19= | 40= | -21 | lieu (télétravail) retiré (-0,22) ; autonomie et compétences (CA ; ancien contrôle) (-0,21) |
| T62 | Contrôleur des finances publiques × fonctionnaire × France | 27= | 40= | -13 | lieu (télétravail) retiré (-0,14) ; sens retiré (+0,05) |
| T20 | Psychologue × contractuel FPH × France | 37= | 40= | -3 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; sens retiré (-0,07) |
| T63 | Contrôleur aérien (ICNA) × fonctionnaire × France | 54= | 40= | +14 | autonomie et compétences (CA ; ancien contrôle) (+0,14) ; revenu (RE, équivalent temps plein) (+0,11) |
| T78 | Diététicien × libéral × France | 45= | 44= | +1 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,14) ; lieu (télétravail) retiré (-0,06) |
| T32 | Médecin de famille × libéral (RAMQ) × Canada (Québec) | 45= | 44= | +1 | autonomie et compétences (CA ; ancien contrôle) (+0,09) ; sens retiré (-0,07) |
| T57 | Professeur certifié × fonctionnaire × France | 16= | 44= | -28 | environnement social (ES ; anciennes relations) (-0,14) ; sens retiré (-0,07) |
| T87 | Ingénieur cloud et DevOps × salarié × Irlande | 48= | 44= | +4 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,24) ; lieu (télétravail) retiré (-0,14) |
| T70 | Comptable × salarié × Luxembourg (frontalier) | 59= | 48= | +11 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; sens retiré (+0,11) |
| T18 | Audioprothésiste × salarié × France | 52= | 48= | +4 | lieu (télétravail) retiré (+0,10) ; conditions de travail (EP, IT, QT ; ancienne charge) (-0,10) |
| T11 | Masseur-kinésithérapeute × fonctionnaire FPH × France | 45= | 50= | -5 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,24) ; lieu (télétravail) retiré (+0,10) |
| T67 | Avocat × libéral × France | 59= | 50= | +9 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,09) ; autonomie et compétences (CA ; ancien contrôle) (+0,09) |
| T65 | Agent contractuel UE (GF II-III) × contractuel × Luxembourg (frontalier) | 64= | 52= | +12 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,19) ; lieu (télétravail) retiré (-0,14) |
| T13 | Infirmier × libéral × France | 33= | 52= | -19 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,14) ; sens retiré (-0,07) |
| T72 | Commercial B2B × salarié × France | 63 | 54= | +9 | conditions de travail (EP, IT, QT ; ancienne charge) (+0,24) ; autonomie et compétences (CA ; ancien contrôle) (-0,16) |
| T22 | Ostéopathe × libéral × France | 37= | 54= | -17 | autonomie et compétences (CA ; ancien contrôle) (-0,21) ; revenu (RE, équivalent temps plein) (-0,12) |
| T69 | Comptable × salarié × France | 52= | 56= | -4 | lieu (télétravail) retiré (-0,14) ; sens retiré (+0,05) |
| T19 | Vétérinaire × libéral × France | 48= | 56= | -8 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,14) ; autonomie et compétences (CA ; ancien contrôle) (-0,06) |
| T06 | Pharmacien adjoint × salarié × France | 83 | 58= | +25 | autonomie et compétences (CA ; ancien contrôle) (+0,24) ; conditions de travail (EP, IT, QT ; ancienne charge) (+0,14) |
| T29 | Médecin × salarié (hôpital) × Suisse (résident) | 51 | 58= | -7 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,29) ; lieu (télétravail) retiré (+0,10) |
| T45 | Technicien réseaux et cybersécurité × salarié × France | 54= | 60 | -6 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,10) ; lieu (télétravail) retiré (-0,06) |
| T74 | Pilote de ligne × salarié × France | 88 | 61= | +27 | autonomie et compétences (CA ; ancien contrôle) (+0,14) ; conditions de travail (EP, IT, QT ; ancienne charge) (+0,14) |
| T04 | Praticien hospitalier × statut PH (public) × France | 54= | 61= | -7 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,29) ; lieu (télétravail) retiré (+0,10) |
| T84 | Analyste SOC (cybersécurité) × salarié × France | 72= | 63 | +9 | autonomie et compétences (CA ; ancien contrôle) (+0,24) ; conditions de travail (EP, IT, QT ; ancienne charge) (-0,05) |
| T31 | Médecin × salarié (hôpital) × Allemagne | 57= | 64= | -7 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,29) ; lieu (télétravail) retiré (+0,10) |
| T07 | Pharmacien titulaire × indépendant × France | 69= | 64= | +5 | autonomie et compétences (CA ; ancien contrôle) (+0,09) ; lieu (télétravail) retiré (+0,02) |
| T08 | Sage-femme × fonctionnaire FPH × France | 59= | 64= | -5 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,33) ; lieu (télétravail) retiré (+0,10) |
| T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | 59= | 64= | -5 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,33) ; lieu (télétravail) retiré (+0,10) |
| T79 | Opticien × salarié × France | 81= | 64= | +17 | autonomie et compétences (CA ; ancien contrôle) (+0,14) ; lieu (télétravail) retiré (+0,10) |
| T24 | Infirmier × salarié × Suisse (frontalier) | 76= | 69= | +7 | autonomie et compétences (CA ; ancien contrôle) (+0,24) ; lieu (télétravail) retiré (+0,10) |
| T50 | Électricien × salarié × Canada (Québec) | 57= | 69= | -12 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,24) ; autonomie et compétences (CA ; ancien contrôle) (-0,10) |
| T25 | Infirmier × salarié × Luxembourg (frontalier) | 76= | 69= | +7 | autonomie et compétences (CA ; ancien contrôle) (+0,24) ; lieu (télétravail) retiré (+0,10) |
| T54 | Conducteur de train × salarié × Suisse (résident) | 76= | 72= | +4 | lieu (télétravail) retiré (+0,10) ; conditions de travail (EP, IT, QT ; ancienne charge) (-0,05) |
| T26 | Infirmier × salarié × Luxembourg (résident) | 67= | 72= | -5 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,29) ; autonomie et compétences (CA ; ancien contrôle) (+0,24) |
| T49 | Électricien × salarié × Suisse (frontalier) | 67= | 72= | -5 | autonomie et compétences (CA ; ancien contrôle) (-0,10) ; lieu (télétravail) retiré (+0,10) |
| T17 | Manipulateur radio (MERM) × fonctionnaire FPH × France | 64= | 72= | -8 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,38) ; autonomie et compétences (CA ; ancien contrôle) (+0,14) |
| T53 | Conducteur de train × salarié (SNCF) × France | 81= | 76= | +5 | lieu (télétravail) retiré (+0,10) ; conditions de travail (EP, IT, QT ; ancienne charge) (-0,05) |
| T23 | Infirmier × salarié × Suisse (résident) | 72= | 76= | -4 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,29) ; autonomie et compétences (CA ; ancien contrôle) (+0,24) |
| T47 | Électricien × salarié × France | 64= | 78= | -14 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,24) ; autonomie et compétences (CA ; ancien contrôle) (-0,10) |
| T28 | Infirmier × salarié × Canada (Québec) | 76= | 78= | -2 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,29) ; autonomie et compétences (CA ; ancien contrôle) (+0,24) |
| T12 | Infirmier × fonctionnaire FPH × France | 84= | 80= | +4 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,29) ; autonomie et compétences (CA ; ancien contrôle) (+0,24) |
| T52 | Frigoriste (CVC) × salarié × France | 69= | 80= | -11 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,19) ; autonomie et compétences (CA ; ancien contrôle) (-0,10) |
| T73 | Agent immobilier × indépendant (mandataire) × France | 84= | 82= | +2 | autonomie et compétences (CA ; ancien contrôle) (-0,16) ; sens retiré (+0,11) |
| T27 | Infirmier × salarié × Allemagne | 84= | 82= | +2 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,29) ; autonomie et compétences (CA ; ancien contrôle) (+0,24) |
| T66 | Sous-officier × militaire × France | 84= | 82= | +2 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,14) ; lieu (télétravail) retiré (+0,10) |
| T48 | Électricien × artisan × France | 72= | 85= | -13 | autonomie et compétences (CA ; ancien contrôle) (-0,25) ; lieu (télétravail) retiré (+0,02) |
| T51 | Plombier-chauffagiste × artisan × France | 72= | 85= | -13 | autonomie et compétences (CA ; ancien contrôle) (-0,25) ; lieu (télétravail) retiré (+0,02) |
| T44 | Technicien de maintenance industrielle × salarié × France | 76= | 85= | -9 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,33) ; lieu (télétravail) retiré (+0,10) |
| T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France | 69= | 88 | -19 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,43) ; lieu (télétravail) retiré (+0,10) |
| T33 | Aide-soignant (ASSC) × salarié × Suisse (frontalier) | 91 | 90 | +1 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,24) ; autonomie et compétences (CA ; ancien contrôle) (+0,19) |
| T75 | Employé commerce ou accueil (référence) × salarié × France | 92 | 91= | +1 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,19) ; sens retiré (+0,11) |
| T21 | Aide-soignant × fonctionnaire FPH × France | 90 | 91= | -1 | conditions de travail (EP, IT, QT ; ancienne charge) (-0,43) ; autonomie et compétences (CA ; ancien contrôle) (+0,19) |

## 8. Cellules revenu sans source fiable ou sans temps de travail réel

- Sans source fiable ou non officielles : T02 (non officielle), T14 (non re-sourcée), T15 (non officielle), T16 (non re-sourcée), T18 (non re-sourcée), T20 (non re-sourcée), T22 (non officielle), T36 (non officielle), T39 (non re-sourcée), T44 (non re-sourcée), T45 (non re-sourcée), T46 (non re-sourcée), T47 (non re-sourcée), T52 (non re-sourcée), T53 (non re-sourcée), T69 (non re-sourcée), T70 (non re-sourcée), T76 (non re-sourcée), T78 (non re-sourcée), T79 (non re-sourcée), T81 (non officielle), T72 (non re-sourcée), T74 (non officielle).
- Temps de travail réel non trouvé (pas de conversion en équivalent temps plein) : T03, T05, T07, T09, T13, T14, T15, T16, T18, T19, T20, T22, T35, T39, T44, T45, T46, T47, T48, T51, T52, T53, T67, T68, T69, T70, T76, T78, T79, T72, T73.

## 9. Conclusion : classement final

Règle déclarée (1.12) : le classement final réunit les triplets présents dans le haut du classement (10 premiers, rangs partagés compris) dans les 8 configurations de poids. Viennent ensuite ceux qui y sont dans les 4 configurations citées dans la demande (poids égaux, revenu, autonomie et sécurité doublés), puis, signalés à part, ceux qui n'y sont que dans une seule.

### 9.1 Noyau robuste : dans le haut du classement dans les 8 configurations

| Rang à poids égaux | Triplet | Palier | Rangs sur les 8 configurations | En une phrase |
|---|---|---|---|---|
| 1 | T30 Médecin généraliste × indépendant × Suisse (résident) | S | 1 à 1 | Premier partout : médian le plus élevé du pool en PPA (112 k€, OFS 2019, 43 h par semaine, donc pas de conversion), aucune note sous 3 ; seule sa note QT a un appui chiffré (heures), ses notes EP, IT, ES et PS sont estimées. |
| 5= | T89 Ingénieur cybersécurité (hors SOC) × salarié × Suisse (résident) | A* | 3 à 10 | Aucune dimension faible (EP 5, QT 5, PS 4), mais revenu moyen pour la Suisse (61 k€ en PPA) et proxy (médiane de tous les spécialistes TIC suisses) ; sa demande n'est documentée qu'en France (P4, donnée transposée) ; dernier admis quand le revenu ou la sécurité comptent double (10e). |

### 9.2 Dans le haut du classement dans les 4 configurations citées, pas dans les 8

| Rang | Triplet | Palier | Sort du haut du classement quand | En une phrase |
|---|---|---|---|---|
| 2= | T05 Chirurgien-dentiste × libéral × France | S* | EP doublé (17e) | Compétences et autonomie maximales (CA 5), 94 k€ médians (CARCDSF 2023) ; ses postures (EP 3, cohérent avec 84 % de troubles musculosquelettiques chez les orthodontistes, E8) le font sortir quand l'environnement physique compte double ; heures non trouvées. |
| 2= | T91 Chirurgien-dentiste × libéral × Suisse (résident) | S* | EP doublé (17e) | Mêmes notes que T05 ; revenu désormais tiré d'une enquête officielle (ESPA de l'OFS exploitée par la ZHAW pour la FMH : 166 000 CHF médians après 34 ans, 42 h par semaine, S111), soit 91 k€ en PPA. |
| 5= | T92 Chirurgien-dentiste × libéral × États-Unis | A* | EP doublé (25e), ES doublé (13e) | P80 le plus élevé du pool (184 k€ en PPA, ADA), 36 h par semaine ; exercice en anglais (ES 3) ; données américaines peu transférables. |
| 5= | T01 Médecin généraliste × libéral × France | A* | EP doublé (17e), QT doublé (16e) | 80 k€ médians ; 46 h par semaine en 2025 (DREES), donc F1 et QT 4, à 1 h du seuil de 45 h. |
| 8= | T03 Médecin spécialiste (rang médian) × libéral × France | A | EP, IT et QT doublés (17e, 11e, 16e) | 74 k€ médians au rang médian des spécialités ; heures non trouvées. |

### 9.3 Autres triplets souvent dans le haut du classement

| Rang | Triplet | Top 10 sur 8 | Remarque |
|---|---|---|---|
| 2= | T15 Orthophoniste × libéral × France | 7 | Premier quand EP ou IT comptent double, 20e quand le revenu compte double (22 k€, source non officielle, heures non trouvées). Son ES 4 est en tension avec le seul chiffre trouvé, celui de son groupe (S2) : appliqué, il passerait 7e, palier A. |
| 8= | T37 Développeur × salarié × Suisse (frontalier) | 6 | 89 k€ en PPA ; sort quand l'intensité ou la sécurité comptent double (PS 3, estimée). |
| 8= | T82, T46, T90, T83 | 5 | Cloud et DevOps frontalier en Suisse, actuaire, cybersécurité aux États-Unis et en France : environnement de bureau (E1) et compétences élevées ; le revenu de T46 n'est pas re-sourcé. |
| 14= à 16= | T09, T93, T64, T16 | 3 | Sage-femme libérale, orthophoniste aux États-Unis, administrateur de l'UE, orthoptiste. |

### 9.4 Dans le haut du classement dans une seule configuration

T85 data engineer (France), T39 développeur frontalier au Luxembourg, T35 développeur (France), T86 ingénieur cloud résident en Suisse : tous seulement quand l'environnement physique compte double (EP 5 des métiers de bureau). T35 et T85 y entrent grâce à leur PS passé de 3 à 4 (P3, créations d'emplois des ingénieurs de l'informatique).

Lecture :
- Avec des poids égaux, les conditions de travail (EP, IT, QT) pèsent 3/7 du score, contre 19 % pour l'ancienne charge, et l'autonomie passe de 22 % à 1/7 (CA, qui mêle latitude et niveau de compétence). Les métiers de bureau à revenu élevé montent (T37 du 23e au 8e rang, T82 du 27e au 8e, T46 du 16e au 8e) ; les soignants libéraux à revenu bas ou à contraintes physiques descendent (sage-femme libérale du 5e au 14e, kinésithérapeute libéral du 7e au 21e). Détail triplet par triplet en section 7.
- Palier S : T30, T05, T91, T15 ; les trois derniers sont à moins de 0,1 de la frontière de 4,2, fixée par la consigne. Scénario IA fort : aucun des 22 premiers ne change de palier.
- Le revenu en équivalent temps plein ne modifie aucune cellule : toutes les heures trouvées dépassent 35 h, ou la source est déjà en temps plein. Là où un temps partiel est probable (orthophoniste, sage-femme libérale, ostéopathe), les heures n'ont pas été trouvées ; ces cellules gardent la quotité 1 et sont signalées.
- Les notes hors revenu du haut du classement sont surtout des estimations : les statistiques par métier trouvées portent surtout sur l'hôpital, la police, le bâtiment et le transport, qui sont en bas du classement, et les confirment.

## 10. Ce qui est vérifiable et ce qui est mon opinion

| Élément | Statut |
|---|---|
| Les 7 dimensions et leur lien avec la santé et le bien-être des travailleurs | Consensus publié (Eurofound, S116). Composantes de la qualité du temps de travail : durée, horaires atypiques, aménagement, flexibilité ; le télétravail n'en fait pas partie (S150). |
| Poids égaux | Le choix le plus neutre, pas un fait : d'où les 8 configurations. Seuls T30 et T89 restent dans le haut du classement dans les 8. |
| Revenus cités (codes S), grilles, indices de prix, heures | Vérifiables, mais lus à travers des extraits de moteur de recherche : à contrôler dans les tableaux primaires avant toute décision. |
| Passage au net, moyenne vers médiane, P80, quotité | Hypothèses déclarées (1.4, 1.11, 1.12), modifiables dans `revenus.py`. |
| Notes EP et IT par groupe de métiers, latitude de décision (moitié de CA), ES et PS des libéraux | Estimations normatives (mon jugement). Sur 558 notes hors revenu : 9 sourcées au niveau du métier, 239 mixtes (dont les 93 notes CA), 310 estimées. |
| Règles d'ancrage (bandes EP, seuil de 1,5 fois la moyenne, seuil de 40 % pour F3, grille PS) | Choix déclarés (1.13) avant leur application ; limites arbitraires. 3 notes modifiées, 18 tensions signalées. |
| Revenus et notes aux États-Unis | Transférabilité limitée : congés payés, assurance santé et protection contre le licenciement non comparables ; seul l'écart de prix est corrigé. |
| Barrière d'entrée, probabilités p, scénarios IA | Informatifs, hors score ; poids de preuve faible. |
| Paliers, seuil d'égalité | Arbitraires ; 21 triplets sur 93 sont à moins de 0,1 d'une frontière de palier. |

Règle de révision : un rang ne changera que sur une donnée nouvelle (par exemple un tableau primaire qui contredit une cellule) ou une incohérence démontrée, jamais sur une simple contestation.

## 11. Cellules signalées

### 11.1 Revenu

- Non re-sourcées (valeur v3, estimée pour le sujet à 40 ans, donc parfois sous-estimée pour un professionnel installé) : T14, T16, T18, T20, T39, T44, T45, T46, T47, T52, T53, T69, T70, T72, T76, T78, T79 (17 cellules ; T53 et T76 : sources trouvées mais non officielles ou en conflit).
- Non officielles : T02 (fourchettes de sites spécialisés), T15 (UNASA ; la DREES ne publie aucun revenu des orthophonistes, son jeu de données 2026 ne les couvre pas, S136), T22 (registre associatif des ostéopathes), T36 et T81 (tarifs journaliers privés), T74 (sites spécialisés, Air France).
- Proxy ou champ plus large : T04, T21, T59 ; T11, T17, T33, T34, T60, T61, T62, T87, T88 ; T41, T42, T48, T49, T51, T58, T68, T73, T80, T82, T84, T85, T86, T89.
- Données anciennes : T23, T24, T29, T55.
- Temps de travail réel non trouvé (quotité 1, pas de conversion en équivalent temps plein) : T03, T05, T07, T09, T13, T14, T15, T16, T18, T19, T20, T22, T35, T39, T44, T45, T46, T47, T48, T51, T52, T53, T67, T68, T69, T70, T72, T73, T76, T78, T79 (31 cellules). Pour T35, la source DARES ne précise pas si le champ est le temps complet.
- Dentiste en Suisse, prioritaire dans la demande : la SSO ne publie pas de revenus ; T91 repose maintenant sur l'enquête officielle ESPA (OFS, 2014 à 2017) exploitée par la ZHAW pour la FMH, avec 42 h par semaine (S111), moins la prime LAMal ; fiabilité « relayée » (lue dans la presse professionnelle).

### 11.2 Notes hors revenu

- Modifiées par un chiffre de statut S : T35 et T85, PS 3 → 4 (P3) ; T57, ES 3 → 2 (S3).
- En tension avec un chiffre de groupe (note maintenue, effet en section 4) : ES de T09, T10, T11, T13, T15, T16, T18, T34, T76, T77, T78, T93 (S2) ; EP de T08 et T14 (E6) ; EP de T53 et T54 (E5) ; PS de T36 (P3) ; QT de T75 (Q8).
- Aucune statistique trouvée pour les conditions de travail des dentistes et des orthophonistes, qui occupent le haut du classement, ni des kinésithérapeutes (hors heures) : leurs notes IT sont des estimations, comme leurs notes EP et ES, sauf l'appui indirect des orthodontistes pour l'EP des dentistes (E8) et le chiffre de groupe pour l'ES des orthophonistes et des kinésithérapeutes (S2).

### 11.3 Pour lever ces limites

- Ajouter dares.travail-emploi.gouv.fr, insee.fr, drees.solidarites-sante.gouv.fr et bfs.admin.ch aux domaines autorisés de l'environnement cloud (accès réseau) permettrait de lire les tableaux primaires : portraits statistiques des métiers de la DARES (conditions de travail par famille professionnelle), enquête Sumer 2017 par famille professionnelle, jeux de données de la DREES, ESPA de l'OFS par profession.
- À chercher ensuite : heures des orthophonistes et des dentistes libéraux (FNO, ONDPS, DREES), revenus des cellules non re-sourcées, demande de développeurs hors de France (Suisse, Luxembourg, Allemagne, Québec).

## 12. Sources

| Code | Source |
|---|---|
| S01 | INSEE, Insee Première 2114, revenus des non-salariés en 2024 (juin 2026) : https://www.insee.fr/fr/statistiques/9013403 |
| S02 | DREES, Études et Résultats 1322, revenu des médecins libéraux 2021 : https://drees.solidarites-sante.gouv.fr/sites/default/files/2024-12/ER1322.pdf |
| S03 | DREES, jeu de données du 15 septembre 2026, revenus des libéraux de santé non médecins 2021 : https://drees.solidarites-sante.gouv.fr/communique-de-presse-jeux-de-donnees/jeux-de-donnees/260915_revenu-des-professionnels-de-sante-liberaux |
| S04 | CARCDSF 2023 via Dentaire365 : https://www.dentaire365.fr/actualites/vie-de-la-profession/salaires-des-chirurgiens-dentistes-des-ecarts-de-revenus-toujours-marques-en-2026/ |
| S05 | UNASA via Le Quotidien du Médecin (BNC 2022) : https://www.lequotidiendumedecin.fr/liberal/honoraires/bnc-2022-7-pour-les-generalistes-revenus-en-baisse-pour-la-majorite-des-medecins-liberaux |
| S06 | UNASA via Acoorde et sites spécialisés : https://www.acoorde.fr/documents/les-revenus-des-professionnels-de-sante/ ; https://kinedarbois.fr/2023/03/11/salaire-kine-liberal/ |
| S07 | DREES 2026, temps de travail des généralistes libéraux (46 h en 2025) : https://drees.solidarites-sante.gouv.fr/publications-communique-de-presse/etudes-et-resultats/260826-temps-travail-medecins-generalistes-liberaux |
| S08 | INSEE, Insee Première 2020, salaires du privé 2023 : https://www.insee.fr/fr/statistiques/8270416 |
| S09 | INSEE, Insee Première 2102, salaires de la FPH 2024 : https://www.insee.fr/fr/statistiques/8986438 |
| S10 | DREES, fiche Les salaires dans les établissements de santé (2025) : https://drees.solidarites-sante.gouv.fr/sites/default/files/2025-07/ES%202025%20-%20Fiche%2008%20-%20Les%20salaires%20dans%20les%20%C3%A9tablissements%20de%20sant%C3%A9.pdf ; relais infirmiers 2023 : https://www.charlottek.fr/salaire-infirmier/ |
| S11 | DEPP, salaires des enseignants : https://www.education.gouv.fr/depp/l-evolution-du-salaire-des-enseignants-titulaires-et-assimiles-titulaires-entre-2022-et-2023-452841 ; https://www.aefinfo.fr/depeche/755475-en-2024-le-salaire-net-moyen-des-enseignants-a-augmente-de-43-en-euros-constants-depp |
| S12 | Point d'indice gelé à 4,92278 € en 2026 : https://www.weka.fr/actualite/?p=207986 |
| S13 | Grille brigadier-chef : https://www.emploi-collectivites.fr/grille-indiciaire-etat-brigadier-chef-police/0/6025/9725.htm |
| S14 | Grille aide-soignant FPH : https://infos.emploipublic.fr/article/grilles-indiciaires-aide-soignant-hospitalier-eea-7996 |
| S15 | Offre SNCF conducteur (France Travail) : https://candidat.francetravail.fr/offres/recherche/detail/191TSYB |
| S16 | IESF, enquête 2025 : https://www.iesf.fr/offres/doc_inline_src/752/Brochure+Enquete+IESF+2025-Repondants.pdf |
| S17 | APEC 2025 via Le Monde Informatique : https://www.lemondeinformatique.fr/actualites/lire-les-salaires-des-cadres-it-analyses-par-l-apec-en-2025-98867.html |
| S18 | Revenus des avocats (médiane 2022) : https://lessentieldeleco.fr/4653-combien-gagne-un-avocat-debutant/ |
| S19 | Baromètre Malt relayé : https://www.lafabriquedunet.fr/agences/tendances/tarifs-des-developpeurs-freelances-dans-les-grandes-villes-de-france |
| S20 | Expert-comptable, UNASA 2024 via JDN : https://www.journaldunet.com/business/salaire/expert-comptable/salaire-00174 |
| S21 | Audioprothésiste : https://thotismedia.com/devenir-audioprothesiste |
| S22 | OFS, ESS 2024 premiers résultats : https://www.bfs.admin.ch/bfs/en.assetdetail.36195848.html ; groupes de professions : https://www.bfs.admin.ch/bfs/fr/home/statistiques/travail-remuneration/salaires-revenus-cout-travail/structure-salaires/groupes-professions.html |
| S23 | OFSP, FAQ salaire médian des infirmiers : https://www.faq.bag.admin.ch/pflegeinitiative/fr/salaire-et-conditions-de-travail/est-il-vrai-que-le-salaire-median-des-infirmierseres-est |
| S24 | OFS, revenus des médecins indépendants 2019 : https://dam-api.bfs.admin.ch/hub/api/dam/assets/19584629/master ; https://www.fmh.ch/files/pdf28/1804-1900.pdf |
| S25 | Étude OFSP/BASS 2018 via HR Today : https://hrtoday.ch/fr/news/les-revenus-des-medecins-sont-plus-eleves-qu-annonces |
| S26 | Médiane TIC ESS 2024 (calculateur) : https://calculateur-de-salaire.ch/metier/informaticien-ne |
| S27 | CCT branche électrique, salaires minimaux 2025 : https://eit.swiss/fileadmin/user_upload/documents/Branche/GAV/_fr/ELEKT_Mindestloehne_2025_FR.pdf |
| S28 | ESS 2022 par formation : https://www.baublatt.ch/management/lohnstrukturerhebung-2022-medianlohn-bei-6788-franken-35689 |
| S29 | FHL Healthcareers : https://fhlux.lu/web/healthcareers-for-exceptional-professionals/ ; valeur du point : https://salairesanteluxembourg.com/en/ |
| S30 | STATEC, Regards 09/2024 : https://statistiques.public.lu/dam-assets/catalogue-publications/regards/2024/regards-09-24.pdf |
| S31 | Grilles de la fonction publique européenne au 1er juillet 2025 : https://eutraining.eu/content/salary-of-eu-officials-civil-servants |
| S32 | Destatis avril 2024 via zm-online : https://www.zm-online.de/news/detail/fachkraefte-fuer-gesundheit-und-pflege-verdienen-deutlich-mehr |
| S33 | Bundesagentur für Arbeit, Entgeltatlas 2024 : https://www.presseportal.de/pm/6776/6080481 ; https://statistik.arbeitsagentur.de/DE/Statischer-Content/Statistiken/Fachstatistiken/Beschaeftigung/Generische-Publikationen/Blickpunkt-Arbeitsmarkt-Analyse-zur-Entgeltstatistik.pdf?__blob=publicationFile |
| S34 | TV-Ärzte VKA : https://www.praktischarzt.de/magazin/tv-aerzte-vka-mehr-gehalt-august-2025/ ; https://medizinio.de/blog/oberarzt-gehalt |
| S35 | Guichet-Emplois et guide Québec 2024 : https://www.guichetemplois.gc.ca/rapportmarche/salaire-profession/993/QC ; https://cdn-contenu.quebec.ca/cdn-contenu/immigration/formulaires/fr/Embaucher_un_travailleur_temporaire/Guide_Salaires_par_professions_Edition_2024.pdf |
| S36 | Eurostat, niveaux de prix 2024 (relais) : https://mail.actmedia.eu/daily/eurostat-household-consumption-price-levels-in-2024/114449 ; https://monstat.org/uploads/files/cijene/Komparativne/2/Comparative%20price%20levels%20in%202024.pdf ; Irlande 138 : https://www.nsi.bg/en/press-release/ravnishta-na-potrebitelski-ceni-v-es-8317 |
| S37 | OCDE, niveaux de prix 2024 via JILPT : https://www.jil.go.jp/kokunai/statistics/databook/2026/01/d2026_1T-16.pdf |
| S38 | Banque de France, parités mensuelles 2025 : https://www.banque-france.fr/fr/statistiques/taux-et-cours/taux-de-change-parites-moyenne-mensuelle-2025-12 |
| S39 | Règles PASS et LAS (AMU) : https://smpm.univ-amu.fr/sites/default/files/ressources_docs/M3C%20Acc%C3%A8s%20s%C3%A9lectif%202%C3%A8%20ann%C3%A9e%20MMOPK%202024-2025.pdf ; réussite 2024 : https://www.letudiant.fr/etudes/medecine-sante/reussite-en-pass-et-las-deux-etudiants-sur-cinq-integrent-les-etudes-de-sante-en-2024-1.html |
| S40 | Licence portail santé 2027 : https://www.lemoniteurdespharmacies.fr/profession/socio-professionnel/licence-portail-sante-le-pass-las-vit-ses-derniers-mois ; https://medisup.com/blog/fin-pass-las/ |
| S41 | IFSI, voie FPC : https://www.infirmiers.com/profession-ide/conditions-dadmission-en-ifsi-que-doivent-savoir-les-candidats |
| S42 | Parcoursup IFSI 2025 (question écrite AN) : https://questions.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE10625.pdf ; orthophonie : https://diplomeo.com/actualite-etudes_orthophoniste |
| S43 | Apprentissage : https://www.francetravail.fr/actualites/le-dossier/alternance/etre-embauche-en-contrat-dappren.html ; https://www.justice.fr/fiche/contrat-apprentissage |
| S44 | Réforme du recrutement des enseignants : https://www.projet-ariane.fr/articles/devenir-professeur-des-ecoles-le-concours-a-bac3-la-licence-lpe-et-le-master-remunere-session-2027 |
| S45 | Concours externe ICNA : https://recrutement.ecologie.gouv.fr/concours/ingenieur-e-du-controle-navigation-aerienne-icna-concours-externe-aviation-civile |
| S46 | CRFPA : https://diplomeo.com/actualite-passer_crfpa |
| S47 | EPSO AD5 2026 : https://www.euronews.com/my-europe/2026/02/17/epso-exam-record-breaking-participation-with-only-3-success-rate |
| S48 | CAST permanent : https://eu-careers.europa.eu/en/cast-permanent |
| S49 | Engagement dans l'armée de Terre, arrêté modifié 2024 : https://prod-site-internet-minarm-admin.cloud.defense.gouv.fr/sites/default/files/sga/Texte%202%20ARR%C3%8AT%C3%89%20fixant%20les%20modalit%C3%A9s%20de%20souscription%20des%20engagements%20dans%20l%27arm%C3%A9e%20de%20terre.pdf |
| S50 | Police nationale (France Travail) : https://www.francetravail.fr/actualites/le-dossier/fonction-publique/concours-recrutements-fonction-p/la-police-nationale-recrute-plus.html |
| S51 | Écoles vétérinaires (Onisep) : https://www.onisep.fr/formation/les-principaux-domaines-de-formation/les-ecoles-veterinaires |
| S52 | ENM : https://www.actu-juridique.fr/breves/magistrats/enm-353-places-prevus-pour-2024/ |
| S53 | Luxembourg, professions de santé réglementées : https://guichet.public.lu/fr/entreprises/creation-developpement/profession/autres-professions-liberales/profession-sante-reglementees.html |
| S54 | Qualifications Québec, infirmiers : https://qualificationsquebec.com/profession/infirmiers-autorises-infirmieres-autorisees-et-infirmiers-psychiatriques-autorises-infirmieres-psychiatriques-autorisees/?print=1 |
| S55 | Formation de mécanicien de locomotive : https://www.orientation.ch/fr/formations/cff-sa/pilote-de-locomotive-chez-cff-voyageurs ; https://www.bls.ch/-/media/bls/pdf/broschueren/broschuere-lokpersonal-kampagne.pdf?sc_lang=fr |
| S56 | OIT, Working Paper 140 (2025) : https://webapps.ilo.org/static/english/intserv/working-papers/wp140/index.html |
| S57 | Judge et al. 2010 : https://experts.arizona.edu/en/publications/the-relationship-between-pay-and-job-satisfaction-a-meta-analysis/ |
| S58 | DARES, panorama des conditions de travail (COR 2023) : https://www.cor-retraites.fr/sites/default/files/2023-03/Doc_06_Dares_panorama_CT.pdf |
| S59 | OCDE, Health at a Glance 2025, rémunération des infirmiers : https://www.oecd.org/en/publications/2025/11/health-at-a-glance-2025_a894f72e/full-report/remuneration-of-nurses_9b98c70c.html |
| S61 | Reconnaissance du diplôme infirmier en Suisse : https://www.guidedufrontalier.com/actualites/devenir-infirmier-suisse |
| S64 | Offre HUG infirmier, 86 500 à 120 500 CHF/an : https://frontaliereticino.ch/fr/trouver-emploi-geneve/infirmier-ou-infirmiere-equipe-antalgie-80-a-100-hug-geneve/ |
| S65 | Grille ergothérapeute FPH : https://www.emploi-collectivites.fr/grille-indiciaire-hospitaliere-ergotherapeute/1/6485.htm |
| S66 | DGAFP, rapport annuel 2025, rémunérations : https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/ra_2025_vue_remunerations_niveaux.pdf |
| S67 | INSEE, Insee Première 2100, FPE 2024 : https://www.insee.fr/fr/statistiques/8986474 |
| S68 | iFRAP citant la Cour des comptes : https://www.ifrap.org/agriculture-et-energie/controleurs-aeriens-une-greve-indigne |
| S69 | DGE, fiche pédicure-podologue : https://www.entreprises.gouv.fr/files/files/directions_services/pedicure-podologue.pdf |
| S70 | INSEE Hauts-de-France, forte demande psychologique des cadres : https://www.insee.fr/fr/statistiques/5542513 |
| S71 | DEPP 2016, enseignants et risques psychosociaux : https://cache.media.education.gouv.fr/file/revue_92/07/8/depp-2016-EF-92-enseignants-face-aux-risques-psychosociaux-comparaison-des-enseignants-avec-certains-cadres-prive-et-fonction-publique-2013_686078.pdf |
| S72 | Robert Half, ingénieur DevOps à Paris : https://www.roberthalf.com/fr/fr/details-emploi/ingenieur-devops/paris |
| S73 | Salaire ingénieur DevOps (moyenne Indeed 49 000 €) : https://recruteurindependant.com/salaire-ingenieur-devops/ |
| S74 | Free-Work, baromètre déclaratif : https://www.free-work.com/fr/tech-it/barometer/contributions/106137 |
| S75 | TJM IT 2025 (étude Morgan Philips) : https://www.blogdumoderateur.com/freelances-taux-journaliers-moyens-it-france |
| S76 | Salaire ingénieur cybersécurité : https://salerya.fr/metiers/tech/ingenieur-cybersecurite/ |
| S77 | Michael Page, salaires en cybersécurité : https://www.michaelpage.fr/advice/m%C3%A9tiers/syst%C3%A8mes-dinformation/quel-salaire-pour-un-expert-en-cybers%C3%A9curit%C3%A9 |
| S78 | Pénurie cyber (observatoire ANSSI 2025, OPIIEC, CESIN) : https://www.it-connect.fr/la-penurie-de-competences-cyber-samplifie-en-france/ |
| S79 | Ingénieur DevOps en Irlande : https://www.morganmckinley.com/ie/salary-guide/data/devops-engineer/dublin ; https://www.jobmentis.com/en/salaries/devops-engineer/ireland |
| S80 | BLS, développeurs logiciels, mai 2024 (relais) : https://qz.com/career-salaries-entry-to-senior-level |
| S81 | BLS, analystes en sécurité de l'information : https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm ; médiane mai 2024 relayée : https://wagedex.com/jobs/information-security-analysts/wisconsin |
| S82 | BLS, dentistes, médiane 2024 (relais) : https://dentistry.louisville.edu/admission/explore-dentistry ; https://www.bls.gov/ooh/healthcare/home.htm |
| S83 | BLS, orthophonistes, médiane mai 2024 (relais) : https://legacy.vault.com/industries-professions/professions/s/speech-language-pathologists-and-audiologists/earnings ; https://wagedex.com/jobs/speech-language-pathologists |
| S84 | Change moyen 2024 de la BCE (Suomen Pankki) : https://www.suomenpankki.fi/en/statistics/interest-rates-and-exchange-rates/exchange-rates/average-annual-exchange-rates-for-the-year-2024 |
| S85 | Irlande, USC et PRSI : https://lawsociety.ie/taxation/universal-social-charge-and-prsi ; https://vialtopartners.com/regional-alerts/ireland-employment-tax-budget-2025-key-measures-impacting-employers-and-employees/ |
| S86 | Dentistes formés à l'étranger aux États-Unis : https://www.ada.org/en/resources/licensure/licensure-for-the-international-dentists ; https://dent.osu.edu/academics/programs/doctor-dental-surgery/advanced-standing-international |
| S87 | BLS, projections d'emploi 2024 à 2034 : https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm ; https://www.bls.gov/opub/ted/2026/artificial-intelligence-information-technology-and-employment-2024-34.htm |
| S88 | H-1B, tirage pondéré et paiement de 100 000 USD : https://www.taftlaw.com/news-events/law-bulletins/the-2026-h-1b-cap-season-is-approaching-lottery-fees-and-new-selection-process/ ; https://www.employmentlawworldview.com/the-new-wage-rule-and-the-100k-proclamation-will-shape-the-2026-h%E2%80%911b-cap-season/ |
| S89 | ASHA, candidats formés à l'étranger : https://www.asha.org/certification/international-applicants-for-ccc-slp/ ; https://www.andrews.edu/chhs/speech/graduate-program/certification-process-for-international-applicants.pdf |
| S90 | Permis B des ressortissants de l'UE : https://www.weka.ch/themes/ressources-humaines/contrats-de-travail-et-reglements/permis-de-travail/article/permis-de-sejour-droit-de-sejour-de-cinq-ans/ ; https://www.kmu.admin.ch/kmu/fr/home/savoir-pratique/personnel/droit-du-travail/aspects-contractuels/permis-de-travail/libre-circulation-ue.html |
| S91 | Gajendran et Harrison 2007, méta-analyse du télétravail : https://www.apa.org/news/press/releases/2007/11/telecommuting ; https://goal-lab.psych.umn.edu/orgpsych/readings/10.%20Work-Life%20Balance/Gajendran%20%26%20Harrison%20(2007).pdf |
| S92 | Pratique du télétravail : https://www.insee.fr/fr/statistiques/8616841 ; DARES 2023 relayée : https://www.letribunaldunet.fr/lifestyle/metiers-teletravail-classement-france.html |
| S93 | Télétravail des frontaliers : https://www.lesfrontaliers.lu/emploi/34-jours-de-teletravail-la-france-adopte-finalement-le-principe/ ; https://www.lesfrontaliers.lu/emploi/le-teletravail-des-frontaliers-tourne-au-ralenti/ |
| S94 | Télétravail dans la fonction publique : https://www.fonction-publique.gouv.fr/etre-agent-public/mon-quotidien-au-travail/le-teletravail-dans-la-fonction-publique/le-cadre-juridique-du-teletravail-dans-la-fonction-publique ; https://www.cfdt-ufetam.org/wp-content/uploads/2022/02/protocole_teletravail_mte_23-02-22.pdf |
| S95 | Commission européenne, décision C(2022) 1788 sur le travail hybride : https://u4unity.eu/-oldsite-/document/RefCard_WorkTime_draft_11052023.pdf ; https://www.ffpe-bxl.eu/sites/default/files/Working%20time%20and%20hybrid%20working%20decision.docx.pdf |
| S96 | KFF, enquête 2024 sur l'assurance santé des employeurs : https://www.kff.org/health-costs/report/2024-employer-health-benefits-survey |
| S97 | Insee, définition du revenu d'activité des non-salariés (CSG et CRDS non déduites) : https://www.insee.fr/fr/metadonnees/definition/c1242 ; https://insee.fr/fr/statistiques/fichier/4470792/ERI20-D2.pdf |
| S98 | CARMF, BNC 2022 par spécialité : https://www.carmf.fr/actualites/communiques/2023/communique-bnc-2023.pdf ; revenus 2024 relayés : https://infos-entreprises.fr/?p=3489 |
| S99 | Insee, revenus des non-salariés par profession (dentistes, pharmaciens), relais : https://www.moneyvox.fr/votre-argent/actualites/109497/salaire-dentiste-medecin-pharmacien-taxi-quel-metier-independant-est-le-mieux-remunere ; https://www.previssima.fr/actualite/revenus-des-independants-quel-metier-non-salarie-rapporte-le-plus.html |
| S100 | Insee-DREES, salaires de la FPH en 2024 : https://www.insee.fr/fr/statistiques/8986438 ; DREES, fiche 08, édition 2026 : https://drees.solidarites-sante.gouv.fr/sites/default/files/2026-07/ES%202026%20-%20Fiche%2008%20-%20Les%20salaires%20dans%20les%20%C3%A9tablissements%20de%20sant%C3%A9.pdf |
| S101 | DEPP, salaires des enseignants en 2024 (NI 26.36) : https://www.education.gouv.fr/sites/default/files/document/depp-ni-2026-36pdf-519727.pdf ; temps de travail déclaré : https://www.education.gouv.fr/depp/la-moitie-des-enseignants-declare-travailler-au-moins-43-heures-par-semaine-452151 ; https://www.education.gouv.fr/les-enseignants-declarent-travailler-41-heures-30-en-moyenne-par-semaine-hors-vacances-scolaires-451702 |
| S102 | Insee, salaires de la fonction publique territoriale 2023 (SDIS) : https://www.insee.fr/fr/statistiques/fichier/8611947/ip2066.pdf ; temps de présence des sapeurs-pompiers : https://questions.assemblee-nationale.fr/dyn/14/questions/QANR5L14QE53121.pdf |
| S103 | APEC, rémunérations des cadres dans 111 familles de métiers 2025 : https://corporate.apec.fr/files/live/sites/corporate/files/Nos%20etudes/PDF/Les%20remunerations%20des%20cadres%20dans%20111%20familles%20de%20metiers%202025.pdf |
| S104 | Médiane des salaires des fonctionnaires de l'État en 2024, d'après l'Insee (relais) : https://www.moneyvox.fr/votre-argent/actualites/108701/voici-evolution-du-salaire-des-fonctionnaires-du-service-public-expliquee-en-graphiques |
| S105 | SDES, salaires nets du transport routier de marchandises : https://www.statistiques.developpement-durable.gouv.fr/edition-numerique/donnees-sociales-transport-routier-marchandises/8-32-les-salaires-nets |
| S106 | Insee, revenus des non-salariés par secteur 2024 et 2023 : https://www.insee.fr/fr/statistiques/8733101?sommaire=8733125 ; https://www.insee.fr/fr/statistiques/fichier/version-html/8590189/IP2060.pdf |
| S107 | CNBF, rapport 2024 : https://www.cnbf.fr/wp-content/uploads/2026/05/CNBF-Rapport-2024.pdf |
| S108 | OFS, revenus des médecins indépendants 2019 : https://admin.ch/gov/en/start/documentation/media-releases.msg-id-85700.html ; https://www.bfs.admin.ch/bfs/fr/home/actualites/quoi-de-neuf.assetdetail.19704726.html ; relais premier recours : https://swissinfo.ch/eng/society/male-doctors-earn-25-more-than-their-female-counterparts/47088168 |
| S109 | ASMAC, enquête 2023 sur le temps de travail des médecins assistants : https://vsao.ch/wp-content/uploads/2023/05/Sondage-membres-2023-Management-Summary_FR.pdf |
| S110 | Revenu AVS médian des médecins salariés en 2014 (BASS pour l'OFSP), cité par l'ASSH : https://www.sagw.ch/fileadmin/redaktion_sagw/dokumente/Publikationen/Berichte/2021_Macht_Medizin/05_Lohnunterschiede_Eine_Soziologische_Perspektive.pdf |
| S111 | ZHAW pour la FMH, revenus horaires des dentistes : https://www.zwp-online.info/zwpnews/dental-news/branchenmeldungen/schweizer-zahnaerzte-verdienen-73-franken-pro-stunde ; https://www.zwp-online.info/zwpnews/dental-news/branchenmeldungen/stundenlohn-schweizer-zahnarzte-verdienen-top |
| S112 | OFS, durée du travail 2024 : https://www.kmu.admin.ch/kmu/en/home/new/news/2025/working-hours-stable.html ; prime LAMal moyenne 2025 : https://www.bag.admin.ch/dam/fr/sd-web/4T-CsX1ytzWE/PG26-FB-Mittlere%20Pr%C3%A4mie_FR.pdf |
| S113 | BLS, Occupational Outlook Handbook et O*NET (mai 2024) : https://www.bls.gov/ooh/computer-and-information-technology/computer-network-architects.htm ; https://www.onetonline.org/link/localwages/15-1241.00 ; https://www.onetonline.org/link/localwages/15-1212.00 ; https://www.bls.gov/ooh/healthcare/speech-language-pathologists.htm ; https://www.onetonline.org/link/localwages/29-1127.00 |
| S114 | ADA Health Policy Institute, revenus et heures des dentistes : https://www.ada.org/resources/research/health-policy-institute/dental-practice-research/trends-in-dentist-income ; https://www.beckersdental.com/benchmarking/median-net-income-of-general-practice-dentists-hit-185k-in-2023 ; https://www.beckersdental.com/benchmarking/how-many-hours-do-dentists-work-per-week/ |
| S115 | OIT, CITP-08 et niveaux de compétence : https://isco.ilo.org/en/isco-08 |
| S116 | Eurofound, qualité de l'emploi (7 indices) : https://www.eurofound.europa.eu/en/topics/job-quality ; 6e enquête européenne sur les conditions de travail, rapport de synthèse : https://www.eurofound.europa.eu/en/publications/all/sixth-european-working-conditions-survey-overview-report |
| S117 | DARES et France Stratégie, Métiers 2030 (mars 2022), relais : https://www.lemondeinformatique.fr/actualites/lire-le-marche-de-l-emploi-it-attractif-mais-tendu-a-l-horizon-2030-86091.html ; https://www.solutions-numeriques.com/?p=96970 ; https://www.blogdumoderateur.com/metiers-informatique-creations-emploi-2030-penurie-talents/ |
| S118 | Allemagne, grille TV-Ärzte VKA : https://www.haufe.de/oeffentlicher-dienst/personal-tarifrecht/entgelttabellen/entgelttabelle-tv-aerztevka_144_519958.html ; https://www.oeffentlichen-dienst.de/entgelttabelle/tv-aerzte-vka.html ; Bundesagentur für Arbeit, Entgeltatlas : https://web.arbeitsagentur.de/entgeltatlas/beruf/59018 |
| S119 | Grilles des institutions de l'UE au 1er juillet 2025 : https://eur-lex.europa.eu/eli/C/2025/6564/oj ; agents contractuels : https://fusionforenergy.europa.eu/wp-content/uploads/2026/01/Remuneration-CA-1.pdf |
| S120 | Police nationale, rémunérations 2026 : https://www.police-nationale.interieur.gouv.fr/nous-rejoindre/nos-voies-dacces/devenir-policier/gpx/ext ; relais DGAFP : https://infos-entreprises.fr/combien-gagne/policier/ ; DGFiP : https://rejoindrelesfinancespubliques.economie.gouv.fr/evoluer-aux-finances-publiques/remuneration-et-avantages-sociaux |
| S121 | CFF, modèle de calcul des salaires des mécaniciens de locomotive (relais) : https://www.suedostschweiz.ch/panorama/was-verdient-ein-lokfuehrer-bei-der-sbb-bis-zu-8190-franken-im-monat-2124489 |
| S122 | Guichet-Emplois, médecins de famille au Québec : https://www.guichetemplois.gc.ca/rapportmarche/salaire-profession/24431/QC |
| S123 | CSO, Earnings Analysis using Administrative Data Sources 2024 : https://www.cso.ie/en/releasesandpublications/ep/p-eaads/earningsanalysisusingadministrativedatasources2024/distributionofearnings/ |
| S124 | Cour des comptes, gestion des ressources humaines de la DGAC (juillet 2026) : https://www.ccomptes.fr/sites/default/files/2026-07/20260706-S2026-0717-Gestion-des-RH-DGAC.pdf |
| S125 | Ministère des Armées, EcoDef n° 266 : https://www.defense.gouv.fr/sites/default/files/ssm/Ecodef%20266.pdf |
| S126 | Rémunération des magistrats (ministère de la Justice, relais) : https://www.simonnetavocat.fr/combien-gagne-un-juge-en-france-la-remuneration-reelle-des-magistrats/ |
| S127 | Pharmacie d'officine, accord salarial de 2026 : https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053907644 ; valeur précédente du point : https://www.legifrance.gouv.fr/conv_coll/id/KALIARTI000051834690/?idConteneur=1996 |
| S128 | DGAFP, rapport annuel 2025, niveaux de rémunération : https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/ra_2025_vue_remunerations_niveaux.pdf |
| S129 | Sources non officielles (centre de santé, SNCF, Air France) : https://www.profilmedecin.fr/contenu/remuneration-du-medecin-generaliste-comparatif-entre-lactivite-salariee-et-lactivite-liberale/ ; https://www.bvoltaire.fr/sncf-des-cheminots-bien-payes-primes-gratifies-mais-encore-en-greve/comment-page-6/ ; https://trajectio.fr/salaire-commandant-air-france/ |
| S130 | ASMAC, enquêtes auprès des membres 2022 et 2023 : https://www.suedostschweiz.ch/schweiz-und-welt/aerztinnen-und-aerzte-arbeiten-nach-wie-vor-viel-zu-viel-2-1915851 ; https://www.demoscope.ch/fileadmin/files/Medienberichte/Mitgliederbefragung-VSAO-2023-Management-Summary_DE_final.pdf |
| S131 | Étude Workforce 2020 sur les médecins de famille (Université de Bâle), relais, attribution probable : https://www.srf.ch/news/schweiz/drohende-versorgungsluecke-hausaerztemangel-die-situation-verbessert-sich-langsam |
| S132 | Ordre des masseurs-kinésithérapeutes, rapport sur les libéraux 2026 : https://www.ordremk.fr/wp-content/uploads/2026/07/rapport-kinesithapeutes-liberaux-2026.pdf |
| S133 | DARES, portraits statistiques des métiers, données ouvertes (salaire médian) : https://dares.travail-emploi.gouv.fr/sites/default/files/d00f3b579cafefe8712640d613401fef/Qualit%C3%A9%20de%20l'emploi%20-%20salaire%20m%C3%A9dian.csv |
| S134 | APEC, offres d'emploi en cybersécurité (relais) : https://www.meilleurs-masters.com/articles/metiers-cybersecurite-les-mieux-payes.html ; https://www.letudiant.fr/metiers/secteur/cybersecurite/analyste-soc.html |
| S135 | Registre des ostéopathes de France, rapport 2026 : https://osteopathie.org/client/document/rapport_rof_29012026_604.pdf |
| S136 | DREES, jeu de données 2026 sur les revenus des libéraux de santé (sans les orthophonistes) : https://drees.solidarites-sante.gouv.fr/communique-de-presse-jeux-de-donnees/jeux-de-donnees/260915_revenu-des-professionnels-de-sante-liberaux ; FNO, livret 2024 : https://www.fno.fr/wp-content/uploads/2024/10/LivretPro-2024-FNO.pdf |
| S137 | Pédicures-podologues : https://www.onpp.fr/assets/cnopp/fichiers/communiques/14-dossier-presse.pdf ; https://www.journaldunet.com/business/salaire/pedicure-podologue/salaire-00885 |
| S138 | DREES, Études et Résultats n° 1215 (novembre 2021), conditions de travail à l'hôpital en 2019 : https://drees.solidarites-sante.gouv.fr/sites/default/files/2021-11/ER1215.pdf ; relais : https://www.senat.fr/rap/r21-587-1/r21-587-123.html ; https://www.weka.fr/actualite/?p=142366 |
| S139 | Insee Références 2023 et DARES, conditions de travail en 2019 (crainte pour l'emploi) : https://www.insee.fr/fr/statistiques/7456903?sommaire=7456956 ; https://dares.travail-emploi.gouv.fr/publication/quelles-etaient-les-conditions-de-travail-en-2019-avant-la-crise-sanitaire |
| S140 | DARES Résultats, horaires atypiques en 2021 : https://dares.travail-emploi.gouv.fr/sites/default/files/9ecbd7771cb5901b009b74fc253e5623/DR%20travail_horaires%20atypiques_2021.pdf |
| S141 | DGAFP, rapport annuel 2024, temps et organisation du travail : https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/ra_2024_vue_temps_organisation_temps_travail.pdf |
| S142 | SSMSI, agressions selon la profession (enquêtes 2013 à 2018), relais : https://www.franceinfo.fr/societe/les-policiers-et-gendarmes-sont-pres-de-septfois-plus-victimes-d-agressions-physiques-que-la-moyenne-des-travailleurs-revele-le-ministere-de-l-interieur_4966776.html |
| S143 | SDES, durée de service des conducteurs routiers : https://www.statistiques.developpement-durable.gouv.fr/la-duree-de-service-des-conducteurs-routiers-de-fret-poids-lourds-en-2020 ; https://www.statistiques.developpement-durable.gouv.fr/la-duree-hebdomadaire-de-service-des-conducteurs-de-poids-lourds-du-transport-routier-de-1 |
| S144 | DARES, enquête Sumer 2017 : https://dares.travail-emploi.gouv.fr/sites/default/files/pdf/dares_expositions_risques_professionnels_produits_chimiques-2.pdf ; https://www.actu-environnement.com/media/pdf/news-34026-enquete-sumer-2017.pdf ; https://dares.travail-emploi.gouv.fr/publication/metiers-potentiellement-les-plus-concernes-par-les-criteres-ergonomiques |
| S145 | DEPP, note d'information 24.02 (enseignants, conditions de travail en 2019) : https://www.education.gouv.fr/depp/les-enseignants-des-cadres-au-contact-du-public-qui-se-sentent-utiles-mais-en-manque-de-452415 ; Insee Première n° 1506 : https://www.insee.fr/fr/statistiques/1283795 |
| S146 | Eurofound, 6e enquête européenne sur les conditions de travail (2015), indices par profession : https://www.researchgate.net/publication/311679538_6th_European_Working_Conditions_Survey_-_overview_report ; ETUI : https://www.etui.org/topics/health-safety-working-conditions/news-list/european-working-conditions-survey-2015-a-few-interesting-trends-in-health-at-work |
| S147 | Eurofound, enquête 2024, premiers résultats et rapport de synthèse : https://www.eurofound.europa.eu/en/publications/all/european-working-conditions-survey-2024-first-findings ; https://www.eurofound.europa.eu/en/publications/all/european-working-conditions-survey-2024-overview-report |
| S148 | Eurofound, travail indépendant et qualité de l'emploi : https://www.eurofound.europa.eu/en/publications/all/exploring-self-employment-european-union ; https://www.eurofound.europa.eu/en/publications/all/self-employment-eu-job-quality-and-developments-social-protection |
| S149 | OFS, Enquête suisse sur la santé 2022, conditions de travail : https://www.bfs.admin.ch/bfs/fr/home/statistiques/sante.assetdetail.31866458.html ; SECO, EWCTS 2021 : https://www.seco.admin.ch/seco/fr/home/seco/nsb-news/medienmitteilungen-2023.msg-id-97402.html |
| S150 | Eurofound, qualité du temps de travail (composantes de l'indice) : https://assets.eurofound.europa.eu/f/279033/75885649e5/ef1634en.pdf |
| S151 | DARES, travail le dimanche en 2025 (relais) : https://www.banquedesterritoires.fr/pres-dun-francais-sur-quatre-concerne-par-le-travail-le-dimanche |
| S152 | DARES, tensions sur le marché du travail en 2024 (février 2026) et déclinaisons régionales : https://centre-val-de-loire.dreets.gouv.fr/sites/centre-val-de-loire.dreets.gouv.fr/IMG/pdf/dares_dr_tensions_2024.pdf ; https://pays-de-la-loire.dreets.gouv.fr/sites/pays-de-la-loire.dreets.gouv.fr/IMG/pdf/les_tensions_sur_le_marche_du_travail_en_2024_dans_la_region_des_pays_de_la_loire.pdf ; https://tpeactu.fr/2026/02/05/metiers-en-tension-marche-du-travail-2024/ |
| S153 | Troubles musculosquelettiques des orthodontistes (enquête 2020) : https://odf.edpsciences.org/articles/odf/abs/2022/02/odf2022019/odf2022019.html ; population générale (Santé publique France) : https://www.santepubliquefrance.fr/maladies-et-traumatismes/maladies-liees-au-travail/troubles-musculo-squelettiques/documents/enquetes-etudes/prevalence-de-tms-en-france-dans-la-population-generale-et-dans-la-population-des-actifs-occupes-selon-la-categorie-socioprofessionnelle-et-le-sec |
| S154 | FNO, accès aux soins en orthophonie, cité dans une question écrite à l'Assemblée nationale (attribution probable) : https://questions.assemblee-nationale.fr/dyn/16/questions/QANR5L16QE6360.pdf ; https://fno.fr/wp-content/uploads/2024/10/FNO-Etude-acces-aux-soins-23.12.21.pptx.pdf |
