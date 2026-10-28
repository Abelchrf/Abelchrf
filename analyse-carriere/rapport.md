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

## 3. Classement v4 (93 triplets, qualité de vie une fois installé)

Lecture des colonnes : C contrôle, Ch charge, R relations, Se sécurité, Sn sens, L lieu (télétravail), notes entières de 1 à 5 ; Rev = note de revenu de 1 à 5, seule note continue, calculée sur les valeurs ajustées en PPA ; poids entre parenthèses. Palier : S ≥ 4,2, A ≥ 3,6, B ≥ 3,0, C en dessous ; * = à moins de 0,1 d'une frontière. « 7= » : rang partagé par des triplets à égalité (écart inférieur à 0,03). « X / Y k€ » : revenu net annuel en milliers d'euros, X au change 2025 sans ajustement, Y en parité de pouvoir d'achat (euros au niveau de prix français) ; le score utilise Y.

### Classement v4, partie A : notes par critère, puis palier

| Rang | ID | Triplet | C (22) | Ch (19) | R (15) | Se (15) | Sn (6) | L (8) | Rev (15) | Palier |
|---|---|---|---|---|---|---|---|---|---|---|
| 1= | T05 | Chirurgien-dentiste × libéral × France | 5 | 3 | 4 | 5 | 5 | 2 | 4,6 | A* |
| 1= | T91 | Chirurgien-dentiste × libéral × Suisse (résident) | 5 | 3 | 4 | 5 | 5 | 2 | 4,5 | A* |
| 3= | T92 | Chirurgien-dentiste × libéral × États-Unis | 5 | 3 | 3 | 5 | 5 | 2 | 4,9 | A |
| 3= | T15 | Orthophoniste × libéral × France | 5 | 5 | 4 | 5 | 5 | 2 | 1,4 | A |
| 5= | T09 | Sage-femme × libéral × France | 5 | 4 | 4 | 5 | 5 | 2 | 2,4 | A |
| 5= | T30 | Médecin généraliste × indépendant × Suisse (résident) | 4 | 3 | 4 | 5 | 5 | 2 | 5,0 | A |
| 7= | T10 | Masseur-kinésithérapeute × libéral × France | 5 | 3 | 4 | 5 | 5 | 2 | 2,8 | A |
| 7= | T01 | Médecin généraliste × libéral × France | 4 | 3 | 4 | 5 | 5 | 2 | 4,2 | A |
| 7= | T89 | Ingénieur cybersécurité (hors SOC) × salarié × Suisse (résident) | 4 | 4 | 4 | 4 | 4 | 4 | 3,3 | A |
| 7= | T81 | Ingénieur cloud et DevOps × indépendant (freelance) × France | 5 | 4 | 3 | 3 | 3 | 5 | 3,7 | A |
| 7= | T03 | Médecin spécialiste (rang médian) × libéral × France | 4 | 3 | 4 | 5 | 5 | 2 | 4,1 | A |
| 12= | T90 | Ingénieur cybersécurité (hors SOC) × salarié × États-Unis | 4 | 4 | 3 | 4 | 4 | 4 | 4,0 | A |
| 12= | T83 | Ingénieur cybersécurité (hors SOC) × salarié × France | 4 | 4 | 4 | 4 | 4 | 4 | 2,9 | A |
| 14= | T93 | Orthophoniste × salarié × États-Unis | 3 | 5 | 3 | 5 | 5 | 2 | 3,4 | A |
| 14= | T76 | Pédicure-podologue × libéral × France | 5 | 4 | 4 | 4 | 4 | 2 | 2,1 | A |
| 16= | T46 | Actuaire × salarié × France | 4 | 4 | 4 | 4 | 2 | 4 | 3,0 | A |
| 16= | T57 | Professeur certifié × fonctionnaire × France | 4 | 4 | 3 | 5 | 5 | 3 | 2,3 | A |
| 16= | T64 | Administrateur UE (AD) × fonctionnaire européen × Luxembourg (résident) | 3 | 4 | 3 | 5 | 3 | 4 | 3,9 | A |
| 19= | T56 | Professeur des écoles × fonctionnaire × France | 4 | 4 | 3 | 5 | 5 | 3 | 2,1 | A* |
| 19= | T36 | Développeur × indépendant (freelance) × France | 5 | 4 | 3 | 2 | 3 | 5 | 3,3 | A* |
| 21= | T02 | Médecin généraliste × salarié (centre de santé) × France | 3 | 4 | 4 | 5 | 5 | 1 | 3,4 | A* |
| 21= | T86 | Ingénieur cloud et DevOps × salarié × Suisse (résident) | 4 | 3 | 4 | 4 | 3 | 4 | 3,3 | A* |
| 23= | T41 | Ingénieur méthodes-industrialisation × salarié × France | 4 | 4 | 4 | 4 | 3 | 2 | 3,0 | A* |
| 23= | T71 | Magistrat × fonctionnaire × France | 4 | 3 | 3 | 5 | 5 | 3 | 2,9 | A* |
| 23= | T37 | Développeur × salarié × Suisse (frontalier) | 4 | 3 | 4 | 3 | 3 | 4 | 4,2 | A* |
| 23= | T40 | Développeur × salarié × Canada (Québec) | 4 | 4 | 4 | 3 | 3 | 4 | 2,9 | A* |
| 27= | T77 | Ergothérapeute × fonctionnaire FPH × France | 3 | 5 | 4 | 5 | 5 | 1 | 1,7 | B* |
| 27= | T82 | Ingénieur cloud et DevOps × salarié × Suisse (frontalier) | 4 | 2 | 4 | 4 | 3 | 4 | 4,1 | B* |
| 27= | T62 | Contrôleur des finances publiques × fonctionnaire × France | 3 | 5 | 3 | 5 | 3 | 4 | 1,8 | B* |
| 27= | T85 | Data engineer × salarié × France | 4 | 4 | 4 | 3 | 3 | 4 | 2,5 | B* |
| 31= | T35 | Développeur × salarié × France | 4 | 4 | 4 | 3 | 3 | 4 | 2,5 | B* |
| 31= | T80 | Ingénieur cloud et DevOps × salarié × France | 4 | 3 | 4 | 4 | 3 | 4 | 2,6 | B* |
| 33= | T38 | Développeur × salarié × Allemagne | 4 | 4 | 3 | 3 | 3 | 4 | 3,3 | B* |
| 33= | T68 | Expert-comptable × libéral × France | 4 | 3 | 3 | 4 | 3 | 3 | 4,0 | B* |
| 33= | T13 | Infirmier × libéral × France | 4 | 2 | 4 | 5 | 5 | 2 | 3,0 | B* |
| 33= | T43 | Ingénieur méthodes-industrialisation × salarié × Allemagne | 4 | 4 | 3 | 4 | 3 | 2 | 3,3 | B* |
| 37= | T34 | Masseur-kinésithérapeute × salarié × Suisse (frontalier) | 3 | 3 | 4 | 5 | 5 | 1 | 3,6 | B |
| 37= | T20 | Psychologue × contractuel FPH × France | 4 | 4 | 4 | 3 | 5 | 3 | 1,7 | B |
| 37= | T61 | Inspecteur des finances publiques × fonctionnaire × France | 3 | 4 | 3 | 5 | 3 | 4 | 2,3 | B |
| 37= | T88 | Ingénieur cloud et DevOps × salarié × États-Unis | 4 | 3 | 3 | 3 | 3 | 4 | 4,1 | B |
| 37= | T22 | Ostéopathe × libéral × France | 5 | 4 | 4 | 2 | 4 | 2 | 2,0 | B |
| 42= | T42 | Ingénieur méthodes-industrialisation × salarié × Suisse (frontalier) | 4 | 3 | 4 | 3 | 3 | 2 | 4,1 | B |
| 42= | T39 | Développeur × salarié × Luxembourg (frontalier) | 4 | 3 | 4 | 3 | 3 | 3 | 3,4 | B |
| 42= | T60 | Attaché d'administration × fonctionnaire × France | 3 | 4 | 3 | 5 | 3 | 4 | 2,0 | B |
| 45= | T78 | Diététicien × libéral × France | 4 | 5 | 4 | 2 | 4 | 3 | 1,4 | B |
| 45= | T32 | Médecin de famille × libéral (RAMQ) × Canada (Québec) | 3 | 2 | 3 | 5 | 5 | 2 | 4,7 | B |
| 45= | T11 | Masseur-kinésithérapeute × fonctionnaire FPH × France | 3 | 4 | 4 | 5 | 5 | 1 | 1,7 | B |
| 48= | T19 | Vétérinaire × libéral × France | 4 | 2 | 3 | 5 | 4 | 2 | 3,5 | B |
| 48= | T87 | Ingénieur cloud et DevOps × salarié × Irlande | 4 | 3 | 3 | 3 | 3 | 4 | 3,4 | B |
| 48= | T16 | Orthoptiste × salarié × France | 3 | 4 | 4 | 5 | 4 | 1 | 1,8 | B |
| 51 | T29 | Médecin × salarié (hôpital) × Suisse (résident) | 3 | 2 | 3 | 5 | 5 | 1 | 4,7 | B |
| 52= | T18 | Audioprothésiste × salarié × France | 3 | 4 | 4 | 4 | 4 | 1 | 2,2 | B |
| 52= | T69 | Comptable × salarié × France | 3 | 5 | 3 | 3 | 3 | 4 | 1,6 | B |
| 54= | T04 | Praticien hospitalier × statut PH (public) × France | 3 | 2 | 3 | 5 | 5 | 1 | 4,0 | B |
| 54= | T63 | Contrôleur aérien (ICNA) × fonctionnaire × France | 2 | 3 | 4 | 5 | 4 | 1 | 3,5 | B |
| 54= | T45 | Technicien réseaux et cybersécurité × salarié × France | 3 | 4 | 3 | 4 | 3 | 3 | 2,0 | B |
| 57= | T50 | Électricien × salarié × Canada (Québec) | 3 | 4 | 3 | 4 | 4 | 1 | 2,5 | B |
| 57= | T31 | Médecin × salarié (hôpital) × Allemagne | 3 | 2 | 2 | 5 | 5 | 1 | 4,5 | B |
| 59= | T70 | Comptable × salarié × Luxembourg (frontalier) | 3 | 4 | 3 | 3 | 2 | 3 | 3,0 | B |
| 59= | T08 | Sage-femme × fonctionnaire FPH × France | 3 | 3 | 3 | 5 | 4 | 1 | 2,5 | B |
| 59= | T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | 3 | 3 | 3 | 5 | 4 | 1 | 2,4 | B |
| 59= | T67 | Avocat × libéral × France | 3 | 3 | 3 | 3 | 3 | 3 | 3,7 | B |
| 63 | T72 | Commercial B2B × salarié × France | 4 | 3 | 3 | 3 | 2 | 3 | 2,5 | B* |
| 64= | T17 | Manipulateur radio (MERM) × fonctionnaire FPH × France | 2 | 4 | 3 | 5 | 4 | 1 | 1,9 | B* |
| 64= | T47 | Électricien × salarié × France | 3 | 4 | 3 | 4 | 4 | 1 | 1,4 | B* |
| 64= | T65 | Agent contractuel UE (GF II-III) × contractuel × Luxembourg (frontalier) | 2 | 4 | 3 | 3 | 3 | 4 | 2,6 | C* |
| 67= | T49 | Électricien × salarié × Suisse (frontalier) | 3 | 3 | 3 | 3 | 4 | 1 | 3,2 | C* |
| 67= | T26 | Infirmier × salarié × Luxembourg (résident) | 2 | 2 | 3 | 5 | 5 | 1 | 3,4 | C* |
| 69= | T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France | 2 | 2 | 4 | 5 | 5 | 1 | 2,2 | C |
| 69= | T07 | Pharmacien titulaire × indépendant × France | 3 | 2 | 3 | 3 | 4 | 2 | 3,5 | C |
| 69= | T52 | Frigoriste (CVC) × salarié × France | 3 | 3 | 3 | 4 | 4 | 1 | 1,7 | C |
| 72= | T23 | Infirmier × salarié × Suisse (résident) | 2 | 2 | 3 | 5 | 5 | 1 | 2,9 | C |
| 72= | T48 | Électricien × artisan × France | 4 | 2 | 3 | 3 | 4 | 2 | 1,8 | C |
| 72= | T51 | Plombier-chauffagiste × artisan × France | 4 | 2 | 3 | 3 | 4 | 2 | 1,8 | C |
| 72= | T84 | Analyste SOC (cybersécurité) × salarié × France | 2 | 3 | 3 | 4 | 4 | 2 | 2,3 | C |
| 76= | T54 | Conducteur de train × salarié × Suisse (résident) | 2 | 3 | 3 | 4 | 4 | 1 | 2,8 | C |
| 76= | T44 | Technicien de maintenance industrielle × salarié × France | 3 | 3 | 3 | 4 | 3 | 1 | 1,6 | C |
| 76= | T28 | Infirmier × salarié × Canada (Québec) | 2 | 2 | 3 | 5 | 5 | 1 | 2,5 | C |
| 76= | T24 | Infirmier × salarié × Suisse (frontalier) | 2 | 1 | 3 | 5 | 5 | 1 | 3,7 | C |
| 76= | T25 | Infirmier × salarié × Luxembourg (frontalier) | 2 | 1 | 3 | 5 | 5 | 1 | 3,7 | C |
| 81= | T79 | Opticien × salarié × France | 2 | 4 | 3 | 4 | 3 | 1 | 1,5 | C |
| 81= | T53 | Conducteur de train × salarié (SNCF) × France | 2 | 3 | 3 | 4 | 4 | 1 | 2,2 | C |
| 83 | T06 | Pharmacien adjoint × salarié × France | 2 | 2 | 3 | 5 | 4 | 1 | 2,4 | C |
| 84= | T66 | Sous-officier × militaire × France | 2 | 2 | 4 | 4 | 4 | 1 | 2,0 | C |
| 84= | T12 | Infirmier × fonctionnaire FPH × France | 2 | 2 | 3 | 5 | 4 | 1 | 2,0 | C |
| 84= | T27 | Infirmier × salarié × Allemagne | 2 | 2 | 2 | 5 | 5 | 1 | 2,5 | C |
| 84= | T73 | Agent immobilier × indépendant (mandataire) × France | 4 | 3 | 3 | 1 | 2 | 3 | 1,4 | C |
| 88 | T74 | Pilote de ligne × salarié × France | 2 | 2 | 3 | 3 | 3 | 1 | 4,1 | C |
| 89 | T58 | Gardien de la paix × fonctionnaire × France | 2 | 2 | 2 | 5 | 4 | 1 | 2,0 | C |
| 90 | T21 | Aide-soignant × fonctionnaire FPH × France | 1 | 2 | 3 | 5 | 4 | 1 | 1,4 | C |
| 91 | T33 | Aide-soignant (ASSC) × salarié × Suisse (frontalier) | 1 | 1 | 3 | 4 | 5 | 1 | 3,0 | C |
| 92 | T75 | Employé commerce ou accueil (référence) × salarié × France | 2 | 3 | 2 | 3 | 2 | 1 | 1,0 | C |
| 93 | T55 | Conducteur poids lourd × salarié × France | 2 | 1 | 2 | 4 | 3 | 1 | 1,0 | C |

