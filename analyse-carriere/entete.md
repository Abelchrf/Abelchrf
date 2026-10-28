# Classement de triplets métier × statut × pays

Sujet de référence : 24 ans, nationalité française, bac général, aucun diplôme du supérieur, quelques années d'emploi peu qualifié, aptitudes moyennes, ni réseau ni capital, sans charge de famille. Date de l'analyse : 11 octobre 2026. Version 3 du 13 octobre 2026 : critère lieu (télétravail) et nouveaux pays, Suisse en résident, Irlande, États-Unis (section 1.10). Version 4 du 28 octobre 2026 : classement par qualité de vie une fois installé, sans aucune barrière d'entrée dans le score, cellules revenu re-sourcées une par une (section 1.11).

Reproductibilité : tout le calcul est dans `modele.py` (entrées) et `tableaux.py` (sorties). Changer une entrée et relancer `python3 assembler.py` régénère les tableaux et le rapport.

## 0. Limites d'accès aux données (à lire avant les chiffres)

| Limite | Effet |
|---|---|
| La politique réseau de cet environnement bloque insee.fr, drees, bfs.admin.ch, statistiques.public.lu ; l'outil de lecture de pages échoue sur tous les hôtes. | Aucun tableau primaire n'a été ouvert. Les chiffres viennent de résumés de moteur de recherche citant ces sources, avec un risque de transcription. Les codes S renvoient aux pages citées. |
| Peu de médianes et de percentiles publiés par profession. | Depuis la v4, le revenu est celui d'un professionnel installé : médiane de la profession quand elle est publiée, sinon moyenne convertie par une règle déclarée (1.4). Chaque cellule porte sa source, sa conversion et un niveau de fiabilité. |
| Quota de recherches web épuisé le 28 octobre (200 recherches par tour, partagées entre les recherches parallèles). | 50 cellules revenu re-sourcées sur une source citée ; 8 gardent leur calcul v3 sur grille officielle ou tarif journalier privé ; 35 gardent leur valeur v3, signalées « non re-sourcée » (liste en section 8), à re-sourcer au tour suivant. |
| Contrôle, charge, relations, sens, sécurité : aucune série officielle par métier et par pays. | Estimations normatives, guidées par DARES, DREES, INSEE, DEPP (S58, S70, S71, S07). |

## 1. Entrées déclarées avant tout calcul

### 1.1 Calendrier et trajectoire de référence

| Entrée | Valeur |
|---|---|
| Début de formation | Rentrée 2027, à 25 ans, pour les cursus Parcoursup et les concours. L'année des 24 ans est l'emploi actuel. |
| Trajectoire de référence (emploi immédiat) | 18 000 € net à 24 ans (SMIC 2026 = 1 823,03 € brut, S43) puis montée linéaire à 21 000 € à 40 ans (médiane des employés 1 800 €/mois, S08), +0,5 %/an ensuite. |
| Revenus en formation | 0 € pour les études à temps plein ; stipendiums d'externat, salaire d'interne, apprentissage (53 % puis 100 % du SMIC, S43), traitements de stagiaire selon les règles de chaque voie. Frais de scolarité élevés comptés en négatif (ostéopathie, pilote, podologie). |
| Après l'entrée | Montée linéaire du revenu de début vers le médian à 40 ans, puis +0,5 %/an réel. |

### 1.2 Poids (opinion, pas consensus chiffré) : version 3, inchangés en version 4

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