### Classement v4, partie B : cellules revenu (net, professionnel installé)

| Rang | ID | Médian nom./PPA k€ | Source du médian | P80 nom./PPA k€ | Source du P80 | Temps de travail réel | Fiabilité |
|---|---|---|---|---|---|---|---|
| 1= | T05 | 94 / 94 | CARCDSF 2023 (S04) : médiane 97 672 € ; × 0,96 ; recoupement Insee (S99) : dentistes 10 300 €/mois moy. | 152 / 152 | estimé : log-normale des libéraux (× 1,62) | non trouvé | relayée |
| 1= | T91 | 144 / 90 | ZHAW pour la FMH (S111) : revenu horaire médian des dentistes 88 CHF (versions en conflit : 73 à 88 CHF), statut non précisé ; × 1 800 h × 0,85 | 233 / 146 | estimé : log-normale des libéraux (× 1,62) | non trouvé (1 800 h par an supposées) | sans source fiable |
| 3= | T92 | 131 / 106 | ADA HPI 2023 (S114) : médiane 185 360 USD, généralistes en cabinet privé ; moins cotisation des indépendants et assurance santé | 227 / 184 | log-normale (moyenne ADA 218 710 USD) | 36,1 h au cabinet (ADA, 2024, S114) | officielle (ordre professionnel) |
| 3= | T15 | 22 / 22 | UNASA 2022 (S06) : 27 550 € moy., temps partiel inclus ; × 0,96 × 0,85 ; recoupement FNO 2023 : 2 400 €/mois moy. | 36 / 36 | estimé : log-normale des libéraux (× 1,62) | temps partiel fréquent, durée non trouvée | non officielle |
| 5= | T09 | 34 / 34 | DREES 2021 (S03) : sages-femmes libérales, 42 200 € moy. ; × 0,96 × 0,85 | 56 / 56 | estimé : log-normale des libéraux (× 1,62) | non trouvé | officielle |
| 5= | T30 | 179 / 112 | OFS 2019 (S24, S108) : premier recours, médiane 172 000 CHF nets d'AVS et de 2e pilier (relayée par la presse) ; moins la prime LAMal | 287 / 179 | log-normale (moyenne OFS 199 975 CHF) | plein temps = 10 demi-journées (OFS) ; heures non trouvées | relayée |
| 7= | T10 | 42 / 42 | DREES 2021 (S03) : masseurs-kinésithérapeutes libéraux, 51 100 € moy. ; × 0,96 × 0,85 | 67 / 67 | estimé : log-normale des libéraux (× 1,62) | non trouvé | officielle |
| 7= | T01 | 80 / 80 | DREES 2021 (S02) : omnipraticiens, revenu d'activité moyen 98 300 € ; × 0,96 × 0,85 ; recoupement CARMF 2024 (S98) : 97 099 € moy. | 130 / 130 | estimé : log-normale des libéraux (× 1,62) | 46 h (DREES, ER 1381, données 2025, S07) | relayée |
| 7= | T89 | 98 / 61 | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre à la cybersécurité) ; × 12 × 0,80 | 114 / 71 | estimé : rapport P80/médian de la v3 (× 1,17) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | relayée, proxy |
| 7= | T81 | 69 / 69 | non officielle : TJM Free-Work et Morgan Philips (S74, S75) 650 € × 180 jours × 0,59 ; Insee 2024 (S106) : 4 190 €/mois moy., champ plus large | 90 / 90 | estimé (v3) | non trouvé | non officielle |
| 7= | T03 | 74 / 74 | DREES 2021 (S02) : pédiatres 88 400 €, psychiatres 92 800 € moy. (spécialités du rang médian) ; × 0,96 × 0,85 ; CARMF 2022 (S98), part libérale seule : 74 884 € et 73 014 € | 120 / 120 | estimé : log-normale des libéraux (× 1,62) | non trouvé | relayée |
| 12= | T90 | 98 / 79 | BLS OEWS mai 2024 (S113) : analystes en sécurité de l'information (15-1212), médiane 124 910 USD ; × 0,91 | 132 / 107 | interpolé entre P75 159 600 et P90 186 420 USD (S113) | 40 h usuelles (non mesurée) | officielle |
| 12= | T83 | 50 / 50 | APEC 2025 (S17, S103) : famille « sécurité informatique », médiane 60 k€ + 4 k€ de variable, brut ; × 0,78 | 63 / 63 | estimé : rapport P80/médian de la v3 (× 1,26) | non trouvé | relayée |
| 14= | T93 | 75 / 61 | BLS OEWS mai 2024 (S113) : orthophonistes, médiane 95 410 USD ; × 0,91 | 94 / 76 | interpolé entre P75 112 510 et P90 132 850 USD (S113) | 40 h usuelles (non mesurée) | officielle |
| 14= | T76 | 33 / 33 | non re-sourcé, valeur v3 : estimé : S69 (Observatoire de l'activité libérale, DGE : 27 600 € moy. en 2011), revalorisé | 45 / 45 | estimé (v3) | non trouvé | non re-sourcée |
| 16= | T46 | 52 / 52 | non re-sourcé, valeur v3 : estimé : enquete de l'Institut des actuaires non récupérée | 66 / 66 | estimé (v3) | non trouvé | non re-sourcée |
| 16= | T57 | 39 / 39 | DEPP 2024 (S101) : professeurs certifiés à temps complet, 3 220 €/mois net moyen ; moyenne = médiane (grille) | 46 / 46 | estimé : amplitude de grille (× 1,2) | 42 h médiane déclarée, second degré (DEPP 2018, S101) | officielle |
| 16= | T64 | 99 / 82 | grilles officielles du statut (S31) : AD7 à mi-carrière + indemnité de dépaysement 16 % ; avant impôt de l'UE | 109 / 91 | estimé (v3) | 40 h (non mesurée) | officielle (grille) |
| 19= | T56 | 35 / 35 | DEPP 2024 (S101) : professeurs des écoles à temps complet, 2 950 €/mois net moyen ; moyenne = médiane (grille) | 42 / 42 | estimé : amplitude de grille (× 1,2) | 43 h médiane déclarée (DEPP 2018) ; 41,8 h moyenne (2022-2023), S101 | officielle |
| 19= | T36 | 58 / 58 | non officielle : TJM Malt (S19) 576 € × 170 jours × 0,59 ; Insee 2024 (S106), information et communication : 4 190 €/mois moy., champ plus large | 76 / 76 | estimé (v3) | non trouvé | non officielle |
| 21= | T02 | 64 / 64 | non re-sourcé, valeur v3 : estimé : pas de série officielle ; ancrage S09 (INSEE FPH 2024 : personnels médicaux 6 926 €/mois moy.) | 76 / 76 | estimé (v3) | non trouvé | non re-sourcée |
| 21= | T86 | 98 / 61 | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre au cloud) ; × 12 × 0,80 | 113 / 71 | estimé : rapport P80/médian de la v3 (× 1,16) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | relayée, proxy |
| 23= | T41 | 52 / 52 | IESF 2025 (S16) : médiane 67 000 € brut, tous ingénieurs (proxy) ; × 0,78 | 65 / 65 | estimé : rapport P80/médian de la v3 (× 1,24) | non trouvé | relayée, proxy |
| 23= | T71 | 52 / 52 | non re-sourcé, valeur v3 : estimé : grille magistrats + primes non récupérée | 60 / 60 | estimé (v3) | non trouvé | non re-sourcée |
| 23= | T37 | 98 / 89 | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois ; × 12 × 0,80 | 116 / 105 | estimé : rapport P80/médian de la v3 (× 1,18) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | relayée |
| 23= | T40 | 51 / 50 | Guichet-Emplois, Québec 2024 (S35) : médiane 45,67 CAD/h ; × 1 950 h × 0,918 | 61 / 60 | estimé : rapport P80/médian de la v3 (× 1,20) | 37,5 à 40 h (non mesurée) | officielle |
| 27= | T77 | 30 / 30 | grille officielle FPH (S65) : IM 395 à 727 + CTI 183 € net/mois ; calcul à 10 ans d'exercice | 34 / 34 | estimé (v3) | non trouvé | officielle (grille) |
| 27= | T82 | 98 / 89 | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre au cloud) ; × 12 × 0,80 | 113 / 103 | estimé : rapport P80/médian de la v3 (× 1,16) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | relayée, proxy |
| 27= | T62 | 31 / 31 | non re-sourcé, valeur v3 : estimé : grille B + primes DGFiP ; ancrage S66 (DGAFP : cat. B 2 588 € moy. 2023) | 36 / 36 | estimé (v3) | non trouvé | non re-sourcée |
| 27= | T85 | 42 / 42 | APEC 2025 (S17, S103) : famille « business intelligence », médiane 50 k€ + 4 k€ de variable, brut (proxy) ; × 0,78 | 51 / 51 | estimé : rapport P80/médian de la v3 (× 1,20) | non trouvé | relayée, proxy |
| 31= | T35 | 40 / 40 | non re-sourcé, valeur v3 : S17 (APEC 2025 : IT 35-45 ans 49 à 101 k€) ; estimé 52 000 € brut × 0,78 | 51 / 51 | estimé (v3) | non trouvé | non re-sourcée |
| 31= | T80 | 43 / 43 | APEC 2025 (S17, S103) : famille « systèmes, réseaux et télécoms », médiane 51 k€ + 4 k€ de variable, brut (proxy) ; × 0,78 | 53 / 53 | estimé : rapport P80/médian de la v3 (× 1,23) | non trouvé | relayée, proxy |
| 33= | T38 | 57 / 58 | Bundesagentur für Arbeit 2024 (S33) : informatique, médiane 6 114 €/mois brut ; × 12 × 0,78 | 71 / 72 | estimé : rapport P80/médian de la v3 (× 1,23) | non trouvé | relayée |
| 33= | T68 | 73 / 73 | Insee 2024 (S106) : activités juridiques et comptables, 8 240 €/mois moy. (proxy) ; × 0,874 × 0,85 ; UNASA 2024 (S20) : 87 024 € moy. | 119 / 119 | estimé : log-normale des libéraux (× 1,62) | non trouvé | relayée, proxy |
| 33= | T13 | 47 / 47 | DREES 2021 (S03) : infirmiers libéraux, 57 100 € moy. ; × 0,96 × 0,85 | 75 / 75 | estimé : log-normale des libéraux (× 1,62) | non trouvé | officielle |
| 33= | T43 | 58 / 60 | non re-sourcé, valeur v3 : S33 (BA 2024 : IKT 6 114 €/mois, proxy) ; estimé 75 000 € × 0,78 | 70 / 71 | estimé (v3) | non trouvé | non re-sourcée |
| 37= | T34 | 77 / 70 | OFS, ESS 2024 (S22) : niveau de compétence 3, médiane 7 523 CHF/mois (proxy) ; × 12 × 0,80 | 86 / 78 | estimé : rapport P80/médian de la v3 (× 1,11) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | officielle, proxy |
| 37= | T20 | 30 / 30 | non re-sourcé, valeur v3 : estimé : grille psychologues FPH ; aucune série récupérée | 35 / 35 | estimé (v3) | non trouvé | non re-sourcée |
| 37= | T61 | 38 / 38 | non re-sourcé, valeur v3 : estimé : grille + primes DGFiP ; ancrage S67 (INSEE FPE 2024 : cat. A 3 543 € moy.) | 48 / 48 | estimé (v3) | non trouvé | non re-sourcée |
| 37= | T88 | 102 / 83 | BLS OEWS mai 2024 (S113) : architectes réseaux et cloud (15-1241), médiane 130 390 USD ; × 0,91 | 138 / 111 | interpolé entre P75 164 440 et P90 198 030 USD (S113) | 40 h usuelles (non mesurée) | officielle, proxy |
| 37= | T22 | 32 / 32 | non re-sourcé, valeur v3 : estimé : aucune série officielle récupérée | 45 / 45 | estimé (v3) | non trouvé | non re-sourcée |
| 42= | T42 | 93 / 84 | OFS, ESS 2022 (S28) : diplômés HES, médiane 9 000 CHF/mois (proxy) ; × 12 × 0,80 | 114 / 103 | estimé : rapport P80/médian de la v3 (× 1,23) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | relayée, proxy |
| 42= | T39 | 66 / 62 | non re-sourcé, valeur v3 : S30 (STATEC 2022 : médiane 58 126 €) ; estimé TIC 75 000 € × 0,875 | 83 / 79 | estimé (v3) | non trouvé | non re-sourcée |
| 42= | T60 | 33 / 33 | non re-sourcé, valeur v3 : estimé : grille attaché + IFSE ; ancrage S66 (DGAFP : cat. A 3 321 € moy. 2023, via secondaire) | 42 / 42 | estimé (v3) | non trouvé | non re-sourcée |
| 45= | T78 | 24 / 24 | non re-sourcé, valeur v3 : estimé : aucune série récupérée | 32 / 32 | estimé (v3) | non trouvé | non re-sourcée |
| 45= | T32 | 111 / 110 | non re-sourcé, valeur v3 : estimé : données RAMQ/ICIS non récupérées ; 180 000 CAD nets de frais | 148 / 146 | estimé (v3) | non trouvé | non re-sourcée |
| 45= | T11 | 30 / 30 | non re-sourcé, valeur v3 : estimé : grille rééducateurs FPH ; ancrage S09 | 34 / 34 | estimé (v3) | non trouvé | non re-sourcée |
| 48= | T19 | 57 / 57 | Insee 2024 (S01) : vétérinaires, 6 370 €/mois moy. ; × 0,874 × 0,85 | 92 / 92 | estimé : log-normale des libéraux (× 1,62) | non trouvé | relayée |
| 48= | T87 | 73 / 59 | non officielle : Jobmentis et Morgan McKinley (S79), médiane DevOps 79 000 € brut ; moins PRSI et USC (S85) | 105 / 85 | log-normale entre la médiane et P75 107 000 € (S79) | 39 h (non mesurée) | non officielle |
| 48= | T16 | 31 / 31 | non re-sourcé, valeur v3 : estimé : aucune série officielle récupérée | 36 / 36 | estimé (v3) | non trouvé | non re-sourcée |
| 51 | T29 | 175 / 110 | BASS pour l'OFSP (S110) : revenu AVS médian des médecins salariés 197 100 CHF, 2014 ; × 0,83 | 227 / 142 | estimé : rapport P80/médian de la v3 (× 1,29) | 50,7 h (médecins assistants, ASMAC 2023, S109) | officielle ancienne |
| 52= | T18 | 36 / 36 | non re-sourcé, valeur v3 : S21 (APEC : offres 36 600 € brut moy. ; confirme 2 300-3 100 € net/mois) | 45 / 45 | estimé (v3) | non trouvé | non re-sourcée |
| 52= | T69 | 29 / 29 | non re-sourcé, valeur v3 : S08 (PI) ; estimé 2 400 €/mois | 34 / 34 | estimé (v3) | non trouvé | non re-sourcée |
| 54= | T04 | 83 / 83 | Insee FPH 2024 (S09) : personnels médicaux, 6 926 €/mois net moyen en EQTP ; moyenne = médiane (grille) | 100 / 100 | estimé : amplitude de grille (× 1,2) | non trouvé | officielle, champ plus large |
| 54= | T63 | 66 / 66 | non re-sourcé, valeur v3 : estimé : S68 (Cour des comptes 2010 via iFRAP : 5 000 € net/mois moy.), revalorisé | 78 / 78 | estimé (v3) | non trouvé | non re-sourcée |
| 54= | T45 | 34 / 34 | non re-sourcé, valeur v3 : S08 (PI médiane 2 440 €, D9 3 680 €) ; estimé 2 800 €/mois | 42 / 42 | estimé (v3) | non trouvé | non re-sourcée |
| 57= | T50 | 44 / 44 | Guichet-Emplois, Québec 2024 (S35) : électriciens en construction, médiane 41 CAD/h ; × 1 900 h × 0,918 | 52 / 51 | estimé : rapport P80/médian de la v3 (× 1,17) | 40 h (non mesurée) | officielle |
| 57= | T31 | 103 / 105 | grille officielle TV-Ärzte VKA (S34) : Facharzt + gardes, 121 000 € brut estimé ; × 0,78 | 119 / 121 | estimé (v3) | 48 h au plus (non mesurée) | officielle (grille) |
| 59= | T70 | 54 / 52 | non re-sourcé, valeur v3 : S30 (STATEC 2022 : médiane 58 126 €) ; estimé 62 000 € × 0,875 | 66 / 62 | estimé (v3) | non trouvé | non re-sourcée |
| 59= | T08 | 41 / 41 | DREES 2022 (S10) : sages-femmes salariées des hôpitaux, 3 442 €/mois net moyen (3 487 € dans le tableau) ; moyenne = médiane (grille) | 50 / 50 | estimé : amplitude de grille (× 1,2) | non trouvé | officielle |
| 59= | T14 | 42 / 42 | non re-sourcé, valeur v3 : estimé : grille IADE FPH ; ancrage S09 | 48 / 48 | estimé (v3) | non trouvé | non re-sourcée |
| 59= | T67 | 54 / 54 | CNBF, rapport 2024 (S107) : médianes nettes 65 378 € (hommes) et 49 491 € (femmes), pondérées 43/57 (part des femmes estimée) ; × 0,96 | 122 / 122 | log-normale (moyennes CNBF 120 198 € et 66 812 €) | non trouvé | relayée |
| 63 | T72 | 38 / 38 | non re-sourcé, valeur v3 : S08 (PI et cadres) ; estimé 3 200 €/mois variable inclus | 55 / 55 | estimé (v3) | non trouvé | non re-sourcée |
| 64= | T17 | 34 / 34 | non re-sourcé, valeur v3 : estimé : grille paramédicale cat. A FPH ; ancrage S09 | 38 / 38 | estimé (v3) | non trouvé | non re-sourcée |
| 64= | T47 | 26 / 26 | non re-sourcé, valeur v3 : S08 (INSEE 2023 : ouvriers médiane 1 920 €/mois) ; estimé ouvrier qualifie 2 200 € | 31 / 31 | estimé (v3) | non trouvé | non re-sourcée |
| 64= | T65 | 46 / 44 | grilles officielles du statut (S31) : GF III + 16 % | 57 / 54 | estimé (v3) | 40 h (non mesurée) | officielle (grille) |
| 67= | T49 | 64 / 58 | OFS, ESS 2022 (S28) : titulaires d'un CFC, médiane 6 190 CHF/mois (proxy) ; × 12 × 0,80 | 74 / 68 | estimé : rapport P80/médian de la v3 (× 1,17) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | relayée, proxy |
| 67= | T26 | 75 / 63 | grille officielle FHL (S29) : 6 600 €/mois × 13 à 12 ans d'exercice ; × 0,875 | 91 / 76 | estimé (v3) | 40 h (non mesurée) | officielle (grille) |
| 69= | T59 | 36 / 36 | Insee 2023 (S102) : agents des SDIS, 3 030 €/mois net moyen en EQTP, sapeurs-pompiers et non-sapeurs-pompiers ; moyenne = médiane (grille) | 44 / 44 | estimé : amplitude de grille (× 1,2) | gardes de 24 h ; au plus 2 256 h de présence par an, soit 1 607 h effectives (S102) | officielle, champ plus large |
| 69= | T07 | 57 / 57 | Insee 2024 (S99) : pharmaciens non salariés, 6 390 €/mois moy. ; × 0,874 × 0,85 | 92 / 92 | estimé : log-normale des libéraux (× 1,62) | non trouvé | relayée |
| 69= | T52 | 30 / 30 | non re-sourcé, valeur v3 : S08 (ouvriers et PI) ; estimé 2 500 €/mois | 36 / 36 | estimé (v3) | non trouvé | non re-sourcée |
| 72= | T23 | 82 / 51 | OFSP (S23) : médiane des infirmiers 7 400 CHF/mois, 2018 ; × 1,074 (hausse de la médiane ESS 2018-2024) × 0,80 | 96 / 60 | v3 (haut de la fourchette HUG, S64) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | officielle ancienne |
| 72= | T48 | 27 / 27 | Insee 2024 (S01) : construction, non-salariés classiques, 3 050 €/mois moy. (proxy) ; × 0,864 × 0,85 | 43 / 43 | estimé : log-normale des libéraux (× 1,62) | non trouvé | relayée, proxy |
| 72= | T51 | 27 / 27 | Insee 2024 (S01) : construction, non-salariés classiques, 3 050 €/mois moy. (proxy) ; × 0,864 × 0,85 | 43 / 43 | estimé : log-normale des libéraux (× 1,62) | non trouvé | relayée, proxy |
| 72= | T84 | 39 / 39 | non re-sourcé, valeur v3 : estimé : S76 (bas de fourchette 37 000 € brut) ; 50 000 € brut à 40 ans × 0,78 | 47 / 47 | estimé (v3) | non trouvé | non re-sourcée |
| 76= | T54 | 78 / 49 | non re-sourcé, valeur v3 : S55 (BLS : 3 615 CHF/mois en formation) + S22 ; estimé 7 000 CHF × 13 × 0,80 | 87 / 55 | estimé (v3) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | non re-sourcée |
| 76= | T44 | 29 / 29 | non re-sourcé, valeur v3 : S08 (INSEE 2023 : professions intermediaires médiane 2 440 €/mois) ; estimé 2 400 € | 34 / 34 | estimé (v3) | non trouvé | non re-sourcée |
| 76= | T28 | 44 / 44 | Guichet-Emplois, Québec 2024 (S35) : médiane 40 CAD/h ; × 1 950 h × 0,918 | 51 / 50 | log-normale entre la médiane et le salaire élevé (45 CAD/h, lu comme Q3) | 37,5 à 40 h (non mesurée) | officielle |
| 76= | T24 | 82 / 74 | OFSP (S23) : médiane des infirmiers 7 400 CHF/mois, 2018 ; × 1,074 × 0,80 | 96 / 87 | v3 (S64) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | officielle ancienne |
| 76= | T25 | 75 / 72 | grille officielle FHL (S29) : 6 600 €/mois × 13 à 12 ans d'exercice ; × 0,875 | 91 / 87 | estimé (v3) | 40 h (non mesurée) | officielle (grille) |
| 81= | T79 | 27 / 27 | non re-sourcé, valeur v3 : S08 (PI médiane 2 440 €) ; estimé 2 250 €/mois | 32 / 32 | estimé (v3) | non trouvé | non re-sourcée |
| 81= | T53 | 37 / 37 | non re-sourcé, valeur v3 : S15 (SNCF : 26 à 34 k€ brut après formation) ; estimé 3 100 €/mois à 40 ans | 46 / 46 | estimé (v3) | non trouvé | non re-sourcée |
| 83 | T06 | 40 / 40 | non re-sourcé, valeur v3 : estimé : grille de la convention collective officine (non récupérée) ; aucune série officielle | 48 / 48 | estimé (v3) | non trouvé | non re-sourcée |
| 84= | T66 | 33 / 33 | non re-sourcé, valeur v3 : estimé : grille de solde non récupérée | 40 / 40 | estimé (v3) | non trouvé | non re-sourcée |
| 84= | T12 | 33 / 33 | DREES 2022 (S10) : infirmiers, 2 755 €/mois net moyen en EQTP, toutes structures ; moyenne = médiane (grille) ; FPH 2024, tous agents : moyenne 2 896 €, médiane 2 474 € (S100) | 40 / 40 | estimé : amplitude de grille (× 1,2) | 12 h ou 7 h 30 par poste ; durée non trouvée | officielle |
| 84= | T27 | 43 / 44 | Destatis avril 2024 (S32) : 4 310 €/mois brut ; × 12,8 (primes annuelles, estimé) × 0,78 | 49 / 50 | estimé : rapport P80/médian de la v3 (× 1,14) | non trouvé | relayée |
| 84= | T73 | 22 / 22 | Insee 2024 (S106) : activités immobilières, 2 480 €/mois moy. (proxy), 27 % de revenus nuls ou déficitaires ; × 0,874 × 0,85 | 36 / 36 | estimé : log-normale des libéraux (× 1,62) | non trouvé | relayée, proxy |
| 88 | T74 | 84 / 84 | non re-sourcé, valeur v3 : estimé : aucune série officielle récupérée | 110 / 110 | estimé (v3) | limites de temps de vol ; non mesurée | non re-sourcée |
| 89 | T58 | 34 / 34 | non re-sourcé, valeur v3 : S13 (grille brigadier-chef 2 550 à 2 678 € brut + ISSP 28,5 %) ; aucune moyenne officielle trouvée | 40 / 40 | estimé (v3) | cycles de 12 h 08 ; durée moyenne non mesurée (Cour des comptes) | non re-sourcée |
| 90 | T21 | 26 / 26 | DREES 2022 (S10) : aides-soignants et ASH, 2 184 €/mois net moyen ; moyenne = médiane (grille) | 31 / 31 | estimé : amplitude de grille (× 1,2) | 12 h ou 7 h 30 par poste ; durée non trouvée | officielle, champ plus large |
| 91 | T33 | 60 / 55 | OFS, ESS 2024 (S22) : niveau de compétence 2, médiane 5 866 CHF/mois (proxy) ; × 12 × 0,80 | 66 / 60 | estimé : rapport P80/médian de la v3 (× 1,09) | 41 h 47 contractuelles, tous salariés (OFS 2024, S112) | officielle, proxy |
| 92 | T75 | 22 / 22 | Insee 2023 (S08) : employés, médiane 1 800 €/mois net | 26 / 26 | estimé : rapport P80/médian de la v3 (× 1,19) | 35 h légales (non mesurée) | officielle |
| 93 | T55 | 22 / 22 | SDES 2019 (S105) : ouvriers qualifiés du transport routier de marchandises, 1 830 €/mois net en EQTP (non actualisé) | 26 / 26 | estimé : rapport P80/médian de la v3 (× 1,17) | non trouvé | officielle ancienne |

### Classement v4, partie C : barrière d'entrée et risque IA (informatif, hors score)

| Rang | ID | Âge d'entrée | Formation et financement | Sélectivité | Années de revenu perdues | Cumul 24-45 ans PPA k€ | IA : exposition, palier si IA fort | Dominé sur les 7 critères par |
|---|---|---|---|---|---|---|---|---|
| 1= | T05 | 31 ans | Licence portail santé + 5 ans ; prêt d'installation après collaboration | Places d'odontologie rares ; p estimé 5 % | 5,7 | 1226 | faible, A* | aucun |
| 1= | T91 | 33 ans | Dentaire en France + reconnaissance automatique UE + rachat ou création de cabinet | p estimé 4 % | 5,7 | 1315 | faible, A* | T05 |
| 3= | T92 | 34 ans | Dentaire en France + 2 à 3 ans d'advanced standing (environ 250 000 USD à Ohio State, S86) + INBDE + licence d'État + visa | p estimé 2 % | 16,6 | 1173 | faible, A | aucun |
| 3= | T15 | 30 ans | CFUO 5 ans (grade master) | 2025 : 3,29 % d'admis ; p estimé 3 % | 5,0 | 478 | faible, A | aucun |
| 5= | T09 | 31 ans | Licence portail santé + 5 ans (maïeutique en 6 ans) | p estimé 16 % | 5,8 | 586 | faible, A | aucun |
| 5= | T30 | 38 ans | Médecine en France + 3 ans en établissement suisse (admission LAMal) | p estimé 7 % | 5,4 | 1057 | faible, A | aucun |
| 7= | T10 | 30 ans | Licence portail santé ou STAPS accès kiné + IFMK 4 ans ; IFMK privés 5 à 9 k€/an | Très sélectif ; p estimé 7 % | 5,0 | 659 | faible, A | T05, T91 |
| 7= | T01 | 35 ans | Licence portail santé (rentrée 2027) puis 9 ans ; internat rémunéré ; bourses | 2 candidatures ; PASS 2024 : 33,8 % admis en 1 an ; p estimé 10 % | 5,4 | 932 | faible, A | T05, T30, T91 |
| 7= | T89 | 31 ans | Comme T83 + 1 an d'expérience + permis B (S90) | p estimé 15 % | 0,5 | 1026 | moyenne, A | aucun |
| 7= | T81 | 34 ans | Comme T80 + 5 ans salarié | p estimé 25 % | 0,5 | 1107 | moyenne, A | aucun |
| 7= | T03 | 38 ans | Idem T01 + internat 5 ans + clinicat 2 ans | Spécialité selon rang EDN ; p estimé 9 % | 5,4 | 897 | faible, A | T01, T05, T30, T91 |
| 12= | T90 | 31 ans | Comme T83 + visa de travail (S88) | p estimé 3 % | 0,5 | 1270 | moyenne, A* | aucun |
| 12= | T83 | 30 ans | BTS SIO option SISR puis bachelor ou mastère cybersécurité, tout en alternance | Offres cyber +49 % de 2019 à 2024 (ANSSI), 25 000 postes à pourvoir d'ici 2028 (OPIIEC) ; p estimé 25 % | 0,5 | 807 | moyenne, A* | T89 |
| 14= | T93 | 33 ans | Orthophonie en France + équivalence de master ASHA, Praxis, 36 semaines de clinical fellowship (S89) + visa | p estimé 2 % | 7,4 | 805 | faible, A | aucun |
| 14= | T76 | 28 ans | DE 3 ans (instituts surtout privés, 6 à 8 k€/an) | p estimé 25 % | 3,8 | 528 | faible, A | T09 |
| 16= | T46 | 30 ans | Licence de mathématiques + master d'actuariat | p estimé 6 % | 4,0 | 795 | élevée, B | T89 |
| 16= | T57 | 30 ans | Licence puis CAPES à bac+3 + 2 ans rémunérés | p estimé 35 % | 3,1 | 509 | moyenne, A* | aucun |
| 16= | T64 | 29 ans | Licence + concours EPSO AD5 (C1 + B2) | 2026 : environ 3 % de réussite ; p estimé 3 % | 3,0 | 1335 | moyenne, A* | aucun |
| 19= | T56 | 30 ans | Licence puis CRPE à bac+3 + 2 ans de master rémunérés (1 400 puis 1 800 € net) | p estimé 40 % | 3,1 | 484 | moyenne, A* | T57 |
| 19= | T36 | 32 ans | Idem T35 + 5 ans salarié | p estimé 30 % | 0,5 | 969 | élevée, B | T81 |
| 21= | T02 | 35 ans | Idem T01 | p estimé 10 % | 5,4 | 829 | faible, A* | aucun |
| 21= | T86 | 31 ans | Comme T80 + 2 ans d'expérience + permis B de droit avec un contrat d'au moins un an (S90) | p estimé 15 % | 0,5 | 1102 | moyenne, B | T89 |
| 23= | T41 | 31 ans | BUT puis école d'ingénieurs en apprentissage (29 ans révolus ; dérogation jusqu'à 35 ans en enchaînement) | p estimé 30 % | 1,2 | 736 | moyenne, B | T89 |
| 23= | T71 | 33 ans | Licence + M1 + concours ENM + 31 mois rémunérés | Environ 10,5 % de réussite ; p estimé 8 % | 5,0 | 711 | faible, A* | aucun |
| 23= | T37 | 30 ans | Idem T35 + 3 ans d'expérience ; permis G | p estimé 25 % | 0,5 | 1488 | élevée, B | aucun |
| 23= | T40 | 29 ans | Idem T35 + immigration | p estimé 25 % | 0,5 | 940 | élevée, B | T83, T89 |
| 27= | T77 | 28 ans | DE 3 ans (Parcoursup ou après année santé) | Sélectif ; p estimé 8 % | 3,0 | 515 | faible, B* | aucun |
| 27= | T82 | 31 ans | Comme T80 + 2 ans d'expérience ; permis G | p estimé 20 % | 0,5 | 1558 | moyenne, B | aucun |
| 27= | T62 | 26 ans | Concours de niveau bac + formation rémunérée | p estimé 30 % | 0,0 | 603 | moyenne, B* | aucun |
| 27= | T85 | 28 ans | BUT informatique ou science des données en alternance | p estimé 30 % | 1,1 | 809 | élevée, B | T40, T83, T89 |
| 31= | T35 | 27 ans | BTS SIO ou BUT en alternance (rémunéré) | Marché junior tendu 2024-2026 ; p estimé 45 % | 0,5 | 745 | élevée, B | T40, T83, T85, T89 |
| 31= | T80 | 29 ans | BTS SIO option SISR en alternance + 2 ans d'administration systèmes + certifications cloud | p estimé 35 % | 0,5 | 897 | moyenne, B | T83, T86, T89 |
| 33= | T38 | 28 ans | Idem T35 + allemand | p estimé 20 % | 0,5 | 995 | élevée, B | T81, T89, T90 |
| 33= | T68 | 33 ans | DCG + DSCG en alternance + stage 3 ans + DEC | p estimé 20 % | 0,6 | 946 | moyenne, B | aucun |
| 33= | T13 | 30 ans | IFSI + 24 mois d'exercice salarié avant installation | p estimé 22 % | 2,8 | 825 | faible, B* | T01, T03, T05, T30, T91 |
| 33= | T43 | 31 ans | Idem T41 + allemand | p estimé 15 % | 1,2 | 927 | moyenne, B | T89, T90 |
| 37= | T34 | 30 ans | Kiné en France + reconnaissance | p estimé 6 % | 5,0 | 1124 | faible, B | T01, T03, T05, T30, T91 |
| 37= | T20 | 30 ans | Licence + master sélectif | p estimé 20 % | 5,0 | 467 | faible, B | aucun |
| 37= | T61 | 29 ans | Licence + concours + ENFiP rémunérée | p estimé 15 % | 3,0 | 646 | moyenne, B | T64 |
| 37= | T88 | 31 ans | Comme T80 + visa de travail (loterie H-1B pondérée, 100 000 USD à la charge de l'employeur pour un candidat à l'étranger, S88) | p estimé 3 % | 0,5 | 1431 | moyenne, B | T37 |
| 37= | T22 | 30 ans | École privée 5 ans, 7 à 10 k€/an (prêt) | Peu sélectif ; marché saturé ; p estimé 65 % | 7,2 | 415 | faible, B | T09, T76 |
| 42= | T42 | 31 ans | Idem T41 + permis G | p estimé 20 % | 1,2 | 1354 | moyenne, B | T01, T05, T30, T37, T91 |
| 42= | T39 | 29 ans | Idem T35 + mobilité | p estimé 25 % | 0,5 | 1075 | élevée, B* | T37 |
| 42= | T60 | 29 ans | Licence + concours IRA + 1 an rémunéré | p estimé 10 % | 3,0 | 571 | moyenne, B | T61, T64 |
| 45= | T78 | 27 ans | BTS diététique ou BUT 2 à 3 ans | p estimé 50 % | 2,0 | 413 | moyenne, B | aucun |
| 45= | T32 | 35 ans | Médecine en France (DES MG) + ARM + immigration | p estimé 7 % | 5,4 | 1298 | faible, B | T30, T92 |
| 45= | T11 | 30 ans | Idem T10 | p estimé 7 % | 5,0 | 473 | faible, B | T02, T09, T77 |
| 48= | T19 | 32 ans | L2 ou BUT + concours (2 tentatives) + 5 ans ; ou école UE payante | Voie post-bac réservée aux néo-bacheliers ; 46 à 58 places par voie ; p estimé 5 % | 7,0 | 687 | faible, B | T01, T03, T05, T30, T91, T92 |
| 48= | T87 | 31 ans | Comme T80 + anglais courant | p estimé 15 % | 0,5 | 1085 | moyenne, B | T37, T81, T88, T90 |
| 48= | T16 | 28 ans | Certificat de capacité 3 ans | Sélectif ; p estimé 10 % | 3,0 | 535 | moyenne, B | T02, T09 |
| 51 | T29 | 35 ans | Médecine en France + autorisation MEBEKO | p estimé 8 % | 5,4 | 1102 | faible, B | T30, T32, T92 |
| 52= | T18 | 28 ans | DE 3 ans | Peu de places ; p estimé 10 % | 3,0 | 604 | faible, B | T02, T09, T83, T89 |
| 52= | T69 | 27 ans | BTS CG en alternance | p estimé 75 % | 0,5 | 554 | élevée, C | T62 |
| 54= | T04 | 38 ans | Idem T03 | p estimé 9 % | 5,4 | 786 | faible, B | T01, T03, T05, T29, T30, T32, T91, T92 |
| 54= | T63 | 30 ans | Concours externe : moins de 26 ans au 1er janvier, niveau CPGE ; formation rémunérée | Fenêtre 2027-2028 seulement ; p estimé 1 % | 0,0 | 1105 | faible, B | T01, T03, T05, T30, T34, T91 |
| 54= | T45 | 27 ans | BTS SIO ou BUT R&T en alternance | p estimé 60 % | 0,5 | 634 | moyenne, B* | T56, T57, T61, T64, T83, T89, T90 |
| 57= | T50 | 28 ans | Idem T47 + certificat CCQ + immigration | p estimé 35 % | 0,5 | 832 | faible, B | T02, T83, T89, T90, T93 |
| 57= | T31 | 35 ans | Médecine en France + allemand C1 (Fachsprachprüfung) | p estimé 6 % | 5,4 | 1244 | faible, B | T05, T29, T30, T32, T91, T92 |
| 59= | T70 | 27 ans | BTS CG + emploi au Luxembourg | p estimé 45 % | 0,5 | 915 | élevée, C | T38, T46, T64, T81, T89, T90 |
| 59= | T08 | 31 ans | Licence portail santé + 5 ans (maïeutique en 6 ans) | p estimé 18 % | 5,8 | 571 | faible, B | T01, T02, T03, T05, T10, T30, T34, T71, T91, T92, T93 |
| 59= | T14 | 32 ans | IFSI + 2 ans d'exercice + concours + 2 ans (promotion professionnelle rémunérée) | p estimé 9 % | 2,8 | 699 | faible, B | T01, T02, T03, T05, T08, T10, T30, T34, T71, T91, T92, T93 |
| 59= | T67 | 32 ans | Licence + M1 + CRFPA (3 tentatives) + 18 mois | Réussite 25 à 35 % ; p estimé 25 % | 6,5 | 652 | moyenne, C* | T37, T64, T68, T88, T90 |
| 63 | T72 | 27 ans | Embauche directe ou BTS NDRC en alternance | p estimé 80 % | 0,5 | 706 | moyenne, C | T37, T38, T39, T40, T46, T68, T71, T80, T81, T83, T85, T86, T87, T88, T89, T90 |
| 64= | T17 | 28 ans | DE ou DTS 3 ans | p estimé 30 % | 3,0 | 576 | faible, B* | T02, T09, T56, T57, T93 |
| 64= | T47 | 26 ans | Titre professionnel ou CAP adulte en moins d'un an (France Travail, CPF) | p estimé 85 % | 0,5 | 514 | faible, B* | T02, T09, T11, T16, T18, T50, T56, T57, T76, T77, T83, T89, T90, T93 |
| 64= | T65 | 26 ans | CAST permanent (bac + 3 ans d'expérience, C1 + B2), inscription continue | p estimé 15 % | 0,0 | 827 | élevée, C | T38, T40, T64, T81, T83, T89, T90 |
| 67= | T49 | 28 ans | Idem T47 + reconnaissance SEFRI ; permis G | p estimé 45 % | 0,5 | 1103 | faible, C* | T01, T02, T03, T05, T30, T34, T89, T90, T91, T92, T93 |
| 67= | T26 | 28 ans | IFSI + autorisation d'exercer (diplôme exempté de reconnaissance) | p estimé 22 % | 2,8 | 1083 | faible, C* | T01, T02, T03, T04, T05, T29, T30, T32, T34, T91, T92 |
| 69= | T59 | 27 ans | Volontariat + concours + recrutement par un SDIS | p estimé 8 % | 0,0 | 592 | faible, C | T01, T02, T03, T05, T09, T10, T13, T30, T34, T91 |
| 69= | T07 | 35 ans | Idem T06 + rachat d'officine (prêt, apport) | p estimé 12 % (financement sans capital) | 5,8 | 769 | faible, C | T01, T03, T05, T30, T32, T90, T91, T92 |
| 69= | T52 | 27 ans | CAP ou BTS froid en alternance | p estimé 70 % | 0,5 | 570 | faible, C | T01, T02, T03, T05, T08, T09, T10, T14, T16, T18, T30, T34, T50, T56, T57, T71, T76, T83, T89, T90, T91, T92, T93 |
| 72= | T23 | 28 ans | IFSI + reconnaissance Croix-Rouge suisse (mois) + permis B | p estimé 22 % | 2,8 | 909 | faible, C | T01, T02, T03, T04, T05, T13, T26, T29, T30, T32, T34, T71, T91, T92, T93 |
| 72= | T48 | 31 ans | Idem T47 + 5 ans salarié + création (outillage, véhicule) | p estimé 45 % (survie à 5 ans) | 0,5 | 581 | faible, C | T01, T03, T05, T09, T10, T13, T19, T30, T56, T57, T71, T76, T83, T89, T90, T91, T92 |
| 72= | T51 | 31 ans | CAP adulte + 5 ans salarié + création | p estimé 45 % | 0,5 | 581 | faible, C | T01, T03, T05, T09, T10, T13, T19, T30, T56, T57, T71, T76, T83, T89, T90, T91, T92 |
| 72= | T84 | 27 ans | BTS SIO option SISR en alternance | p estimé 45 % | 0,5 | 708 | élevée, C | T01, T03, T05, T09, T10, T30, T71, T83, T89, T90, T91, T92, T93 |
| 76= | T54 | 26 ans | Formation 14 à 16 mois rémunérée ; résidence près du dépôt | p estimé 15 % | 0,0 | 958 | faible, C | T01, T02, T03, T05, T10, T30, T34, T63, T71, T83, T89, T90, T91, T92, T93 |
| 76= | T44 | 27 ans | BTS MS en alternance | p estimé 70 % | 0,5 | 562 | faible, C | T01, T02, T03, T05, T08, T09, T10, T11, T14, T16, T18, T30, T34, T41, T43, T45, T50, T52, T56, T57, T60, T61, T62, T64, T68, T71, T76, T77, T80, T83, T86, T89, T90, T91, T92, T93 |
| 76= | T28 | 29 ans | IFSI + ARM (stage d'adaptation 75 jours) + immigration | p estimé 18 % | 2,8 | 808 | faible, C | T01, T02, T03, T04, T05, T10, T13, T23, T26, T29, T30, T32, T34, T71, T91, T92, T93 |
| 76= | T24 | 28 ans | IFSI + reconnaissance + permis G | p estimé 22 % | 2,8 | 1312 | faible, C | T01, T03, T04, T05, T29, T30, T32, T91, T92 |
| 76= | T25 | 28 ans | IFSI + autorisation d'exercer (diplôme exempté de reconnaissance) | p estimé 22 % | 2,8 | 1233 | faible, C | T01, T03, T04, T05, T24, T29, T30, T32, T91, T92 |
| 81= | T79 | 27 ans | BTS OL en alternance | p estimé 70 % | 0,5 | 523 | faible, C | T02, T09, T11, T16, T17, T18, T41, T43, T45, T50, T56, T57, T60, T61, T62, T64, T76, T77, T83, T89, T90, T93 |
| 81= | T53 | 26 ans | Recrutement + 12 mois de formation rémunérée | Tests psychotechniques ; p estimé 30 % | 0,0 | 685 | faible, C | T01, T02, T03, T05, T08, T09, T10, T14, T30, T34, T50, T54, T57, T63, T71, T83, T84, T89, T90, T91, T92, T93 |
| 83 | T06 | 31 ans | Licence portail santé + 5 ans | Places de pharmacie souvent non pourvues ; p estimé 25 % | 5,8 | 599 | faible, C | T01, T02, T03, T04, T05, T08, T10, T13, T14, T19, T23, T26, T28, T29, T30, T32, T34, T63, T71, T91, T92, T93 |
| 84= | T66 | 26 ans | École de sous-officiers 8 mois (moins de 32 ans, bac) | p estimé 70 % | 0,0 | 622 | faible, C | T01, T02, T03, T05, T09, T10, T13, T18, T30, T34, T59, T63, T76, T83, T89, T91 |
| 84= | T12 | 28 ans | IFSI 3 ans (Parcoursup, ou voie FPC avec 3 ans de cotisations ; Transition Pro possible) | 2025 : 116 000 candidats pour 25 000 places ; p estimé 25 % | 2,8 | 600 | faible, C | T01, T02, T03, T04, T05, T06, T08, T09, T10, T13, T14, T19, T23, T26, T28, T29, T30, T32, T34, T56, T57, T59, T63, T71, T91, T92, T93 |
| 84= | T27 | 29 ans | IFSI + allemand B2 + Anerkennung | p estimé 12 % | 2,8 | 773 | faible, C | T01, T02, T03, T04, T05, T10, T13, T23, T26, T28, T29, T30, T31, T32, T34, T71, T91, T92, T93 |
| 84= | T73 | 26 ans | Statut d'agent commercial, formation courte | p estimé 50 % (survie) | 0,5 | 465 | moyenne, C | T20, T35, T36, T37, T38, T39, T40, T46, T56, T57, T68, T71, T80, T81, T83, T85, T86, T87, T88, T89, T90, T72 |
| 88 | T74 | 28 ans | ATPL intégré (environ 100 k€) ou EPL (condition d'âge non vérifiée) | p estimé 10 % | 8,5 | 1183 | faible, C | T01, T05, T29, T30, T32, T37, T82, T91, T92 |
| 89 | T58 | 26 ans | Concours (bac) + 12 mois rémunérés (1 570 à 1 617 € net) | p estimé 30 % | 0,0 | 665 | faible, C | T01, T02, T03, T04, T05, T06, T08, T09, T10, T13, T14, T19, T23, T26, T27, T28, T29, T30, T31, T32, T34, T56, T57, T59, T63, T71, T91, T92, T93 |
| 90 | T21 | 26 ans | IFAS 1 an (apprentissage possible) | p estimé 75 % | 1,0 | 523 | faible, C | T01, T02, T03, T04, T05, T06, T08, T09, T10, T11, T12, T13, T14, T16, T17, T19, T23, T26, T28, T29, T30, T32, T34, T56, T57, T59, T63, T71, T77, T91, T92, T93 |
| 91 | T33 | 26 ans | IFAS + reconnaissance Croix-Rouge suisse | p estimé 55 % | 1,0 | 1084 | faible, C | T01, T02, T03, T04, T05, T13, T24, T25, T26, T29, T30, T32, T34, T91, T92, T93 |
| 92 | T75 | 24 ans | Aucune | p 100 % | 0,0 | 438 | moyenne, C | T01, T02, T03, T05, T08, T09, T10, T11, T14, T15, T16, T17, T18, T20, T30, T34, T35, T37, T38, T39, T40, T41, T42, T43, T44, T45, T46, T47, T49, T50, T52, T53, T54, T56, T57, T60, T61, T62, T63, T64, T65, T67, T68, T69, T70, T71, T76, T77, T79, T80, T81, T83, T84, T85, T86, T87, T88, T89, T90, T91, T92, T93, T72 |
| 93 | T55 | 25 ans | Permis C/CE + FIMO (3 mois, financés) | p estimé 85 % | 0,0 | 539 | moyenne, C | T01, T02, T03, T04, T05, T06, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T23, T24, T25, T26, T27, T28, T29, T30, T31, T32, T34, T41, T43, T44, T45, T47, T50, T52, T53, T54, T56, T57, T58, T59, T60, T61, T62, T63, T64, T66, T68, T71, T76, T77, T79, T80, T82, T83, T84, T86, T89, T90, T91, T92, T93 |

## 4. Égalités, frontières de palier, sensibilité aux poids

### Égalités déclarées (écart inférieur à 0,03 avec le premier du groupe)

rang 1 : T05 = T91 ; rang 3 : T92 = T15 ; rang 5 : T09 = T30 ; rang 7 : T10 = T01 = T89 = T81 = T03 ; rang 12 : T90 = T83 ; rang 14 : T93 = T76 ; rang 16 : T46 = T57 = T64 ; rang 19 : T56 = T36 ; rang 21 : T02 = T86 ; rang 23 : T41 = T71 = T37 = T40 ; rang 27 : T77 = T82 = T62 = T85 ; rang 31 : T35 = T80 ; rang 33 : T38 = T68 = T13 = T43 ; rang 37 : T34 = T20 = T61 = T88 = T22 ; rang 42 : T42 = T39 = T60 ; rang 45 : T78 = T32 = T11 ; rang 48 : T19 = T87 = T16 ; rang 52 : T18 = T69 ; rang 54 : T04 = T63 = T45 ; rang 57 : T50 = T31 ; rang 59 : T70 = T08 = T14 = T67 ; rang 64 : T17 = T47 = T65 ; rang 67 : T49 = T26 ; rang 69 : T59 = T07 = T52 ; rang 72 : T23 = T48 = T51 = T84 ; rang 76 : T54 = T44 = T28 = T24 = T25 ; rang 81 : T79 = T53 ; rang 84 : T66 = T12 = T27 = T73

### À moins de 0,1 d'une frontière de palier

T05 (A), T91 (A), T56 (A), T36 (A), T02 (A), T86 (A), T41 (A), T71 (A), T37 (A), T40 (A), T77 (B), T82 (B), T62 (B), T85 (B), T35 (B), T80 (B), T38 (B), T68 (B), T13 (B), T43 (B), T72 (B), T17 (B), T47 (B), T65 (C), T49 (C), T26 (C)

### Sensibilité des paliers aux poids (opinion, pas consensus)

| Variante | Palier S | Nombre S/A/B/C | Premier |
|---|---|---|---|
| Base (22/19/15/15/6/15, lieu 8) | aucun | 0/26/39/28 | T05 |
| Poids égaux (7 critères) | aucun | 0/21/43/29 | T05 |
| Revenu 30 (18/16/12/12/5/30, lieu 7) | T05, T92, T91 | 3/18/37/35 | T05 |
| Contrôle 30 (30/17/13/13/5/14, lieu 8) | T05, T91 | 2/27/34/30 | T05 |

## 5. Pourquoi T89 (cybersécurité, salarié, Suisse) est devant des indépendants

Le contrôle a le plus gros poids (22 sur 100), mais le score est une moyenne pondérée, pas un ordre strict : une note de contrôle en moins coûte 0,22, et une note de plus en relations et en sécurité rapporte 0,30. Un salarié peut donc passer devant un indépendant mieux noté en contrôle s'il le dépasse ailleurs. Si tu veux que le contrôle départage avant tout le reste, c'est un autre mode de calcul (ordre lexicographique), à décider explicitement.

Écart pondéré par critère (poids × différence de note, divisé par 100) entre T89 et chaque libéral, indépendant ou artisan classé sous lui ; un nombre positif favorise T89.

| Triplet classé sous T89 | Rang | C | Ch | R | Se | Sn | L | Rev | Total |
|---|---|---|---|---|---|---|---|---|---|
| T81 Ingénieur cloud et DevOps × indépendant (freelance) × France | 7= | -0,22 | +0,00 | +0,15 | +0,15 | +0,06 | -0,08 | -0,06 | +0,00 |
| T03 Médecin spécialiste (rang médian) × libéral × France | 7= | +0,00 | +0,19 | +0,00 | -0,15 | -0,06 | +0,16 | -0,11 | +0,03 |
| T76 Pédicure-podologue × libéral × France | 14= | -0,22 | +0,00 | +0,00 | +0,00 | +0,00 | +0,16 | +0,18 | +0,12 |
| T36 Développeur × indépendant (freelance) × France | 19= | -0,22 | +0,00 | +0,15 | +0,30 | +0,06 | -0,08 | -0,00 | +0,21 |
| T68 Expert-comptable × libéral × France | 33= | +0,00 | +0,19 | +0,15 | +0,00 | +0,06 | +0,08 | -0,11 | +0,37 |
| T13 Infirmier × libéral × France | 33= | +0,00 | +0,38 | +0,00 | -0,15 | -0,06 | +0,16 | +0,04 | +0,37 |
| T22 Ostéopathe × libéral × France | 37= | -0,22 | +0,00 | +0,00 | +0,30 | +0,00 | +0,16 | +0,19 | +0,43 |
| T78 Diététicien × libéral × France | 45= | +0,00 | -0,19 | +0,00 | +0,30 | +0,00 | +0,08 | +0,29 | +0,48 |
| T32 Médecin de famille × libéral (RAMQ) × Canada (Québec) | 45= | +0,22 | +0,38 | +0,15 | -0,15 | -0,06 | +0,16 | -0,22 | +0,48 |
| T19 Vétérinaire × libéral × France | 48= | +0,00 | +0,38 | +0,15 | -0,15 | +0,00 | +0,16 | -0,03 | +0,51 |
| T67 Avocat × libéral × France | 59= | +0,22 | +0,19 | +0,15 | +0,15 | +0,06 | +0,08 | -0,06 | +0,79 |
| T07 Pharmacien titulaire × indépendant × France | 69= | +0,22 | +0,38 | +0,15 | +0,15 | +0,00 | +0,16 | -0,03 | +1,03 |
| T48 Électricien × artisan × France | 72= | +0,00 | +0,38 | +0,15 | +0,15 | +0,00 | +0,16 | +0,23 | +1,07 |
| T51 Plombier-chauffagiste × artisan × France | 72= | +0,00 | +0,38 | +0,15 | +0,15 | +0,00 | +0,16 | +0,23 | +1,07 |
| T73 Agent immobilier × indépendant (mandataire) × France | 84= | +0,00 | +0,19 | +0,15 | +0,45 | +0,12 | +0,08 | +0,29 | +1,28 |

## 6. Modifications de rang par rapport à la version 3

Décomposition de l'écart de score de chaque triplet : (1) cumul 24-45 ans retiré du score revenu ; (2) notes modifiées ; (3) cellules revenu re-sourcées (médian et P80 installés, nouvelles bornes). Rang v3 avec la règle d'égalité de la v3 (écart inférieur à 0,005), rang v4 avec la nouvelle règle (0,03). Seuls les triplets dont le rang change sont listés.

| ID | Triplet | Rang v3 | Rang v4 | Variation | Cellule qui l'explique |
|---|---|---|---|---|---|
| T05 | Chirurgien-dentiste × libéral × France | 2 | 1= | +1 | revenu installé (S04) : médian 92 vers 94 k€ PPA, P80 127 vers 152 (+0,02) ; cumul 24-45 ans retiré du score (+0,01) ; croisé par T91 |
| T91 | Chirurgien-dentiste × libéral × Suisse (résident) | 1 | 1= | 0 | revenu installé (S111) : médian 97 vers 90 k€ PPA, P80 147 vers 146 (-0,03) ; cumul 24-45 ans retiré du score (+0,01) ; croisé par T05 |
| T92 | Chirurgien-dentiste × libéral × États-Unis | 4 | 3= | +1 | cumul 24-45 ans retiré du score (+0,04) ; revenu installé (S114) : médian 114 vers 106 k€ PPA, P80 165 vers 184 (-0,01) ; croisé par T15 |
| T15 | Orthophoniste × libéral × France | 3 | 3= | 0 | revenu installé (S06) : médian 31 vers 22 k€ PPA, P80 42 vers 36 (-0,09) ; cumul 24-45 ans retiré du score (+0,03) ; croisé par T92 |
| T09 | Sage-femme × libéral × France | 5 | 5= | 0 | revenu installé (S03) : médian 40 vers 34 k€ PPA, P80 55 vers 56 (-0,04) ; cumul 24-45 ans retiré du score (+0,03) |
| T30 | Médecin généraliste × indépendant × Suisse (résident) | 8 | 5= | +3 | revenu installé (S24) : médian 91 vers 112 k€ PPA, P80 125 vers 179 (+0,08) ; cumul 24-45 ans retiré du score (+0,03) ; croisé par T89, T81 |
| T10 | Masseur-kinésithérapeute × libéral × France | 9= | 7= | +2 | cumul 24-45 ans retiré du score (+0,02) ; revenu installé (S03) : médian 45 vers 42 k€ PPA, P80 60 vers 67 (-0,01) ; croisé par T89, T81 |
| T01 | Médecin généraliste × libéral × France | 13 | 7= | +6 | revenu installé (S02) : médian 76 vers 80 k€ PPA, P80 100 vers 130 (+0,04) ; cumul 24-45 ans retiré du score (+0,03) ; croisé par 5 triplets |
| T89 | Ingénieur cybersécurité (hors SOC) × salarié × Suisse (résident) | 6 | 7= | -1 | revenu installé (S26) : médian 64 vers 61 k€ PPA, P80 75 vers 71 (-0,03) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T30, T10, T01 |
| T81 | Ingénieur cloud et DevOps × indépendant (freelance) × France | 7 | 7= | 0 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T30, T10, T01 |
| T03 | Médecin spécialiste (rang médian) × libéral × France | 11 | 7= | +4 | cumul 24-45 ans retiré du score (+0,05) ; revenu installé (S02) : médian 82 vers 74 k€ PPA, P80 130 vers 120 (-0,04) ; croisé par T01, T90 |
| T90 | Ingénieur cybersécurité (hors SOC) × salarié × États-Unis | 9= | 12= | -3 | revenu installé (S113) : médian 83 vers 79 k€ PPA, P80 105 vers 107 (-0,01) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T01, T03 |
| T83 | Ingénieur cybersécurité (hors SOC) × salarié × France | 12 | 12= | 0 | score propre quasi inchangé ; croisé par T01 |
| T93 | Orthophoniste × salarié × États-Unis | 14 | 14= | 0 | revenu installé (S113) : médian 63 vers 61 k€ PPA, P80 79 vers 76 (-0,03) ; cumul 24-45 ans retiré du score (+0,03) |
| T76 | Pédicure-podologue × libéral × France | 15 | 14= | +1 | cumul 24-45 ans retiré du score (+0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) |
| T46 | Actuaire × salarié × France | 17 | 16= | +1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (+0,01) ; croisé par T64 |
| T57 | Professeur certifié × fonctionnaire × France | 24 | 16= | +8 | revenu installé (S101) : médian 29 vers 39 k€ PPA, P80 35 vers 46 (+0,08) ; cumul 24-45 ans retiré du score (+0,01) ; croisé par 7 triplets |
| T64 | Administrateur UE (AD) × fonctionnaire européen × Luxembourg (résident) | 16 | 16= | 0 | cumul 24-45 ans retiré du score (-0,03) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T46, T57 |
| T56 | Professeur des écoles × fonctionnaire × France | 28 | 19= | +9 | revenu installé (S101) : médian 27 vers 35 k€ PPA, P80 32 vers 42 (+0,08) ; cumul 24-45 ans retiré du score (+0,01) ; croisé par 9 triplets |
| T36 | Développeur × indépendant (freelance) × France | 18= | 19= | -1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T57, T56 |
| T02 | Médecin généraliste × salarié (centre de santé) × France | 22= | 21= | +1 | cumul 24-45 ans retiré du score (+0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par 5 triplets |
| T86 | Ingénieur cloud et DevOps × salarié × Suisse (résident) | 18= | 21= | -3 | revenu installé (S26) : médian 67 vers 61 k€ PPA, P80 78 vers 71 (-0,04) ; cumul 24-45 ans retiré du score (-0,02) ; croisé par T57, T56, T02 |
| T41 | Ingénieur méthodes-industrialisation × salarié × France | 31 | 23= | +8 | revenu installé (S16) : médian 45 vers 52 k€ PPA, P80 56 vers 65 (+0,04) ; croisé par 8 triplets |
| T71 | Magistrat × fonctionnaire × France | 25= | 23= | +2 | cumul 24-45 ans retiré du score (+0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par 6 triplets |
| T37 | Développeur × salarié × Suisse (frontalier) | 21 | 23= | -2 | cumul 24-45 ans retiré du score (-0,03) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par 6 triplets |
| T40 | Développeur × salarié × Canada (Québec) | 20 | 23= | -3 | revenu installé (S35) : médian 54 vers 50 k€ PPA, P80 65 vers 60 (-0,04) ; cumul 24-45 ans retiré du score (-0,02) ; croisé par 6 triplets |
| T77 | Ergothérapeute × fonctionnaire FPH × France | 29= | 27= | +2 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par 5 triplets |
| T82 | Ingénieur cloud et DevOps × salarié × Suisse (frontalier) | 22= | 27= | -5 | revenu installé (S26) : médian 97 vers 89 k€ PPA, P80 113 vers 103 (-0,04) ; cumul 24-45 ans retiré du score (-0,03) ; croisé par 5 triplets |
| T62 | Contrôleur des finances publiques × fonctionnaire × France | 29= | 27= | +2 | cumul 24-45 ans retiré du score (-0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T41, T77, T85, T80 |
| T85 | Data engineer × salarié × France | 25= | 27= | -2 | revenu installé (S17) : médian 47 vers 42 k€ PPA, P80 56 vers 51 (-0,05) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par 5 triplets |
| T35 | Développeur × salarié × France | 32 | 31= | +1 | cumul 24-45 ans retiré du score (-0,01) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T80 |
| T80 | Ingénieur cloud et DevOps × salarié × France | 25= | 31= | -6 | revenu installé (S17) : médian 51 vers 43 k€ PPA, P80 62 vers 53 (-0,07) ; cumul 24-45 ans retiré du score (-0,02) ; croisé par 5 triplets |
| T38 | Développeur × salarié × Allemagne | 33 | 33= | 0 | cumul 24-45 ans retiré du score (-0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) |
| T68 | Expert-comptable × libéral × France | 39= | 33= | +6 | revenu installé (S106) : médian 65 vers 73 k€ PPA, P80 103 vers 119 (+0,03) ; cumul 24-45 ans retiré du score (+0,02) ; croisé par 5 triplets |
| T13 | Infirmier × libéral × France | 36 | 33= | +3 | score propre quasi inchangé ; croisé par T68, T43, T34 |
| T43 | Ingénieur méthodes-industrialisation × salarié × Allemagne | 34= | 33= | +1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T68, T13 |
| T34 | Masseur-kinésithérapeute × salarié × Suisse (frontalier) | 34= | 37= | -3 | revenu installé (S22) : médian 73 vers 70 k€ PPA, P80 81 vers 78 (-0,02) ; cumul 24-45 ans retiré du score (-0,02) ; croisé par T68, T13 |
| T20 | Psychologue × contractuel FPH × France | 39= | 37= | +2 | cumul 24-45 ans retiré du score (+0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T61, T88, T42 |
| T61 | Inspecteur des finances publiques × fonctionnaire × France | 39= | 37= | +2 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T20, T88, T42 |
| T88 | Ingénieur cloud et DevOps × salarié × États-Unis | 37 | 37= | 0 | revenu installé (S113) : médian 89 vers 83 k€ PPA, P80 114 vers 111 (-0,03) ; cumul 24-45 ans retiré du score (-0,02) ; croisé par T68, T20, T61 |
| T22 | Ostéopathe × libéral × France | 43= | 37= | +6 | cumul 24-45 ans retiré du score (+0,06) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T42, T39, T60 |
| T42 | Ingénieur méthodes-industrialisation × salarié × Suisse (frontalier) | 38 | 42= | -4 | revenu installé (S28) : médian 89 vers 84 k€ PPA, P80 109 vers 103 (-0,03) ; cumul 24-45 ans retiré du score (-0,02) ; croisé par T68, T20, T61, T22 |
| T39 | Développeur × salarié × Luxembourg (frontalier) | 42 | 42= | 0 | cumul 24-45 ans retiré du score (-0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T22 |
| T60 | Attaché d'administration × fonctionnaire × France | 43= | 42= | +1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (+0,01) ; croisé par T22 |
| T11 | Masseur-kinésithérapeute × fonctionnaire FPH × France | 48 | 45= | +3 | cumul 24-45 ans retiré du score (+0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T87 |
| T19 | Vétérinaire × libéral × France | 50 | 48= | +2 | cumul 24-45 ans retiré du score (+0,04) ; revenu installé (S01) : médian 52 vers 57 k€ PPA, P80 76 vers 92 (+0,03) ; croisé par T87, T16 |
| T87 | Ingénieur cloud et DevOps × salarié × Irlande | 45= | 48= | -3 | revenu installé (S79) : médian 67 vers 59 k€ PPA, P80 81 vers 85 (-0,03) ; cumul 24-45 ans retiré du score (-0,02) ; croisé par T78, T32, T11, T19 |
| T16 | Orthoptiste × salarié × France | 49 | 48= | +1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T19 |
| T29 | Médecin × salarié (hôpital) × Suisse (résident) | 53 | 51 | +2 | revenu installé (S110) : médian 94 vers 110 k€ PPA, P80 122 vers 142 (+0,04) ; cumul 24-45 ans retiré du score (+0,03) ; croisé par T18, T69 |
| T18 | Audioprothésiste × salarié × France | 51= | 52= | -1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (+0,01) ; croisé par T29, T69 |
| T69 | Comptable × salarié × France | 51= | 52= | -1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T29, T18 |
| T04 | Praticien hospitalier × statut PH (public) × France | 59= | 54= | +5 | revenu installé (S09) : médian 68 vers 83 k€ PPA, P80 82 vers 100 (+0,06) ; cumul 24-45 ans retiré du score (+0,04) ; croisé par 5 triplets |
| T63 | Contrôleur aérien (ICNA) × fonctionnaire × France | 54 | 54= | 0 | cumul 24-45 ans retiré du score (-0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T04 |
| T45 | Technicien réseaux et cybersécurité × salarié × France | 56 | 54= | +2 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T04, T50 |
| T50 | Électricien × salarié × Canada (Québec) | 55 | 57= | -2 | revenu installé (S35) : médian 48 vers 44 k€ PPA, P80 56 vers 51 (-0,04) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T04, T45 |
| T31 | Médecin × salarié (hôpital) × Allemagne | 58 | 57= | +1 | cumul 24-45 ans retiré du score (+0,01) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T04, T70 |
| T70 | Comptable × salarié × Luxembourg (frontalier) | 57 | 59= | -2 | cumul 24-45 ans retiré du score (-0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T04, T31 |
| T08 | Sage-femme × fonctionnaire FPH × France | 62 | 59= | +3 | cumul 24-45 ans retiré du score (+0,02) ; revenu installé (S10) : médian 40 vers 41 k€ PPA, P80 45 vers 50 (+0,01) ; croisé par T14, T72 |
| T67 | Avocat × libéral × France | 66 | 59= | +7 | cumul 24-45 ans retiré du score (+0,05) ; revenu installé (S107) : médian 49 vers 54 k€ PPA, P80 94 vers 122 (+0,04) ; croisé par T72, T17, T47, T65 |
| T72 | Commercial B2B × salarié × France | 61 | 63 | -2 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T08, T67 |
| T17 | Manipulateur radio (MERM) × fonctionnaire FPH × France | 63= | 64= | -1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T67, T47, T65 |
| T47 | Électricien × salarié × France | 63= | 64= | -1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T67, T17, T65 |
| T65 | Agent contractuel UE (GF II-III) × contractuel × Luxembourg (frontalier) | 63= | 64= | -1 | cumul 24-45 ans retiré du score (-0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T67, T17, T47 |
| T49 | Électricien × salarié × Suisse (frontalier) | 67 | 67= | 0 | cumul 24-45 ans retiré du score (-0,03) ; revenu installé (S28) : médian 61 vers 58 k€ PPA, P80 71 vers 68 (-0,03) |
| T26 | Infirmier × salarié × Luxembourg (résident) | 68 | 67= | +1 | cumul 24-45 ans retiré du score (-0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) |
| T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France | 74= | 69= | +5 | revenu installé (S102) : médian 31 vers 36 k€ PPA, P80 34 vers 44 (+0,06) ; cumul 24-45 ans retiré du score (-0,02) ; croisé par 5 triplets |
| T07 | Pharmacien titulaire × indépendant × France | 74= | 69= | +5 | cumul 24-45 ans retiré du score (+0,03) ; croisé par 6 triplets |
| T52 | Frigoriste (CVC) × salarié × France | 69 | 69= | 0 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T59, T07 |
| T23 | Infirmier × salarié × Suisse (résident) | 70= | 72= | -2 | cumul 24-45 ans retiré du score (-0,02) ; revenu installé (S23) : médian 52 vers 51 k€ PPA, P80 60 vers 60 (-0,01) ; croisé par T59, T07, T48, T51 |
| T48 | Électricien × artisan × France | 70= | 72= | -2 | revenu installé (S01) : médian 31 vers 27 k€ PPA, P80 45 vers 43 (-0,04) ; croisé par T59, T07, T23 |
| T51 | Plombier-chauffagiste × artisan × France | 70= | 72= | -2 | revenu installé (S01) : médian 31 vers 27 k€ PPA, P80 45 vers 43 (-0,04) ; croisé par T59, T07, T23 |
| T84 | Analyste SOC (cybersécurité) × salarié × France | 74= | 72= | +2 | cumul 24-45 ans retiré du score (-0,01) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T07, T54 |
| T54 | Conducteur de train × salarié × Suisse (résident) | 73 | 76= | -3 | cumul 24-45 ans retiré du score (-0,04) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T59, T07, T84 |
| T44 | Technicien de maintenance industrielle × salarié × France | 78 | 76= | +2 | cumul 24-45 ans retiré du score (-0,01) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T24 |
| T28 | Infirmier × salarié × Canada (Québec) | 82= | 76= | +6 | sécurité 4 vers 5 (+0,15) ; revenu installé (S35) : médian 49 vers 44 k€ PPA, P80 57 vers 50 (-0,05) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par 5 triplets |
| T24 | Infirmier × salarié × Suisse (frontalier) | 77 | 76= | +1 | cumul 24-45 ans retiré du score (-0,03) ; revenu installé (S23) : médian 76 vers 74 k€ PPA, P80 87 vers 87 (-0,01) ; croisé par T44, T28 |
| T25 | Infirmier × salarié × Luxembourg (frontalier) | 79 | 76= | +3 | cumul 24-45 ans retiré du score (-0,03) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T28 |
| T79 | Opticien × salarié × France | 80 | 81= | -1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T28 |
| T53 | Conducteur de train × salarié (SNCF) × France | 81 | 81= | 0 | cumul 24-45 ans retiré du score (-0,01) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T28 |
| T06 | Pharmacien adjoint × salarié × France | 82= | 83 | -1 | cumul 24-45 ans retiré du score (+0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T28 |
| T27 | Infirmier × salarié × Allemagne | 88= | 84= | +4 | sécurité 4 vers 5 (+0,15) ; revenu installé (S32) : médian 46 vers 44 k€ PPA, P80 52 vers 50 (-0,03) ; cumul 24-45 ans retiré du score (-0,01) ; croisé par T73, T74, T58 |
| T74 | Pilote de ligne × salarié × France | 87 | 88 | -1 | nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T27 |
| T58 | Gardien de la paix × fonctionnaire × France | 88= | 89 | -1 | cumul 24-45 ans retiré du score (-0,02) ; nouvelles bornes de l'échelle revenu (cellule v3 conservée) (-0,01) ; croisé par T27 |

## 7. Conclusion : palier S vide, tête du classement

| Rang | Triplet | En une phrase |
|---|---|---|
| 1= | T05 Chirurgien-dentiste × libéral × France | Premier à égalité et à 0,03 du palier S : contrôle maximal, pénurie qui garantit l'emploi, 94 k€ médians nets (CARCDSF 2023) ; il égale ou dépasse le dentiste suisse sur les sept critères. |
| 1= | T91 Chirurgien-dentiste × libéral × Suisse (résident) | Mêmes notes que le dentiste français, mais son revenu (90 k€ en PPA) n'a pas de source fiable : sans statistique de la SSO, c'est un revenu horaire d'enquête ; c'est la place la plus fragile du haut du classement. |
| 3= | T92 Chirurgien-dentiste × libéral × États-Unis | Revenu le plus élevé du pool au P80 (184 k€ en PPA, ADA 2023), freiné par l'exercice en anglais (relations 3) ; donnée américaine peu transférable. |
| 3= | T15 Orthophoniste × libéral × France | La charge la plus légère (5) et un emploi garanti compensent le revenu le plus bas du haut du classement : 22 k€ médians au temps réel, souvent partiel (source non officielle, UNASA). |
| 5= | T09 Sage-femme × libéral × France | Contrôle 5 et charge 4 pour 34 k€ médians (DREES 2021, revenus en forte hausse depuis). |
| 5= | T30 Médecin généraliste × indépendant × Suisse (résident) | Médian installé le plus élevé du pool en PPA (112 k€, OFS 2019), avec un contrôle de 4 et une charge de 3. |

Lecture :
- Retirer la barrière fait monter les métiers à études longues, dont le cumul 24-45 ans était pénalisé : médecin généraliste libéral en France du 13e au 7e rang (ex aequo), médecin généraliste en Suisse du 8e au 5e, spécialiste du 11e au 7e.
- Mesurer le revenu au temps de travail réel fait baisser l'orthophoniste (31 vers 22 k€) et la sage-femme (40 vers 34 k€), sans les faire sortir du haut du classement.
- La tech reste dans le palier A : cybersécurité en Suisse du 6e au 7e rang (ex aequo), car la seule médiane officielle trouvée est celle de tous les spécialistes TIC ; cloud et DevOps freelance 7e (ex aequo) ; cybersécurité aux États-Unis du 9e au 12e (ex aequo) ; cybersécurité en France 12e (ex aequo).
- Le palier S reste vide pour la même raison qu'en v3 : la note de lieu de 2 des soignants libéraux. Avec un poids de contrôle de 30, T05 et T91 passent en S.

## 8. Ce qui est vérifiable et ce qui est mon opinion

| Élément | Statut |
|---|---|
| Revenus médians ou moyens cités (codes S), grilles de rémunération, indices de prix Eurostat, temps de travail cités | Vérifiable, mais lu ici à travers des extraits de moteur de recherche : à contrôler dans les tableaux primaires avant toute décision. |
| Passage au net, conversion d'une moyenne en médiane, P80 estimés, frais de scolarité, surcoûts régionaux des frontaliers | Hypothèses déclarées (sections 1.4 et 1.11), modifiables dans `revenus_v4.py`. |
| Notes de contrôle, charge, relations, sécurité, sens, lieu | Estimations normatives (mon jugement), guidées par DARES, DREES, INSEE, DEPP et les règles de télétravail citées. |
| Revenus et notes aux États-Unis | Revenus BLS et ADA vérifiables, mais transférabilité limitée : congés payés, assurance santé et protection contre le licenciement non comparables ; seul l'écart de prix est corrigé. |
| Poids des critères | Opinion fondée sur des tailles d'effet publiées ; aucun consensus chiffré. |
| Barrière d'entrée, probabilités p, scénarios IA | Informatifs, hors score ; p et IA sont des estimations à poids de preuve faible. |
| Seuils de paliers, seuil d'égalité | Arbitraires ; 26 triplets sur 93 sont à moins de 0,1 d'une frontière de palier. |

Règle de révision : un rang ne changera que sur une donnée nouvelle (par exemple un tableau primaire qui contredit une cellule) ou une incohérence démontrée, jamais sur une simple contestation.

## 9. Cellules revenu non re-sourcées ou sans source fiable

- Non re-sourcées faute de quota de recherche (valeur v3 conservée, estimée à 40 ans pour le sujet, donc parfois sous-estimée pour un professionnel installé) : T02, T06, T11, T14, T16, T17, T18, T20, T22, T32, T35, T39, T43, T44, T45, T46, T47, T52, T53, T54, T58, T60, T61, T62, T63, T66, T69, T70, T71, T72, T74, T76, T78, T79, T84.
- Sans source fiable : T91 (revenu horaire d'enquête, versions en conflit).
- Sources non officielles : T15 (UNASA, confirmé par la FNO), T36 et T81 (tarifs journaliers Malt, Free-Work, Morgan Philips), T87 (guides de salaires privés).
- Proxy (métier voisin ou champ plus large) : T04 (personnels médicaux de la FPH), T21 (avec les ASH), T33, T34, T42, T49 (niveaux de qualification suisses), T41 (tous ingénieurs), T48, T51 (toute la construction), T59 (tous agents des SDIS), T68 (activités juridiques et comptables), T73 (activités immobilières), T80, T85 (familles APEC voisines), T82, T86, T89 (tous spécialistes TIC suisses), T88 (architectes réseaux et cloud).
- Données anciennes : T23 et T24 (2018, actualisées par la hausse de la médiane ESS), T29 (2014), T55 (2019, non actualisé).
- P80 publiés ou interpolés : T88, T90, T93 (BLS) ; tous les autres sont estimés (log-normale, amplitude de grille ou rapport v3).
- Temps de travail réel trouvé seulement pour T01 (46 h), T56 et T57 (42 à 43 h déclarées), T29 (50,7 h), T92 (36,1 h), T59 (plafonds annuels) et la durée contractuelle suisse (41 h 47).
- À lire au tour suivant : jeux de données DREES (déciles par profession), fiche santé de l'Insee « Emploi et revenus des indépendants » 2025, portraits statistiques des métiers de la DARES, tableaux OFS de l'ESS par profession, revenus des dentistes suisses (SSO, Medisuisse), STATEC, Destatis et Bundesagentur für Arbeit, Guichet-Emplois et RAMQ.

## 10. Sources

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
