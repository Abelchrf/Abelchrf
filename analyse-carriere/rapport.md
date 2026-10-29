# Classement de triplets métier × statut × pays

Sujet de référence : 24 ans, nationalité française, bac général, aucun diplôme du supérieur, quelques années d'emploi peu qualifié, aptitudes moyennes, ni réseau ni capital, sans charge de famille. Date de l'analyse : 11 octobre 2026. Version 3 du 13 octobre 2026 : critère lieu (télétravail) et nouveaux pays, Suisse en résident, Irlande, États-Unis (section 1.10). Version 4 du 28 octobre 2026 : classement par qualité de vie une fois installé, sans aucune barrière d'entrée dans le score, cellules revenu re-sourcées une par une (section 1.11). Version 5 du 28 octobre 2026 : grille de qualité de l'emploi d'Eurofound, 7 dimensions à poids égaux, revenu en équivalent temps plein, robustesse testée sur 8 pondérations (section 1.12) ; elle remplace la pondération personnelle. Les notes hors revenu y sont confrontées aux statistiques publiées (DARES, DREES, Insee, SSMSI, DEPP, Eurofound, OFS, BLS) selon des règles déclarées (section 1.13). Version 6 du 29 octobre 2026 : gardes obligatoires (facteur F3), nouveaux ancrages et robustesse aux notes estimées par tirages aléatoires (section 1.14). Version 7 du 29 octobre 2026 : postes précis codés en CITP-08 à 4 chiffres, revenu net après impôt, deux classements séparés : France et Suisse (frontaliers compris), puis les 10 pays retenus par un tri déclaré des pays de l'OCDE, de Singapour et des Émirats (section 1.15). Le rapport de la version 6 est archivé dans `rapport_v6.md`.

Reproductibilité : entrées v1 à v6 dans `modele.py`, `revenus.py` et `eurofound.py` ; version 7 dans `pays_v7.py` (tri des pays), `postes_v7.py` (postes et triplets du classement 1), `notes_v7.py` (ancrages), `fiscalite_v7.py` (impôt), `modele_v7.py` (calculs et tirages), `classement2_v7.py` (classement 2) et `tableaux_v7.py` (sorties). Changer une entrée et relancer `python3 assembler.py` régénère les tableaux et le rapport ; les tirages ont une graine fixe.

## 0. Limites d'accès aux données (à lire avant les chiffres)

| Limite | Effet |
|---|---|
| La politique réseau de cet environnement bloque insee.fr, drees, dares.travail-emploi.gouv.fr (données ouvertes comprises), bfs.admin.ch, statistiques.public.lu ; l'outil de lecture de pages échoue sur tous les hôtes. Toujours le cas le 29 octobre, malgré l'autorisation annoncée : refus 403 du proxy sur dares.travail-emploi.gouv.fr, www.insee.fr, drees.solidarites-sante.gouv.fr et www.bfs.admin.ch ; même refus en v7 (29 octobre, 12 h 13 UTC) pour carmf.fr, OCDE, Eurostat, SSB, Danmarks Statistik, CBS, ONS, Statistik Austria, SURS, Hagstofa, STATEC, Destatis et l'Entgeltatlas. | Aucun tableau primaire n'a été ouvert. Les chiffres viennent de résumés de moteur de recherche citant ces sources, avec un risque de transcription. Les codes S renvoient aux pages citées. |
| Peu de médianes et de percentiles publiés par profession. | Depuis la v4, le revenu est celui d'un professionnel installé : médiane de la profession quand elle est publiée, sinon moyenne convertie par une règle déclarée (1.4). Chaque cellule porte sa source, sa conversion et un niveau de fiabilité. |
| Quota de 200 recherches web par tour, partagé entre les recherches parallèles (atteint en v4). | v5 : 18 des 35 cellules non re-sourcées en v4 l'ont été, dont le dentiste en Suisse ; 17 gardent leur valeur v3, signalées « non re-sourcée » (section 6 ; 15 d'entre elles sont encore dans le classement 1). |
| Notes hors revenu : peu de statistiques par métier (DARES, DREES, SSMSI, DEPP en France ; Eurofound par grand groupe de professions ; OFS par branche ; rien sur les conditions de travail des dentistes, orthophonistes et kinésithérapeutes, sauf leurs heures ; aucune statistique par métier lue hors de France et de Suisse). | Classement 1 : sur 666 notes, 12 sourcées, 311 mixtes (dont les 111 notes CA), 343 estimées ; 3 notes modifiées par un chiffre, 29 tensions. Classement 2 : sur 2 046 notes, 1 sourcée, 1 043 mixtes, 1 002 estimées, presque toutes transposées. Effet mesuré par tirages (sections 3 et 4, parties E et F). |
| Revenus par profession hors France et Suisse : très peu de chiffres lus (10 cellules). | Classement 2 : 296 cellules sur 341 viennent d'une règle de structure déclarée (1.15), signalées « estimé (structure) » et tirées à ± 20 % en variante D. |

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
| QT = 5 - F1 (plus de 45 h) - F3 (nuits, week-ends, astreintes) - H (horaires imposés, contrôle v4 de 3 ou moins), plancher 1 | Composantes de l'indice Eurofound : durée, horaires atypiques, aménagement des horaires et flexibilité ; le télétravail n'en fait pas partie (S150). | Tous |
| ES = relations v4 ; PS = sécurité v4, sauf contradiction avec un chiffre de statut S (1.13) | Même contenu ; les perspectives de carrière ne sont pas notées à part (limite). | Tous |
| CA = moyenne du contrôle v4 (latitude de décision) et du niveau de compétence CITP-08 de l'OIT (niveau 4 : 5 ; 3 : 3,67 ; 2 : 2,33 ; 1 : 1) | Eurofound réunit la latitude de décision et l'usage des compétences ; le niveau CITP-08 est une classification publiée (S115). | Tous |
| Facteurs F1 à F5 explicités pour chaque triplet (rapport v6, section 6, tableau de conversion) | 5 moins leur nombre redonne les 93 notes de charge v4 (contrôle automatique) : la conversion est traçable. | Tous |
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
| Contradiction | Un chiffre de statut S qui contredit la note la remplace par la valeur compatible la plus proche (liste dans le rapport v6, section 3 ; en v7, colonne « Notes hors revenu » et parties C et D). Un chiffre de statut M qui la contredit est signalé « tension » sans changer la note : une moyenne de groupe ou d'un autre pays ne fixe pas la note d'un métier précis. L'effet des tensions est montré à part (rapport v6, section 4 ; en v7, partie F du classement 1). |
| Groupes exclus | Trop hétérogènes pour un métier précis : l'ensemble des professions intermédiaires, le grand groupe CITP 5 (services et vente), la branche suisse « santé et action sociale ». |
| Non appliqué | Écarts entre la Suisse et l'Europe de l'enquête EWCTS 2021 (cadence plus élevée, moins de contraintes physiques, plus de latitude en Suisse) : moyennes nationales sans détail par métier, et le SECO juge l'enquête insuffisante pour une analyse détaillée (S149). Résultats Eurofound par statut (employeurs et indépendants stables au-dessus des indépendants dépendants, S148) : qualité globale, pas une dimension. |
| Recherche | 40 recherches sur les conditions de travail par métier (DARES, DREES, Insee, SSMSI, DEPP, SDES, DGAFP, Eurofound, OFS, SECO), puis 6 sur les heures, la demande et l'exposition des métiers du haut du classement. Rien trouvé sur les conditions de travail des dentistes (sauf une enquête sur les orthodontistes), des orthophonistes (sauf la saturation des agendas) et des kinésithérapeutes (sauf leurs heures). |

### 1.14 Changements de la version 6 (29 octobre 2026), déclarés avant recalcul

| Changement | Justification | Triplets touchés |
|---|---|---|
| Tableaux primaires (DARES par famille professionnelle, Sumer, OFS) non ouverts | Le proxy de la session refuse toujours les quatre domaines (403). Remplacement : 23 recherches web ciblées ; chiffres lus dans les résumés du moteur, avec la même limite qu'en section 0. | Aucun |
| Garde obligatoire = F3 : quand une obligation légale de participer à un service de garde ou d'urgence (nuits, week-ends ou astreinte) s'applique au métier et au statut, même rachetable par une taxe, le facteur F3 est marqué | Consigne du 29 octobre pour T30, étendue à tous les triplets concernés pour éviter une incohérence : la même loi suisse (LPMéd art. 40 let. g) vise les médecins-dentistes, et le code de la santé publique impose la permanence des soins dentaires des dimanches et jours fériés en France. Limite : la fréquence des gardes n'est publiée nulle part. Pas d'obligation pour les médecins libéraux français (volontariat ; environ 40 % participent) ni pour les dentistes aux États-Unis. | T30, T91, T05 |
| Astreintes en cybersécurité | Aucune part officielle trouvée. Astreintes signalées pour certains postes, surtout en SOC et en gestion de crise (France Travail) ; 70 % disent travailler souvent le week-end (enquête d'un éditeur de logiciels). Chiffre non officiel : tension signalée, F3 non ajouté. L'analyste SOC (T84) garde son F3. | T83, T89, T90 |
| Nouveaux ancrages (codes Q15 à Q19, E9, P8 à P12) | Demande : Obsan pour les médecins de premier recours en Suisse, HRSA pour les dentistes aux États-Unis, BLS pour les orthophonistes aux États-Unis, enquête de la SSO pour les dentistes suisses, classement suisse de pénurie de l'informatique. Exposition : critères ergonomiques par métier (DARES, Sumer 2017). Règles de statut et de conversion de la section 1.13. | T30, T92, T93, T91, T37, T82, T86, T89, T35, T80, T83, T85 |
| Chiffres sans référence comparable : note inchangée, statut E | Épuisement professionnel : 48,6 % des orthophonistes libéraux (enquête CARPIMKO 2020 ; 53,5 % pour l'ensemble des auxiliaires médicaux libéraux), 82 % ont connu un surmenage (FNO) ; environ 35 % des répondants à l'enquête de l'Ordre des chirurgiens-dentistes (2018). Cybersécurité : 62 % jugent leur activité stressante, 88 % sont satisfaits de leurs conditions d'exercice, horaires compris (ANSSI 2025). Dentistes en France : densité projetée en hausse de 39 % de 2021 à 2050 (DREES), un indicateur d'offre qui ne contredit pas la note 5 fondée sur le retour à l'emploi quasi certain. Sans moyenne de tous les actifs mesurée avec la même question, la règle du rapport (1.13) ne s'applique pas (S159, S166). | T15, T05, T91, T92, T83, T89, T90 |
| Robustesse aux notes : 10 000 tirages à poids égaux, graine fixe (20261029) | A (consigne) : chaque note estimée prend un écart de -1, 0 ou +1 avec la même probabilité, indépendamment, borné à [1, 5]. B : écart commun de EP et IT pour tout un groupe de métiers, car ces notes viennent d'une grille par groupe. C : notes estimées et mixtes tirées, CA à 0,5 près (seule la latitude y est estimée) ; notes sourcées et revenu fixes. Rang dans un tirage = 1 + nombre de triplets au score strictement plus élevé, sans la règle d'égalité de 0,03 ; P(1er) partagée en cas d'égalité exacte. Les bornes rendent le tirage asymétrique pour une note de 5 (elle ne peut que baisser) ou de 1. | Tous |

### 1.15 Version 7 (29 octobre 2026) : règles déclarées avant tout calcul

| Règle | Contenu |
|---|---|
| Postes précis | Chaque catégorie large est remplacée par des postes réels codés en CITP-08 à 4 chiffres (OIT) ; le nom exact du poste figure dans les tableaux. Exemples : « cybersécurité » devient analyste SOC, pentesteur, ingénieur sécurité cloud, consultant GRC, RSSI ; « spécialiste libéral » devient chaque spécialité. |
| Classement 1 | Triplets poste × statut × pays en France et en Suisse seulement (Suisse en résident et en frontalier). |
| Classement 2, tri des pays | Tous les pays de l'OCDE, plus Singapour et les Émirats arabes unis. Trois piliers à poids égaux : (1) revenu net après impôt d'un célibataire sans enfant au salaire moyen, en USD PPA (OCDE, Taxing Wages 2026, données 2025) ; (2) heures annuelles effectivement travaillées par travailleur (OCDE ; Singapour et Émirats : sources nationales), moins c'est mieux ; (3) qualité de l'emploi OCDE : part des travailleurs en situation de tension au travail (job strain, 2021), moins c'est mieux. Chaque pilier est ramené à [0, 1] par la méthode min-max sur les pays disponibles. Un pilier sans donnée comparable prend la médiane des pays disponibles (valeur neutre) et le pays est signalé. Score = moyenne des trois piliers ; on garde les 10 premiers, sans repêchage. |
| Tri des pays, valeurs non lues | Une valeur non lue dans une source pendant cette analyse est marquée « connue » (chiffre OCDE connu avant l'analyse, non revérifié) ou « imputée » (calculée ou bornée par d'autres chiffres lus). Robustesse : 10 000 tirages avec un écart uniforme de ± 10 % sur ces valeurs et de ± 3 % sur les valeurs lues ; probabilité de chaque pays d'être dans les 10 premiers. |
| Classement 2, triplets | Les postes du classement 1 qui ont un équivalent international, dans les 10 pays retenus ; la France et la Suisse n'y entrent que si elles passent le tri. |
| Revenu (RE) | Revenu net après impôt sur le revenu (célibataire sans enfant, barème 2025), en équivalent temps plein et en PPA, pour les deux classements. Changement par rapport à la v6 (revenu avant impôt) : il applique aux triplets l'indicateur demandé pour le tri des pays et corrige le biais déclaré en 1.4 en faveur des pays à impôt élevé. Barèmes légaux simplifiés, vérifiés au salaire moyen contre le taux publié par l'OCDE quand il est connu. |
| Notes hors revenu | Méthode v6 inchangée (grilles 1.3 et 1.12, ancrages 1.13, gardes 1.14), appliquée poste par poste ; mêmes notes EP et IT pour un poste dans tous les pays (aucune donnée par métier et par pays) ; PS, ES (règle de langue 1.10) et QT peuvent varier selon le pays. |
| Comparabilité hors Europe | Pour un pays hors Europe, une dimension est signalée « sans donnée comparable » quand l'enquête européenne sur les conditions de travail (Eurofound) ne le couvre pas et qu'aucune enquête équivalente n'a été trouvée. |
| Robustesse | Pour chaque classement : 8 pondérations (poids égaux, puis chaque dimension doublée) et 10 000 tirages des notes estimées (variantes A, B, C de la section 1.14). |
| Conclusion | Le groupe de tête est présenté avec la probabilité de chaque triplet d'être dans les 10 premiers. Un 1er n'est désigné que si un triplet est premier dans plus de 50 % des tirages (variante A). |
| Postes nouveaux | Spécialités libérales françaises : les 13 spécialités dont un revenu publié par la CARMF a été trouvé (radiologue, ophtalmologue, anesthésiste-réanimateur, anatomopathologiste, cancérologue, médecin nucléaire, gastro-entérologue, cardiologue, dermatologue, gynécologue-obstétricien, rhumatologue, psychiatre, pédiatre) ; les autres (ORL, chirurgie orthopédique, pneumologie, neurologie, néphrologie, endocrinologie, etc.) ne sont pas classées faute de montant trouvé. Suisse : psychiatre, pédiatre et ophtalmologue indépendants (seuls groupes de l'OFS 2019 publiés). Cybersécurité : analyste SOC, pentesteur, ingénieur sécurité cloud, consultant GRC et RSSI, en France et en Suisse. Ajouts : administrateur P-3 des Nations unies à Genève et enseignant du secondaire I à Genève (équivalents suisses des postes publics et européens du pool), notaire (profession juridique libérale à revenu publié). |
| Médecins libéraux français, revenu | Une seule source pour toutes les spécialités : CARMF 2023, revenu net d'activité indépendante moyen (nouvelle méthode), × 0,96 × 0,85 (règles 1.4) ; elle remplace la DREES 2021 pour le généraliste (T01 devient F01 : 89 238 € au lieu de 98 300 €). Montants 2024 ou d'année incertaine signalés. |
| Notes des postes nouveaux | Grille 1.3 appliquée au poste, à partir du triplet v6 d'origine (code src) ; chaque écart est justifié : EP 3 pour une exposition régulière aux rayonnements, aux produits chimiques ou aux risques biologiques ; IT 2 pour la vigilance de sécurité ou des exigences émotionnelles fortes ; F3 pour les astreintes de bloc et de maternité, et pour les gardes obligatoires des médecins indépendants suisses (règle 1.14). Statut E sauf ancrage hérité ou étendu (un ancrage étendu est au mieux M). |
| Impôt, barèmes | France : barème 2025 des revenus 2024, une part, décote et contribution sur les hauts revenus ; salariés : net imposable = net × 1,035 moins 10 % de frais (plafond 14 171 €) ; libéraux : bénéfice = net / 0,96. Suisse, résidents et frontaliers : impôt à la source genevois, barème A0, en % du brut (points lus : 16,5 % à 100 000 CHF, 22,5 % à 200 000, 25 % à 300 000 ; points intermédiaires estimés, S179) ; indépendants : même taux sur le revenu avant prime LAMal (approximation, impôt ordinaire non calculé). Fonctionnaires internationaux : exonérés. Autres pays : barèmes 2025 simplifiés (`fiscalite_v7.py`), vérifiés au salaire moyen contre les taux de l'OCDE. |
| Robustesse, variante D (revenu) | Ajoutée aux variantes A, B, C : notes estimées tirées comme en A, et chaque cellule revenu multipliée par un facteur uniforme commun à sa médiane et à son P80, ± 20 % si la cellule est estimée, non officielle, proxy, ancienne, d'année incertaine ou tirée de la règle de structure, ± 5 % sinon ; bornes de l'échelle logarithmique fixes. |
| Classement 2, statuts | Le poste garde son statut français ou suisse (« libéral » devient « indépendant » ; « fonctionnaire » devient « salarié du secteur public », avec PS moins 1 hors Allemagne, Autriche et Luxembourg, où ce statut protégé existe). Spécialités médicales libérales transposées seulement là où l'exercice libéral des spécialistes est courant (Allemagne, Autriche, Luxembourg, Pays-Bas) ; ailleurs le spécialiste est représenté par la grille hospitalière lue du pays. |
| Classement 2, revenu sans donnée lue | Règle de structure : brut = rapport du poste au salaire moyen en France (cellule / 0,78 / 45 964 €, salaire moyen OCDE 2025) et en Suisse (cellule / 0,80 / 100 700 CHF), moyenne géométrique quand les deux existent, × salaire moyen OCDE 2025 du pays (Taxing Wages 2026) ; cellule signalée « estimé (structure) ». Une donnée lue dans une source nationale ou internationale remplace la règle. |
| Classement 2, sélection des postes | Postes dont un triplet est dans les 30 premiers du classement 1, plus les fonctionnaires internationaux (Nations unies à Genève, Union européenne à Luxembourg) ; contrôle : tout poste exclu dont le score maximal possible (RE = 5, sans pénalité de langue) atteint le 10e score du classement 2 est ajouté et le calcul refait. La Suisse entre avec tous ses triplets du classement 1. |
| Classement 2, langue | Règle 1.10 maintenue : ES moins 1 dans les pays non francophones (tous sauf la Suisse romande et le Luxembourg) ; sensibilité sans cette règle publiée à titre informatif. |
| Classement 2, prix et change | Indices de niveau des prix 2024 (consommation des ménages, UE = 100) : Danemark 143, Luxembourg 133, Autriche 111,7, Allemagne 108,3, Suisse 174, Islande 162, Norvège 124 (lus, S190) ; Pays-Bas 118, Slovénie 90, Royaume-Uni 115 (connus, non revérifiés) ; change de référence BCE, moyennes 2024 et 2025 (S191). |
| Classement 2, plafond de structure | Pour une spécialité médicale transposée, le rapport au salaire moyen tiré de la règle de structure est plafonné à 5, haut de la fourchette des spécialistes indépendants publiée par l'OCDE (trois à cinq fois le salaire moyen, S189) ; notes du poste = celles de son meilleur triplet au classement 1. Luxembourg : postes salariés en résident et en frontalier (résidence en France, surcoût régional de 5 %, impôt luxembourgeois). |

## 2. Tri des pays (OCDE, Singapour, Émirats arabes unis)

### Tri des pays : 40 pays, trois piliers, 10 retenus

| Rang | Pays | Net au salaire moyen, USD PPA 2025 (provenance) | Heures par an (provenance) | Tension au travail 2021 (provenance) | P(10 premiers), 10 000 tirages | Retenu |
|---|---|---|---|---|---|---|
| 1 | Pays-Bas | 67 017 (lu) | 1 417 (lu) | 9 % (imputé) | 100 % | oui |
| 2 | Suisse | 87 303 (lu) | 1 533 (lu) | 13 % (imputé) | 100 % | oui |
| 3 | Norvège | 63 052 (lu) | 1 407 (lu) | 13 % (imputé) | 99 % | oui |
| 4 | Allemagne | 57 600 (imputé) | 1 331 (lu) | 13 % (imputé) | 96 % | oui |
| 5 | Luxembourg | 63 385 (lu) | 1 450 (imputé) | 13 % (imputé) | 91 % | oui |
| 6 | Islande | 60 863 (lu) | 1 433 (lu) | sans donnée comparable (médiane) | 100 % | oui |
| 7 | Danemark | 57 205 (lu) | 1 379 (lu) | 13 % (imputé) | 92 % | oui |
| 8 | Royaume-Uni | 63 277 (lu) | 1 524 (connu) | sans donnée comparable (médiane) | 85 % | oui |
| 9 | Autriche | 57 600 (imputé) | 1 442 (lu) | 13 % (imputé) | 78 % | oui |
| 10 | Slovénie | 34 100 (imputé) | 1 593 (connu) | 9 % (imputé) | 69 % | oui |
| 11 | Suède | 48 500 (connu) | 1 444 (lu) | 13 % (imputé) | 29 % | non |
| 12 | Estonie | 33 000 (connu) | 1 742 (connu) | 9 % (imputé) | 20 % | non |
| 13 | Portugal | 30 000 (connu) | 1 696 (connu) | 9 % (imputé) | 18 % | non |
| 14 | Belgique | 49 000 (connu) | 1 493 (lu) | 13 % (imputé) | 16 % | non |
| 15 | Canada | 60 811 (lu) | 1 685 (lu) | sans donnée comparable (médiane) | 3 % | non |
| 16 | Australie | 60 275 (lu) | 1 694 (lu) | sans donnée comparable (médiane) | 1 % | non |
| 17 | Irlande | 60 500 (imputé) | 1 775 (lu) | 13 % (imputé) | 4 % | non |
| 18 | États-Unis | 55 580 (imputé) | 1 796 (lu) | sans donnée comparable (médiane) | 0 % | non |
| 19 | Japon | 43 000 (connu) | 1 607 (lu) | sans donnée comparable (médiane) | 0 % | non |
| 20 | Espagne | 38 000 (connu) | 1 632 (connu) | 13 % (imputé) | 0 % | non |
| 21 | Nouvelle-Zélande | 44 000 (connu) | 1 730 (lu) | sans donnée comparable (médiane) | 0 % | non |
| 22 | Corée | 55 000 (imputé) | 1 910 (lu) | sans donnée comparable (médiane) | 0 % | non |
| 23 | Lituanie | 32 000 (connu) | 1 597 (connu) | 13 % (imputé) | 0 % | non |
| 24 | Lettonie | 26 000 (connu) | 1 547 (connu) | 13 % (imputé) | 0 % | non |
| 25 | Slovaquie | 27 000 (connu) | 1 589 (connu) | 13 % (imputé) | 0 % | non |
| 26 | Italie | 36 000 (connu) | 1 734 (connu) | 13 % (imputé) | 0 % | non |
| 27 | Émirats arabes unis | 83 500 (imputé) | 2 496 (imputé) | sans donnée comparable (médiane) | 0 % | non |
| 28 | Israël | 40 000 (connu) | 1 880 (connu) | sans donnée comparable (médiane) | 0 % | non |
| 29 | Hongrie | 26 000 (connu) | 1 680 (connu) | 13 % (imputé) | 0 % | non |
| 30 | Türkiye | 29 000 (connu) | 1 732 (connu) | sans donnée comparable (médiane) | 0 % | non |
| 31 | Pologne | 32 000 (connu) | 1 803 (connu) | 13 % (imputé) | 0 % | non |
| 32 | Finlande | 46 000 (connu) | 1 518 (lu) | 17 % (lu) | 0 % | non |
| 33 | Singapour | 57 300 (imputé) | 2 298 (imputé) | sans donnée comparable (médiane) | 0 % | non |
| 34 | France | 46 000 (connu) | 1 490 (lu) | 18 % (lu) | 0 % | non |
| 35 | Grèce | 26 000 (connu) | 1 897 (connu) | 13 % (imputé) | 0 % | non |
| 36 | Chili | 22 000 (connu) | 1 953 (connu) | sans donnée comparable (médiane) | 0 % | non |
| 37 | Tchéquie | 32 000 (connu) | 1 754 (connu) | 17 % (lu) | 0 % | non |
| 38 | Costa Rica | 19 000 (connu) | 2 149 (connu) | sans donnée comparable (médiane) | 0 % | non |
| 39 | Mexique | 15 000 (connu) | 2 207 (connu) | sans donnée comparable (médiane) | 0 % | non |
| 40 | Colombie | 13 000 (connu) | 2 297 (connu) | sans donnée comparable (médiane) | 0 % | non |

Lecture : l'ordre suit la moyenne des trois piliers ramenés à [0, 1] (règle 1.15) ; l'indice lui-même n'est pas affiché (pas de score décimal). « lu » : lu dans une source pendant l'analyse ; « imputé » : calculé ou borné à partir de chiffres lus ; « connu » : chiffre OCDE connu avant l'analyse, non revérifié. Sources : S167 (revenu), S168 à S172 (heures), S173 (tension).

Pays hors Europe sans donnée comparable de tension au travail (enquête européenne EWCTS 2021) : Canada, Australie, États-Unis, Corée, Japon, Israël, Nouvelle-Zélande, Mexique, Chili, Colombie, Costa Rica, Singapour, Émirats arabes unis. En Europe, l'Islande, le Royaume-Uni et la Türkiye n'ont pas non plus de valeur publiée. Aucun pays hors Europe n'entre dans les 10 premiers : le meilleur, le Canada, est 15e (5 % des tirages dans les 10 premiers).

## 3. Classement 1 : France et Suisse (111 triplets, postes précis)

Lecture des colonnes : EP environnement physique, IT intensité du travail, QT qualité du temps de travail, ES environnement social, CA compétences et autonomie, PS perspectives et sécurité, RE revenu net après impôt ; notes de 1 (mauvais) à 5 (bon), poids égaux. CA et RE sont continues, les autres entières. Palier : S ≥ 4,2, A ≥ 3,6, B ≥ 3,0, C en dessous ; * = à moins de 0,1 d'une frontière. « 2= » : rang partagé (écart inférieur à 0,03). P(10 premiers) : part des 10 000 tirages de la variante A où le triplet est dans les 10 premiers.

### Classement 1, catalogue des postes (111 triplets)

| ID | Poste exact | CITP-08 | Statut | Pays | Origine v6 | Écart à la note d'origine, justification |
|---|---|---|---|---|---|---|
| C20 | Administrateur de programme (P-3), Nations unies, Genève | 2422 | fonctionnaire international | Suisse (résident) | T64 | notes de l'administrateur de l'UE (T64) ; PS 3 au lieu de 5 : contrats à durée déterminée renouvelables et suppressions de postes annoncées en 2025 et 2026 à Genève (grille 1.3 : marché moyen, cyclique) |
| C21 | Administrateur de programme (P-3), Nations unies, Genève | 2422 | fonctionnaire international | Suisse (frontalier) | T64 | notes de l'administrateur de l'UE (T64) ; PS 3 au lieu de 5 : contrats à durée déterminée renouvelables et suppressions de postes annoncées en 2025 et 2026 à Genève (grille 1.3 : marché moyen, cyclique) |
| C10 | Analyste SOC (niveaux 1 et 2) | 2529 | salarié | Suisse (résident) | T84 | poste précis issu de T89 ; notes de T89 et de T84 (SOC) |
| C11 | Analyste SOC (niveaux 1 et 2) | 2529 | salarié | Suisse (frontalier) | T84 | poste précis issu de T89 ; notes de T89 et de T84 (SOC) |
| T33r | Assistant en soins et santé communautaire (ASSC) | 5321 | salarié | Suisse (résident) | T33 |  |
| T33 | Assistant en soins et santé communautaire (ASSC) | 5321 | salarié | Suisse (frontalier) | T33 |  |
| C16 | Consultant GRC (gouvernance, risques et conformité) | 2529 | salarié | Suisse (résident) | T89 | poste précis issu de T89 ; notes de T89 |
| C17 | Consultant GRC (gouvernance, risques et conformité) | 2529 | salarié | Suisse (frontalier) | T89 | poste précis issu de T89 ; notes de T89 |
| T37r | Développeur logiciel | 2512 | salarié | Suisse (résident) | T37 |  |
| T37 | Développeur logiciel | 2512 | salarié | Suisse (frontalier) | T37 |  |
| C22 | Enseignant du secondaire I (cycle d'orientation), Genève | 2330 | fonctionnaire cantonal | Suisse (résident) | T57 | notes du professeur certifié français (T57), ancrages français ramenés au statut mixte (autre pays) ; frontalier non retenu (condition de résidence non vérifiée) |
| T23 | Infirmier en soins généraux hospitalier | 2221 | salarié | Suisse (résident) | T23 |  |
| T24 | Infirmier en soins généraux hospitalier | 2221 | salarié | Suisse (frontalier) | T24 |  |
| T86 | Ingénieur cloud DevOps | 2522 | salarié | Suisse (résident) | T86 |  |
| T82 | Ingénieur cloud DevOps | 2522 | salarié | Suisse (frontalier) | T82 |  |
| T42r | Ingénieur méthodes et industrialisation | 2141 | salarié | Suisse (résident) | T42 |  |
| T42 | Ingénieur méthodes et industrialisation | 2141 | salarié | Suisse (frontalier) | T42 |  |
| C14 | Ingénieur sécurité cloud | 2529 | salarié | Suisse (résident) | T89 | poste précis issu de T89 ; notes de T89 |
| C15 | Ingénieur sécurité cloud | 2529 | salarié | Suisse (frontalier) | T89 | poste précis issu de T89 ; notes de T89 |
| T54 | Mécanicien de locomotive (CFF) | 8311 | salarié | Suisse (résident) | T54 |  |
| T30 | Médecin de famille (médecine interne générale) | 2211 | indépendant | Suisse (résident) | T30 |  |
| T29 | Médecin hospitalier (chef de clinique à médecin adjoint) | 2212 | salarié (hôpital) | Suisse (résident) | T29 |  |
| T29f | Médecin hospitalier (chef de clinique à médecin adjoint) | 2212 | salarié (hôpital) | Suisse (frontalier) | T29 |  |
| T91 | Médecin-dentiste | 2261 | indépendant | Suisse (résident) | T91 |  |
| C03 | Ophtalmologue | 2212 | indépendant | Suisse (résident) | T30 | F1 transposé du spécialiste français ; F3 : gardes obligatoires (Q15) ; Q10 et P8 retirés |
| C12 | Pentesteur (auditeur en tests d'intrusion) | 2529 | salarié | Suisse (résident) | T89 | poste précis issu de T89 ; notes de T89 |
| C13 | Pentesteur (auditeur en tests d'intrusion) | 2529 | salarié | Suisse (frontalier) | T89 | poste précis issu de T89 ; notes de T89 |
| T34r | Physiothérapeute | 2264 | salarié | Suisse (résident) | T34 |  |
| T34 | Physiothérapeute | 2264 | salarié | Suisse (frontalier) | T34 |  |
| C01 | Psychiatre | 2212 | indépendant | Suisse (résident) | T30 | F1 transposé du spécialiste français (heures non trouvées) ; F3 : gardes obligatoires des indépendants (Q15, 1,14) ; Q10 et P8 propres au premier recours, retirés |
| C02 | Pédiatre | 2212 | indépendant | Suisse (résident) | T30 | premier recours : Q10 (43 h) et P8 (pénurie) gardés en mixte ; F3 : gardes obligatoires (Q15) |
| C18 | Responsable de la sécurité des systèmes d'information (RSSI) | 1330 | salarié | Suisse (résident) | T89 | poste précis issu de T89 ; notes de T89 ; IT 2 et F3 comme le RSSI français |
| C19 | Responsable de la sécurité des systèmes d'information (RSSI) | 1330 | salarié | Suisse (frontalier) | T89 | poste précis issu de T89 ; notes de T89 ; IT 2 et F3 comme le RSSI français |
| T49r | Électricien de montage (CFC) | 7411 | salarié | Suisse (résident) | T49 |  |
| T49 | Électricien de montage (CFC) | 7411 | salarié | Suisse (frontalier) | T49 |  |
| T46 | Actuaire | 2120 | salarié | France | T46 |  |
| T73 | Agent immobilier | 3334 | indépendant (mandataire) | France | T73 |  |
| T21 | Aide-soignant hospitalier | 5321 | fonctionnaire FPH | France | T21 |  |
| T84 | Analyste SOC (niveaux 1 et 2) | 2529 | salarié | France | T84 |  |
| F05 | Anatomopathologiste | 2212 | libéral | France | T03 | EP 3 : fixateurs et solvants (formol, xylène) ; IA : lecture de lames numérisées |
| F04 | Anesthésiste-réanimateur | 2212 | libéral | France | T03 | exercice en clinique : EP 3 (gaz anesthésiques, risques biologiques), IT 2 (vigilance de sécurité), F3 (astreintes de continuité des soins chirurgicaux et obstétricaux) ; ancrages des médecins de ville (Q2, Q18) retirés, ancrage des médecins hospitaliers (Q3) étendu en mixte |
| T72 | Attaché commercial B2B | 3322 | salarié | France | T72 |  |
| T60 | Attaché d'administration de l'État | 2422 | fonctionnaire | France | T60 |  |
| T18 | Audioprothésiste | 2266 | salarié | France | T18 |  |
| T67 | Avocat | 2611 | libéral | France | T67 |  |
| F06 | Cancérologue (oncologie médicale et radiothérapie) | 2212 | libéral | France | T03 | IT 2 : exigences émotionnelles fortes et fréquentes (annonce, fin de vie) |
| F09 | Cardiologue | 2212 | libéral | France | T03 |  |
| T05 | Chirurgien-dentiste omnipraticien | 2261 | libéral | France | T05 |  |
| T69 | Comptable | 3313 | salarié | France | T69 |  |
| T53 | Conducteur de train | 8311 | salarié (SNCF) | France | T53 |  |
| T55 | Conducteur routier poids lourd | 8332 | salarié | France | T55 |  |
| F17 | Consultant GRC (gouvernance, risques et conformité) | 2529 | salarié | France | T83 | IA élevée : rédaction documentaire et contrôles de conformité automatisables |
| T63 | Contrôleur aérien (ICNA) | 3154 | fonctionnaire | France | T63 |  |
| T62 | Contrôleur des finances publiques | 3352 | fonctionnaire | France | T62 |  |
| T85 | Data engineer (ingénieur des données) | 2521 | salarié | France | T85 |  |
| F10 | Dermatologue | 2212 | libéral | France | T03 | IA : classement d'images de lésions |
| T78 | Diététicien | 2265 | libéral | France | T78 |  |
| T36 | Développeur logiciel | 2512 | indépendant (freelance) | France | T36 |  |
| T35 | Développeur logiciel (études et développement) | 2512 | salarié | France | T35 |  |
| T77 | Ergothérapeute hospitalier | 2269 | fonctionnaire FPH | France | T77 |  |
| T68 | Expert-comptable | 2411 | libéral | France | T68 |  |
| T52 | Frigoriste (froid et climatisation) | 7127 | salarié | France | T52 |  |
| T58 | Gardien de la paix | 5412 | fonctionnaire | France | T58 |  |
| F08 | Gastro-entérologue | 2212 | libéral | France | T03 | EP 3 : endoscopies (risques biologiques, postures) |
| F11 | Gynécologue-obstétricien | 2212 | libéral | France | T03 | EP 3 et IT 2 : urgences obstétricales ; F3 : astreintes de maternité ; ancrages Q2 et Q18 retirés, Q3 étendu en mixte |
| T14 | Infirmier anesthésiste (IADE) | 2221 | fonctionnaire FPH | France | T14 |  |
| T13 | Infirmier en soins généraux (IDE) | 2221 | libéral | France | T13 |  |
| T12 | Infirmier en soins généraux (IDE) hospitalier | 2221 | fonctionnaire FPH | France | T12 |  |
| T80 | Ingénieur cloud DevOps | 2522 | salarié | France | T80 |  |
| T81 | Ingénieur cloud DevOps | 2522 | indépendant (freelance) | France | T81 |  |
| T41 | Ingénieur méthodes et industrialisation | 2141 | salarié | France | T41 |  |
| F16 | Ingénieur sécurité cloud | 2529 | salarié | France | T83 |  |
| T61 | Inspecteur des finances publiques | 2411 | fonctionnaire | France | T61 |  |
| T71 | Magistrat de l'ordre judiciaire | 2612 | fonctionnaire | France | T71 |  |
| T17 | Manipulateur en électroradiologie médicale (MERM) | 3211 | fonctionnaire FPH | France | T17 |  |
| T10 | Masseur-kinésithérapeute | 2264 | libéral | France | T10 |  |
| T11 | Masseur-kinésithérapeute hospitalier | 2264 | fonctionnaire FPH | France | T11 |  |
| T02 | Médecin généraliste | 2211 | salarié (centre de santé) | France | T02 |  |
| F01 | Médecin généraliste | 2211 | libéral | France | T01 |  |
| F07 | Médecin nucléaire | 2212 | libéral | France | T03 | EP 3 : sources radioactives non scellées |
| F19 | Notaire | 2619 | libéral | France | nouveau | notes estimées : C 4 (office propre), R 3 (clients en transaction), Se 4 (profession réglementée, activité immobilière cyclique), F1 et F2 (charge d'actes et responsabilité) |
| F03 | Ophtalmologue | 2212 | libéral | France | T03 |  |
| T79 | Opticien-lunetier | 3254 | salarié | France | T79 |  |
| T15 | Orthophoniste | 2266 | libéral | France | T15 |  |
| T16 | Orthoptiste | 2267 | salarié | France | T16 |  |
| T22 | Ostéopathe | 2230 | libéral | France | T22 |  |
| F15 | Pentesteur (auditeur en tests d'intrusion) | 2529 | salarié | France | T83 |  |
| T06 | Pharmacien adjoint d'officine | 2262 | salarié | France | T06 |  |
| T07 | Pharmacien titulaire d'officine | 2262 | indépendant | France | T07 |  |
| T74 | Pilote de ligne | 3153 | salarié | France | T74 |  |
| T51 | Plombier-chauffagiste | 7126 | artisan | France | T51 |  |
| T04 | Praticien hospitalier (spécialiste, grille commune à toutes les spécialités) | 2212 | statut PH (public) | France | T04 |  |
| T57 | Professeur certifié (collège et lycée) | 2330 | fonctionnaire | France | T57 |  |
| T56 | Professeur des écoles | 2341 | fonctionnaire | France | T56 |  |
| F13 | Psychiatre | 2212 | libéral | France | T03 | EP 5 : cabinet sans contrainte physique |
| T20 | Psychologue hospitalier | 2634 | contractuel FPH | France | T20 |  |
| F14 | Pédiatre | 2212 | libéral | France | T03 |  |
| T76 | Pédicure-podologue | 2269 | libéral | France | T76 |  |
| F02 | Radiologue | 2212 | libéral | France | T03 | EP 3 : rayonnements ionisants réguliers (grille 1.3) ; IA : imagerie, exposition la plus citée |
| F18 | Responsable de la sécurité des systèmes d'information (RSSI) | 1330 | salarié | France | T83 | IT 2 : gestion de crise, responsabilité ; F3 : astreintes de crise (Q19, mixte) |
| F12 | Rhumatologue | 2212 | libéral | France | T03 |  |
| T09 | Sage-femme | 2222 | libéral | France | T09 |  |
| T08 | Sage-femme hospitalière | 2222 | fonctionnaire FPH | France | T08 |  |
| T59 | Sapeur-pompier professionnel | 5411 | fonctionnaire territorial | France | T59 |  |
| T66 | Sous-officier de l'armée de Terre | 0210 | militaire | France | T66 |  |
| T44 | Technicien de maintenance industrielle | 3115 | salarié | France | T44 |  |
| T45 | Technicien systèmes et réseaux | 3513 | salarié | France | T45 |  |
| T75 | Vendeur en magasin (référence) | 5223 | salarié | France | T75 |  |
| T19 | Vétérinaire praticien | 2250 | libéral | France | T19 |  |
| T47 | Électricien du bâtiment | 7411 | salarié | France | T47 |  |
| T48 | Électricien du bâtiment | 7411 | artisan | France | T48 |  |

### Classement 1, partie A : notes des 7 dimensions, palier et probabilité d'être dans les 10 premiers

| Rang | ID | Triplet | EP | IT | QT | ES | CA | PS | RE | Palier | Top 10 (sur 8 pondérations) | P(10 premiers), variante A |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | T15 | Orthophoniste × libéral × France | 5 | 4 | 5 | 4 | 5,0 | 5 | 1,3 | A* | 7 | 44 % |
| 2= | C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,2 | A* | 7 | 49 % |
| 2= | C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,1 | A | 7 | 48 % |
| 2= | F03 | Ophtalmologue × libéral × France | 4 | 3 | 4 | 4 | 4,5 | 5 | 4,1 | A | 6 | 47 % |
| 2= | C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,1 | A | 7 | 41 % |
| 2= | F13 | Psychiatre × libéral × France | 5 | 3 | 4 | 4 | 4,5 | 5 | 3,0 | A | 7 | 30 % |
| 7= | F06 | Cancérologue (oncologie médicale et radiothérapie) × libéral × France | 4 | 2 | 4 | 4 | 4,5 | 5 | 5,0 | A | 5 | 39 % |
| 7= | F09 | Cardiologue × libéral × France | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,9 | A | 6 | 37 % |
| 9= | C02 | Pédiatre × indépendant × Suisse (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,8 | A | 6 | 36 % |
| 9= | T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,8 | A | 6 | 36 % |
| 9= | F16 | Ingénieur sécurité cloud × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,6 | A | 3 | 30 % |
| 9= | C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,6 | A | 3 | 30 % |
| 13= | C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,5 | A | 2 | 29 % |
| 13= | C03 | Ophtalmologue × indépendant × Suisse (résident) | 4 | 3 | 3 | 4 | 4,5 | 5 | 4,5 | A | 2 | 25 % |
| 13= | C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,4 | A | 2 | 28 % |
| 13= | T09 | Sage-femme × libéral × France | 4 | 3 | 5 | 4 | 5,0 | 5 | 1,9 | A | 3 | 15 % |
| 13= | T46 | Actuaire × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,4 | A | 2 | 19 % |
| 13= | F07 | Médecin nucléaire × libéral × France | 3 | 3 | 4 | 4 | 4,5 | 5 | 4,3 | A | 2 | 29 % |
| 13= | F17 | Consultant GRC (gouvernance, risques et conformité) × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,3 | A | 0 | 23 % |
| 13= | F19 | Notaire × libéral × France | 5 | 3 | 4 | 3 | 4,5 | 4 | 4,3 | A | 1 | 24 % |
| 21= | F10 | Dermatologue × libéral × France | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,2 | A | 1 | 27 % |
| 21= | T37 | Développeur logiciel × salarié × Suisse (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 3 | 3,1 | A | 0 | 13 % |
| 21= | T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | 5 | 3 | 4 | 4 | 4,5 | 4 | 3,1 | A | 0 | 21 % |
| 21= | T16 | Orthoptiste × salarié × France | 5 | 4 | 4 | 4 | 4,0 | 5 | 1,6 | A | 1 | 9 % |
| 21= | F12 | Rhumatologue × libéral × France | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,1 | A | 0 | 19 % |
| 21= | F02 | Radiologue × libéral × France | 3 | 3 | 4 | 4 | 4,5 | 5 | 4,1 | A | 1 | 19 % |
| 21= | F15 | Pentesteur (auditeur en tests d'intrusion) × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,1 | A | 0 | 15 % |
| 21= | F05 | Anatomopathologiste × libéral × France | 3 | 3 | 4 | 4 | 4,5 | 5 | 4,1 | A | 1 | 18 % |
| 21= | T85 | Data engineer (ingénieur des données) × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,0 | A | 0 | 9 % |
| 30= | C01 | Psychiatre × indépendant × Suisse (résident) | 5 | 3 | 3 | 4 | 4,5 | 5 | 3,0 | A | 0 | 6 % |
| 30= | C19 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × Suisse (frontalier) | 5 | 2 | 4 | 4 | 4,5 | 4 | 4,0 | A | 0 | 12 % |
| 30= | F01 | Médecin généraliste × libéral × France | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,0 | A | 0 | 16 % |
| 30= | T91 | Médecin-dentiste × indépendant × Suisse (résident) | 3 | 3 | 4 | 4 | 5,0 | 5 | 3,4 | A | 0 | 11 % |
| 30= | F14 | Pédiatre × libéral × France | 4 | 3 | 4 | 4 | 4,5 | 5 | 2,9 | A | 0 | 16 % |
| 30= | T35 | Développeur logiciel (études et développement) × salarié × France | 5 | 3 | 5 | 4 | 4,5 | 4 | 1,9 | A | 0 | 8 % |
| 30= | T05 | Chirurgien-dentiste omnipraticien × libéral × France | 3 | 3 | 4 | 4 | 5,0 | 5 | 3,3 | A | 0 | 7 % |
| 37= | F08 | Gastro-entérologue × libéral × France | 3 | 3 | 4 | 4 | 4,5 | 5 | 3,8 | A | 0 | 14 % |
| 37= | T10 | Masseur-kinésithérapeute × libéral × France | 2 | 4 | 5 | 4 | 5,0 | 5 | 2,2 | A | 1 | 6 % |
| 37= | T71 | Magistrat de l'ordre judiciaire × fonctionnaire × France | 5 | 3 | 4 | 3 | 4,5 | 5 | 2,6 | A | 0 | 14 % |
| 40= | T37r | Développeur logiciel × salarié × Suisse (résident) | 5 | 3 | 5 | 4 | 4,5 | 3 | 2,5 | A | 0 | 5 % |
| 40= | T86 | Ingénieur cloud DevOps × salarié × Suisse (résident) | 5 | 3 | 4 | 4 | 4,5 | 4 | 2,5 | A | 0 | 12 % |
| 40= | T41 | Ingénieur méthodes et industrialisation × salarié × France | 4 | 3 | 5 | 4 | 4,5 | 4 | 2,4 | A | 0 | 5 % |
| 40= | C22 | Enseignant du secondaire I (cycle d'orientation), Genève × fonctionnaire cantonal × Suisse (résident) | 4 | 3 | 5 | 3 | 4,5 | 5 | 2,4 | A | 0 | 0 % |
| 40= | C18 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × Suisse (résident) | 5 | 2 | 4 | 4 | 4,5 | 4 | 3,3 | A | 0 | 7 % |
| 45= | T81 | Ingénieur cloud DevOps × indépendant (freelance) × France | 5 | 3 | 5 | 3 | 5,0 | 3 | 2,8 | A | 0 | 2 % |
| 45= | T76 | Pédicure-podologue × libéral × France | 3 | 4 | 5 | 4 | 5,0 | 4 | 1,7 | A | 0 | 6 % |
| 45= | T80 | Ingénieur cloud DevOps × salarié × France | 5 | 3 | 4 | 4 | 4,5 | 4 | 2,1 | A | 0 | 6 % |
| 45= | T42 | Ingénieur méthodes et industrialisation × salarié × Suisse (frontalier) | 4 | 3 | 5 | 4 | 4,5 | 3 | 3,1 | A | 0 | 4 % |
| 49= | T77 | Ergothérapeute hospitalier × fonctionnaire FPH × France | 4 | 4 | 4 | 4 | 4,0 | 5 | 1,5 | A | 0 | 5 % |
| 49= | T68 | Expert-comptable × libéral × France | 5 | 3 | 4 | 3 | 4,5 | 4 | 3,0 | A | 0 | 5 % |
| 49= | T02 | Médecin généraliste × salarié (centre de santé) × France | 4 | 3 | 4 | 4 | 4,0 | 5 | 2,5 | A | 0 | 4 % |
| 49= | F18 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × France | 5 | 2 | 4 | 4 | 4,5 | 4 | 2,8 | A | 0 | 0 % |
| 53 | T56 | Professeur des écoles × fonctionnaire × France | 4 | 3 | 5 | 3 | 4,5 | 5 | 1,8 | A | 0 | 0 % |
| 54= | T20 | Psychologue hospitalier × contractuel FPH × France | 5 | 3 | 5 | 4 | 4,5 | 3 | 1,5 | A | 0 | 1 % |
| 54= | T62 | Contrôleur des finances publiques × fonctionnaire × France | 5 | 4 | 4 | 3 | 3,3 | 5 | 1,7 | A | 0 | 2 % |
| 54= | T60 | Attaché d'administration de l'État × fonctionnaire × France | 5 | 3 | 4 | 3 | 4,0 | 5 | 2,0 | A | 0 | 3 % |
| 54= | T61 | Inspecteur des finances publiques × fonctionnaire × France | 5 | 3 | 4 | 3 | 4,0 | 5 | 2,0 | A | 0 | 3 % |
| 54= | T42r | Ingénieur méthodes et industrialisation × salarié × Suisse (résident) | 4 | 3 | 5 | 4 | 4,5 | 3 | 2,4 | A | 0 | 2 % |
| 59= | C21 | Administrateur de programme (P-3), Nations unies, Genève × fonctionnaire international × Suisse (frontalier) | 5 | 3 | 4 | 3 | 4,0 | 3 | 3,8 | A* | 0 | 4 % |
| 59= | T78 | Diététicien × libéral × France | 5 | 4 | 5 | 4 | 4,5 | 2 | 1,3 | A* | 0 | 0 % |
| 59= | T34 | Physiothérapeute × salarié × Suisse (frontalier) | 2 | 4 | 4 | 4 | 4,0 | 5 | 2,7 | A* | 0 | 1 % |
| 59= | F04 | Anesthésiste-réanimateur × libéral × France | 3 | 2 | 3 | 4 | 4,5 | 5 | 4,2 | A* | 0 | 2 % |
| 63= | T36 | Développeur logiciel × indépendant (freelance) × France | 5 | 3 | 5 | 3 | 5,0 | 2 | 2,5 | A* | 0 | 0 % |
| 63= | T57 | Professeur certifié (collège et lycée) × fonctionnaire × France | 4 | 3 | 5 | 2 | 4,5 | 5 | 1,9 | A* | 0 | 0 % |
| 65= | C20 | Administrateur de programme (P-3), Nations unies, Genève × fonctionnaire international × Suisse (résident) | 5 | 3 | 4 | 3 | 4,0 | 3 | 3,2 | B* | 0 | 1 % |
| 65= | T34r | Physiothérapeute × salarié × Suisse (résident) | 2 | 4 | 4 | 4 | 4,0 | 5 | 2,1 | B* | 0 | 0 % |
| 65= | T63 | Contrôleur aérien (ICNA) × fonctionnaire × France | 5 | 2 | 3 | 4 | 2,8 | 5 | 3,2 | B* | 0 | 0 % |
| 68 | T18 | Audioprothésiste × salarié × France | 4 | 4 | 3 | 4 | 4,0 | 4 | 1,9 | B* | 0 | 1 % |
| 69= | F11 | Gynécologue-obstétricien × libéral × France | 3 | 2 | 3 | 4 | 4,5 | 5 | 3,1 | B* | 0 | 0 % |
| 69= | T11 | Masseur-kinésithérapeute hospitalier × fonctionnaire FPH × France | 2 | 4 | 4 | 4 | 4,0 | 5 | 1,6 | B* | 0 | 0 % |
| 71 | T22 | Ostéopathe × libéral × France | 3 | 4 | 5 | 4 | 5,0 | 2 | 1,1 | B | 0 | 0 % |
| 72= | T72 | Attaché commercial B2B × salarié × France | 4 | 3 | 5 | 3 | 3,8 | 3 | 2,0 | B | 0 | 0 % |
| 72= | T13 | Infirmier en soins généraux (IDE) × libéral × France | 2 | 3 | 3 | 4 | 4,5 | 5 | 2,3 | B | 0 | 0 % |
| 72= | T69 | Comptable × salarié × France | 5 | 4 | 4 | 3 | 3,3 | 3 | 1,5 | B | 0 | 0 % |
| 72= | T67 | Avocat × libéral × France | 5 | 3 | 3 | 3 | 4,0 | 3 | 2,8 | B | 0 | 0 % |
| 76= | C11 | Analyste SOC (niveaux 1 et 2) × salarié × Suisse (frontalier) | 5 | 2 | 3 | 3 | 3,5 | 4 | 3,0 | B | 0 | 0 % |
| 76= | T06 | Pharmacien adjoint d'officine × salarié × France | 4 | 3 | 3 | 3 | 3,5 | 5 | 1,9 | B | 0 | 0 % |
| 78= | T19 | Vétérinaire praticien × libéral × France | 2 | 3 | 3 | 3 | 4,5 | 5 | 2,6 | B | 0 | 0 % |
| 78= | T45 | Technicien systèmes et réseaux × salarié × France | 4 | 4 | 3 | 3 | 3,3 | 4 | 1,8 | B | 0 | 0 % |
| 78= | T29f | Médecin hospitalier (chef de clinique à médecin adjoint) × salarié (hôpital) × Suisse (frontalier) | 3 | 2 | 2 | 3 | 4,0 | 5 | 4,1 | B | 0 | 0 % |
| 81 | C10 | Analyste SOC (niveaux 1 et 2) × salarié × Suisse (résident) | 5 | 2 | 3 | 3 | 3,5 | 4 | 2,3 | B | 0 | 0 % |
| 82= | T29 | Médecin hospitalier (chef de clinique à médecin adjoint) × salarié (hôpital) × Suisse (résident) | 3 | 2 | 2 | 3 | 4,0 | 5 | 3,4 | B | 0 | 0 % |
| 82= | T84 | Analyste SOC (niveaux 1 et 2) × salarié × France | 5 | 2 | 3 | 3 | 3,5 | 4 | 1,9 | B | 0 | 0 % |
| 82= | T79 | Opticien-lunetier × salarié × France | 4 | 4 | 3 | 3 | 2,8 | 4 | 1,4 | B | 0 | 0 % |
| 85= | T74 | Pilote de ligne × salarié × France | 4 | 3 | 3 | 3 | 2,8 | 3 | 3,3 | B | 0 | 0 % |
| 85= | T04 | Praticien hospitalier (spécialiste, grille commune à toutes les spécialités) × statut PH (public) × France | 3 | 2 | 2 | 3 | 4,0 | 5 | 3,1 | B | 0 | 0 % |
| 85= | T08 | Sage-femme hospitalière × fonctionnaire FPH × France | 3 | 2 | 3 | 3 | 4,0 | 5 | 2,0 | B | 0 | 0 % |
| 85= | T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | 3 | 2 | 3 | 3 | 4,0 | 5 | 2,0 | B | 0 | 0 % |
| 89= | T07 | Pharmacien titulaire d'officine × indépendant × France | 4 | 3 | 2 | 3 | 4,0 | 3 | 2,6 | B* | 0 | 0 % |
| 89= | T17 | Manipulateur en électroradiologie médicale (MERM) × fonctionnaire FPH × France | 3 | 3 | 3 | 3 | 2,8 | 5 | 1,7 | B* | 0 | 0 % |
| 91= | T24 | Infirmier en soins généraux hospitalier × salarié × Suisse (frontalier) | 2 | 2 | 3 | 3 | 3,5 | 5 | 2,9 | B* | 0 | 0 % |
| 91= | T54 | Mécanicien de locomotive (CFF) × salarié × Suisse (résident) | 4 | 3 | 3 | 3 | 2,2 | 4 | 2,1 | B* | 0 | 0 % |
| 91= | T49 | Électricien de montage (CFC) × salarié × Suisse (frontalier) | 2 | 4 | 4 | 3 | 2,7 | 3 | 2,5 | B* | 0 | 0 % |
| 94= | T53 | Conducteur de train × salarié (SNCF) × France | 4 | 3 | 3 | 3 | 2,2 | 4 | 1,9 | B* | 0 | 0 % |
| 94= | T47 | Électricien du bâtiment × salarié × France | 2 | 4 | 4 | 3 | 2,7 | 4 | 1,4 | B* | 0 | 0 % |
| 96= | T23 | Infirmier en soins généraux hospitalier × salarié × Suisse (résident) | 2 | 2 | 3 | 3 | 3,5 | 5 | 2,2 | C* | 0 | 0 % |
| 96= | T49r | Électricien de montage (CFC) × salarié × Suisse (résident) | 2 | 4 | 4 | 3 | 2,7 | 3 | 1,9 | C* | 0 | 0 % |
| 98= | T52 | Frigoriste (froid et climatisation) × salarié × France | 2 | 4 | 3 | 3 | 2,7 | 4 | 1,6 | C | 0 | 0 % |
| 98= | T12 | Infirmier en soins généraux (IDE) hospitalier × fonctionnaire FPH × France | 2 | 2 | 3 | 3 | 3,5 | 5 | 1,7 | C | 0 | 0 % |
| 98= | T73 | Agent immobilier × indépendant (mandataire) × France | 4 | 3 | 4 | 3 | 3,8 | 1 | 1,3 | C | 0 | 0 % |
| 101= | T44 | Technicien de maintenance industrielle × salarié × France | 2 | 3 | 3 | 3 | 3,3 | 4 | 1,5 | C | 0 | 0 % |
| 101= | T66 | Sous-officier de l'armée de Terre × militaire × France | 2 | 3 | 3 | 4 | 2,2 | 4 | 1,6 | C | 0 | 0 % |
| 101= | T48 | Électricien du bâtiment × artisan × France | 2 | 3 | 4 | 3 | 3,2 | 3 | 1,6 | C | 0 | 0 % |
| 101= | T51 | Plombier-chauffagiste × artisan × France | 2 | 3 | 4 | 3 | 3,2 | 3 | 1,6 | C | 0 | 0 % |
| 105 | T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France | 1 | 2 | 3 | 4 | 2,2 | 5 | 1,8 | C | 0 | 0 % |
| 106 | T58 | Gardien de la paix × fonctionnaire × France | 2 | 2 | 3 | 2 | 2,2 | 5 | 1,8 | C | 0 | 0 % |
| 107= | T75 | Vendeur en magasin (référence) × salarié × France | 3 | 3 | 3 | 2 | 2,2 | 3 | 1,1 | C | 0 | 0 % |
| 107= | T33 | Assistant en soins et santé communautaire (ASSC) × salarié × Suisse (frontalier) | 1 | 2 | 3 | 3 | 1,7 | 4 | 2,4 | C | 0 | 0 % |
| 107= | T21 | Aide-soignant hospitalier × fonctionnaire FPH × France | 1 | 2 | 3 | 3 | 1,7 | 5 | 1,4 | C | 0 | 0 % |
| 110= | T33r | Assistant en soins et santé communautaire (ASSC) × salarié × Suisse (résident) | 1 | 2 | 3 | 3 | 1,7 | 4 | 1,7 | C | 0 | 0 % |
| 110= | T55 | Conducteur routier poids lourd × salarié × France | 2 | 3 | 2 | 2 | 2,2 | 4 | 1,1 | C | 0 | 0 % |

Paliers : S 0, A 64, B 31, C 16. « 2= » : rang partagé (écart inférieur à 0,03). * : à moins de 0,1 d'une frontière.

### Classement 1, partie B : revenu net après impôt, en équivalent temps plein

| ID | Triplet | Cellule avant impôt, médiane / P80 | Impôt (médiane) | Médiane après impôt, k€ change / PPA | P80 après impôt, k€ change / PPA | Fiabilité | Source de la médiane |
|---|---|---|---|---|---|---|---|
| T15 | Orthophoniste × libéral × France | 22 / 36 kEUR | 5 % | 21 / 21 | 32 / 32 | non officielle | UNASA 2022 (S06) : 27 550 € moy. ; × 0,96 × 0,85 ; aucun chiffre de la DREES, dont le jeu de données 2026 ne couvre pas les orthophonistes (S136) ; FNO : chiffre d'affaires moyen 2022 de 51 266 € avant charges (S136) |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 99 / 112 kCHF | 22 % | 82 / 75 | 92 / 83 | non officielle | Paymetric Labs 2026 (S178) : médiane 124 000 CHF, quartiles 120 000 et 131 000, senior 162 000 ; Optima, senior : 125 000 à 168 000 ; × 0,80 |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 92 / 107 kCHF | 22 % | 77 / 70 | 88 / 80 | non officielle | ERI SalaryExpert (S178) : consultant en cybersécurité, médiane 114 716 CHF (proxy) ; × 0,80 |
| F03 | Ophtalmologue × libéral × France | 164 / 265 kEUR | 33 % | 110 / 110 | 163 / 163 | relayée | CARMF  revenu net d'activité indépendante moyen 201 000 € (2023  Quotidien du Médecin citant la CARMF (S174)) ; × 0 96 × 0 85 |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 90 / 104 kCHF | 22 % | 75 / 69 | 86 / 78 | non officielle | ERI SalaryExpert, décembre 2025 (S178) : moyenne 114 262 CHF, 80 331 en début, 141 304 après 8 ans ; × 0,80 |
| F13 | Psychiatre × libéral × France | 76 / 122 kEUR | 22 % | 59 / 59 | 86 / 86 | relayée | CARMF  revenu net d'activité indépendante moyen 92 500 € (2023  Quotidien du Médecin citant la CARMF (S174)) ; × 0 96 × 0 85 |
| F06 | Cancérologue (oncologie médicale et radiothérapie) × libéral × France | 299 / 483 kEUR | 40 % | 180 / 180 | 272 / 272 | relayée | CARMF  revenu net d'activité indépendante moyen 366 200 € (2023  Quotidien du Médecin citant la CARMF  environ 700 médecins (S174)) ; × 0 96 × 0 85 |
| F09 | Cardiologue × libéral × France | 139 / 225 kEUR | 31 % | 96 / 96 | 143 / 143 | relayée (2024, site secondaire) | CARMF  revenu net d'activité indépendante moyen 170 766 € (2024  cabinet d'expertise comptable citant la CARMF (S175)) ; × 0 96 × 0 85 |
| C02 | Pédiatre × indépendant × Suisse (résident) | 167 / 268 kCHF | 21 % | 140 / 88 | 216 / 135 | relayée, groupe | OFS 2019 (S176) : groupe premier recours (médecine interne générale et pédiatrie)  médiane 172 000 CHF nets d'AVS et de 2e pilier ; moins la prime LAMal |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | 167 / 268 kCHF | 21 % | 140 / 88 | 216 / 135 | relayée | OFS 2019 (S24, S108) : premier recours, médiane 172 000 CHF nets d'AVS et de 2e pilier (relayée par la presse) ; moins la prime LAMal |
| F16 | Ingénieur sécurité cloud × salarié × France | 62 / 70 kEUR | 17 % | 52 / 52 | 57 / 57 | non officielle | site de formation (S177) : 70 à 90 k€ brut pour un profil confirmé ; milieu × 0,78 ; APEC, famille sécurité informatique : 64 k€ (recoupement) |
| C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | 99 / 112 kCHF | 22 % | 82 / 52 | 92 / 57 | non officielle | Paymetric Labs 2026 (S178) : médiane 124 000 CHF, quartiles 120 000 et 131 000, senior 162 000 ; Optima, senior : 125 000 à 168 000 ; × 0,80 |
| C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | 92 / 107 kCHF | 22 % | 77 / 48 | 88 / 55 | non officielle | ERI SalaryExpert (S178) : consultant en cybersécurité, médiane 114 716 CHF (proxy) ; × 0,80 |
| C03 | Ophtalmologue × indépendant × Suisse (résident) | 261 / 417 kCHF | 25 % | 210 / 131 | 327 / 204 | relayée, groupe | OFS 2019 (S176) : groupe à activité chirurgicale (ophtalmologie  ORL  chirurgie)  médiane 266 000 CHF nets d'AVS et de 2e pilier ; moins la prime LAMal |
| C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | 90 / 104 kCHF | 22 % | 75 / 47 | 86 / 54 | non officielle | ERI SalaryExpert, décembre 2025 (S178) : moyenne 114 262 CHF, 80 331 en début, 141 304 après 8 ans ; × 0,80 |
| T09 | Sage-femme × libéral × France | 34 / 56 kEUR | 11 % | 30 / 30 | 45 / 45 | officielle | DREES 2021 (S03) : sages-femmes libérales, 42 200 € moy. ; × 0,96 × 0,85 |
| T46 | Actuaire × salarié × France | 52 / 66 kEUR | 15 % | 44 / 44 | 54 / 54 | non re-sourcée | non re-sourcé, valeur v3 : estime : enquete de l'Institut des actuaires non recuperee |
| F07 | Médecin nucléaire × libéral × France | 189 / 305 kEUR | 35 % | 124 / 124 | 183 / 183 | relayée | CARMF  revenu net d'activité indépendante moyen 231 400 € (2023  Quotidien du Médecin citant la CARMF (S174)) ; × 0 96 × 0 85 |
| F17 | Consultant GRC (gouvernance, risques et conformité) × salarié × France | 50 / 63 kEUR | 14 % | 43 / 43 | 52 / 52 | relayée, proxy | APEC 2025 (S17, S103) : famille « sécurité informatique », médiane 60 k€ + 4 k€ de variable, brut (proxy) ; × 0,78 |
| F19 | Notaire × libéral × France | 184 / 297 kEUR | 34 % | 121 / 121 | 179 / 179 | relayée (site secondaire) | UNASA 2024 relayée (S182) : revenu moyen estimé 224 976 € ; × 0,96 × 0,85 ; médiane relayée de 197 500 € « brut » (définition non précisée) ; activité en baisse de 10 % en 2023 et de 4 % en 2024 |
| F10 | Dermatologue × libéral × France | 87 / 141 kEUR | 24 % | 66 / 66 | 97 / 97 | relayée (2024, site secondaire) | CARMF  revenu net d'activité indépendante moyen 107 139 € (2024  site spécialisé citant la CARMF (S175)) ; × 0 96 × 0 85 |
| T37 | Développeur logiciel × salarié × Suisse (frontalier) | 91 / 108 kCHF | 22 % | 76 / 70 | 89 / 81 | relayée | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois ; × 12 × 0,80 |
| T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | 91 / 106 kCHF | 22 % | 76 / 70 | 87 / 79 | relayée, proxy | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre au cloud) ; × 12 × 0,80 |
| T16 | Orthoptiste × salarié × France | 31 / 36 kEUR | 6 % | 29 / 29 | 33 / 33 | non re-sourcée | non re-sourcé, valeur v3 : estime : aucune serie officielle recuperee |
| F12 | Rhumatologue × libéral × France | 78 / 126 kEUR | 22 % | 60 / 60 | 88 / 88 | relayée | CARMF  revenu net d'activité indépendante moyen 95 200 € (2023  Quotidien du Médecin citant la CARMF (S174)) ; × 0 96 × 0 85 |
| F02 | Radiologue × libéral × France | 157 / 254 kEUR | 32 % | 106 / 106 | 158 / 158 | relayée | CARMF  revenu net d'activité indépendante moyen 192 625 € (2023  Docteur Imago citant la CARMF (S174)) ; × 0 96 × 0 85 |
| F15 | Pentesteur (auditeur en tests d'intrusion) × salarié × France | 43 / 51 kEUR | 12 % | 38 / 38 | 43 / 43 | non officielle | baromètre Silkhom 2026 relayé (S177) : 50 à 60 k€ brut fixe de 3 à 7 ans, 60 à 70 k€ au-delà ; milieu de fourchette × 0,78 |
| F05 | Anatomopathologiste × libéral × France | 156 / 251 kEUR | 32 % | 105 / 105 | 156 / 156 | relayée | CARMF  revenu net d'activité indépendante moyen 190 600 € (2023  Quotidien du Médecin citant la CARMF (S174)) ; × 0 96 × 0 85 |
| T85 | Data engineer (ingénieur des données) × salarié × France | 42 / 51 kEUR | 12 % | 37 / 37 | 43 / 43 | relayée, proxy | APEC 2025 (S17, S103) : famille « business intelligence », médiane 50 k€ + 4 k€ de variable, brut (proxy) ; × 0,78 |
| C01 | Psychiatre × indépendant × Suisse (résident) | 103 / 166 kCHF | 18 % | 90 / 56 | 140 / 87 | relayée, groupe | OFS 2019 (S176) : groupe psychiatrie  médiane 108 000 CHF nets d'AVS et de 2e pilier ; moins la prime LAMal |
| C19 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × Suisse (frontalier) | 160 / 200 kCHF | 28 % | 123 / 112 | 151 / 137 | non officielle | cabinets de recrutement (S178) : CISO 185 000 à 320 000 CHF (Optima 2026), responsable de la sécurité de l'information 190 000 à 250 000 CHF ; estimé 200 000 ; × 0,80 |
| F01 | Médecin généraliste × libéral × France | 73 / 118 kEUR | 22 % | 57 / 57 | 83 / 83 | relayée | CARMF  revenu net d'activité indépendante moyen 89 238 € (2023  Quotidien du Médecin citant la CARMF (S174)) ; × 0 96 × 0 85 |
| T91 | Médecin-dentiste × indépendant × Suisse (résident) | 136 / 219 kCHF | 20 % | 117 / 73 | 179 / 112 | relayée | OFS, ESPA 2014-2017, exploitée par la ZHAW pour la FMH (S111) : dentistes de plus de 34 ans, revenu annuel médian 166 000 CHF brut standardisé, tous statuts (indépendants : 84 CHF/h, salariés : 68 CHF/h) ; × 0,85 (AVS et prévoyance des indépendants, estimé) moins la prime LAMal ; aucune statistique de la SSO |
| F14 | Pédiatre × libéral × France | 70 / 114 kEUR | 22 % | 55 / 55 | 81 / 81 | relayée (année non confirmée) | CARMF  revenu net d'activité indépendante moyen 86 200 € (Quotidien du Médecin citant la CARMF  année non confirmée (S174)) ; × 0 96 × 0 85 |
| T35 | Développeur logiciel (études et développement) × salarié × France | 37 / 47 kEUR | 10 % | 34 / 34 | 41 / 41 | relayée | DARES, portraits statistiques des métiers, données ouvertes (S133) : ingénieurs de l'informatique (M2Z), salaire médian 3 120 € par mois en 2017-2019, net probable (non actualisé) |
| T05 | Chirurgien-dentiste omnipraticien × libéral × France | 94 / 152 kEUR | 26 % | 70 / 70 | 103 / 103 | relayée | CARCDSF 2023 (S04) : médiane 97 672 € ; × 0,96 ; recoupement Insee (S99) : dentistes 10 300 €/mois moy. |
| F08 | Gastro-entérologue × libéral × France | 128 / 207 kEUR | 30 % | 90 / 90 | 133 / 133 | relayée (site secondaire) | CARMF  revenu net d'activité indépendante moyen 157 239 € (2023  site spécialisé citant la CARMF (S175)) ; × 0 96 × 0 85 |
| T10 | Masseur-kinésithérapeute × libéral × France | 42 / 67 kEUR | 15 % | 36 / 36 | 53 / 53 | officielle | DREES 2021 (S03) : masseurs-kinésithérapeutes libéraux, 51 100 € moy. ; × 0,96 × 0,85 |
| T71 | Magistrat de l'ordre judiciaire × fonctionnaire × France | 61 / 73 kEUR | 17 % | 51 / 51 | 60 / 60 | relayée | ministère de la Justice (S126, relayé) : 5 083 €/mois net moyen après six ans d'exercice, primes comprises (3 884 € au début, 8 480 € en fin de carrière) |
| T37r | Développeur logiciel × salarié × Suisse (résident) | 91 / 108 kCHF | 22 % | 76 / 48 | 89 / 55 | relayée | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois ; × 12 × 0,80 |
| T86 | Ingénieur cloud DevOps × salarié × Suisse (résident) | 91 / 106 kCHF | 22 % | 76 / 48 | 87 / 54 | relayée, proxy | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre au cloud) ; × 12 × 0,80 |
| T41 | Ingénieur méthodes et industrialisation × salarié × France | 52 / 65 kEUR | 15 % | 45 / 45 | 54 / 54 | relayée, proxy | IESF 2025 (S16) : médiane 67 000 € brut, tous ingénieurs (proxy) ; × 0,78 |
| C22 | Enseignant du secondaire I (cycle d'orientation), Genève × fonctionnaire cantonal × Suisse (résident) | 87 / 97 kCHF | 21 % | 73 / 46 | 81 / 51 | non officielle | agrégateur de salaires (S180) : 102 000 à 115 000 CHF brut en milieu de carrière, 90 000 à 100 000 au début ; milieu × 0,80 ; grille officielle du canton non lue |
| C18 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × Suisse (résident) | 160 / 200 kCHF | 28 % | 123 / 77 | 151 / 94 | non officielle | cabinets de recrutement (S178) : CISO 185 000 à 320 000 CHF (Optima 2026), responsable de la sécurité de l'information 190 000 à 250 000 CHF ; estimé 200 000 ; × 0,80 |
| T81 | Ingénieur cloud DevOps × indépendant (freelance) × France | 69 / 90 kEUR | 21 % | 54 / 54 | 68 / 68 | non officielle | non officielle : TJM Free-Work et Morgan Philips (S74, S75) 650 € × 180 jours × 0,59 ; Insee 2024 (S106) : 4 190 €/mois moy., champ plus large |
| T76 | Pédicure-podologue × libéral × France | 33 / 45 kEUR | 11 % | 30 / 30 | 38 / 38 | non re-sourcée | non re-sourcé, valeur v3 : sources en conflit : ONPP 2014, 25 012 EUR moy. ; UNASA 2024 via JDN, 43 500 EUR brut (S137) |
| T80 | Ingénieur cloud DevOps × salarié × France | 43 / 53 kEUR | 12 % | 38 / 38 | 45 / 45 | relayée, proxy | APEC 2025 (S17, S103) : famille « systèmes, réseaux et télécoms », médiane 51 k€ + 4 k€ de variable, brut (proxy) ; × 0,78 |
| T42 | Ingénieur méthodes et industrialisation × salarié × Suisse (frontalier) | 86 / 106 kCHF | 21 % | 73 / 66 | 87 / 80 | relayée, proxy | OFS, ESS 2022 (S28) : diplômés HES, médiane 9 000 CHF/mois (proxy) ; × 12 × 0,80 |
| T77 | Ergothérapeute hospitalier × fonctionnaire FPH × France | 30 / 34 kEUR | 6 % | 28 / 28 | 31 / 31 | officielle (grille) | grille officielle FPH (S65) : IM 395 à 727 + CTI 183 € net/mois ; calcul à 10 ans d'exercice |
| T68 | Expert-comptable × libéral × France | 73 / 119 kEUR | 22 % | 57 / 57 | 84 / 84 | relayée, proxy | Insee 2024 (S106) : activités juridiques et comptables, 8 240 €/mois moy. (proxy) ; × 0,874 × 0,85 ; UNASA 2024 (S20) : 87 024 € moy. |
| T02 | Médecin généraliste × salarié (centre de santé) × France | 57 / 67 kEUR | 16 % | 48 / 48 | 55 / 55 | non officielle | non officielle : 60 000 à 85 000 € brut par an en centre de santé (S129) ; milieu de fourchette × 0,78 |
| F18 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × France | 70 / 86 kEUR | 18 % | 57 / 57 | 69 / 69 | non officielle | Robert Half 2026 relayé (S177) : médiane 90 k€ brut, 25e centile 80 k€, 75e centile 110 k€ ; × 0,78 |
| T56 | Professeur des écoles × fonctionnaire × France | 35 / 42 kEUR | 9 % | 32 / 32 | 37 / 37 | officielle | DEPP 2024 (S101) : professeurs des écoles à temps complet, 2 950 €/mois net moyen ; moyenne = médiane (grille) |
| T20 | Psychologue hospitalier × contractuel FPH × France | 30 / 35 kEUR | 6 % | 28 / 28 | 32 / 32 | non re-sourcée | non re-sourcé, valeur v3 : estime : grille psychologues FPH ; aucune serie recuperee |
| T62 | Contrôleur des finances publiques × fonctionnaire × France | 33 / 39 kEUR | 7 % | 30 / 30 | 35 / 35 | officielle, proxy | Insee et DGAFP 2023 (S67) : catégorie B, 2 720 €/mois net moyen (proxy) ; DGFiP : 2 120 € net à la titularisation |
| T60 | Attaché d'administration de l'État × fonctionnaire × France | 40 / 49 kEUR | 11 % | 36 / 36 | 42 / 42 | officielle, proxy | Insee et DGAFP 2023 (S67) : fonctionnaires de catégorie A, 3 373 €/mois net moyen (enseignants compris, proxy) |
| T61 | Inspecteur des finances publiques × fonctionnaire × France | 40 / 49 kEUR | 11 % | 36 / 36 | 42 / 42 | officielle, proxy | Insee et DGAFP 2023 (S67) : catégorie A, 3 373 €/mois net moyen (proxy) ; DGFiP (S120) : 2 378 € net à la titularisation |
| T42r | Ingénieur méthodes et industrialisation × salarié × Suisse (résident) | 86 / 106 kCHF | 21 % | 73 / 46 | 87 / 55 | relayée, proxy | OFS, ESS 2022 (S28) : diplômés HES, médiane 9 000 CHF/mois (proxy) ; × 12 × 0,80 |
| C21 | Administrateur de programme (P-3), Nations unies, Genève × fonctionnaire international × Suisse (frontalier) | 106 / 125 kCHF | 0 % | 114 / 104 | 134 / 122 | relayée, estimée | barème CFPI relayé (S181) : P-3 échelon 6 estimé à 78 760 USD net de contribution du personnel, × 1,84 (ajustement de poste de 84 %), moins pension 7,9 % et assurance maladie (estimées) ; converti au change 2025 |
| T78 | Diététicien × libéral × France | 24 / 32 kEUR | 5 % | 23 / 23 | 29 / 29 | non re-sourcée | non re-sourcé, valeur v3 : estime : aucune serie recuperee |
| T34 | Physiothérapeute × salarié × Suisse (frontalier) | 72 / 80 kCHF | 18 % | 63 / 57 | 68 / 62 | officielle, proxy | OFS, ESS 2024 (S22) : niveau de compétence 3, médiane 7 523 CHF/mois (proxy) ; × 12 × 0,80 |
| F04 | Anesthésiste-réanimateur × libéral × France | 171 / 277 kEUR | 33 % | 114 / 114 | 169 / 169 | relayée | CARMF  revenu net d'activité indépendante moyen 209 906 € (2023  Quotidien du Médecin et What's up Doc citant la CARMF (S174)) ; × 0 96 × 0 85 |
| T36 | Développeur logiciel × indépendant (freelance) × France | 58 / 76 kEUR | 19 % | 47 / 47 | 59 / 59 | non officielle | non officielle : TJM Malt (S19) 576 € × 170 jours × 0,59 ; Insee 2024 (S106), information et communication : 4 190 €/mois moy., champ plus large |
| T57 | Professeur certifié (collège et lycée) × fonctionnaire × France | 39 / 46 kEUR | 10 % | 35 / 35 | 40 / 40 | officielle | DEPP 2024 (S101) : professeurs certifiés à temps complet, 3 220 €/mois net moyen ; moyenne = médiane (grille) |
| C20 | Administrateur de programme (P-3), Nations unies, Genève × fonctionnaire international × Suisse (résident) | 106 / 125 kCHF | 0 % | 114 / 71 | 134 / 84 | relayée, estimée | barème CFPI relayé (S181) : P-3 échelon 6 estimé à 78 760 USD net de contribution du personnel, × 1,84 (ajustement de poste de 84 %), moins pension 7,9 % et assurance maladie (estimées) ; converti au change 2025 |
| T34r | Physiothérapeute × salarié × Suisse (résident) | 72 / 80 kCHF | 18 % | 63 / 39 | 68 / 43 | officielle, proxy | OFS, ESS 2024 (S22) : niveau de compétence 3, médiane 7 523 CHF/mois (proxy) ; × 12 × 0,80 |
| T63 | Contrôleur aérien (ICNA) × fonctionnaire × France | 94 / 113 kEUR | 21 % | 74 / 74 | 86 / 86 | officielle | Cour des comptes 2026 (S124) : environ 110 000 € brut annuel moyen, dont 61 % de primes ; net calculé (pension sur le traitement, CSG et CRDS) |
| T18 | Audioprothésiste × salarié × France | 36 / 45 kEUR | 9 % | 33 / 33 | 39 / 39 | non re-sourcée | non re-sourcé, valeur v3 : S21 (APEC : offres 36 600 EUR brut moy. ; confirme 2 300-3 100 EUR net/mois) |
| F11 | Gynécologue-obstétricien × libéral × France | 80 / 130 kEUR | 23 % | 62 / 62 | 90 / 90 | relayée (année incertaine) | CARMF  revenu net d'activité indépendante moyen 98 390 € (tableau de la CARMF relayé  année incertaine (2022 ou 2023  S175)) ; × 0 96 × 0 85 |
| T11 | Masseur-kinésithérapeute hospitalier × fonctionnaire FPH × France | 31 / 37 kEUR | 6 % | 29 / 29 | 33 / 33 | officielle, proxy | DGAFP 2025 (S128) : FPH, personnels des services de soins, 2 565 €/mois net moyen en 2023 (proxy) |
| T22 | Ostéopathe × libéral × France | 20 / 33 kEUR | 3 % | 20 / 20 | 29 / 29 | non officielle | Registre des ostéopathes de France, rapport 2026 (S135) : revenu mensuel moyen 1 987 € en 2024, définition non précisée ; × 0,85 |
| T72 | Attaché commercial B2B × salarié × France | 38 / 55 kEUR | 10 % | 35 / 35 | 46 / 46 | non re-sourcée | non re-sourcé, valeur v3 : S08 (PI et cadres) ; estime 3 200 EUR/mois variable inclus |
| T13 | Infirmier en soins généraux (IDE) × libéral × France | 47 / 75 kEUR | 17 % | 39 / 39 | 59 / 59 | officielle | DREES 2021 (S03) : infirmiers libéraux, 57 100 € moy. ; × 0,96 × 0,85 |
| T69 | Comptable × salarié × France | 29 / 34 kEUR | 5 % | 27 / 27 | 31 / 31 | non re-sourcée | non re-sourcé, valeur v3 : S08 (PI) ; estime 2 400 EUR/mois |
| T67 | Avocat × libéral × France | 54 / 122 kEUR | 19 % | 44 / 44 | 86 / 86 | relayée | CNBF, rapport 2024 (S107) : médianes nettes 65 378 € (hommes) et 49 491 € (femmes), pondérées 43/57 (part des femmes estimée) ; × 0,96 |
| C11 | Analyste SOC (niveaux 1 et 2) × salarié × Suisse (frontalier) | 78 / 101 kCHF | 20 % | 67 / 61 | 84 / 76 | non officielle | sites de salaires (S178) : environ 97 000 CHF brut en 2025 ; Glassdoor, SOC Analyst I : médiane 90 000, quartiles 71 804 et 109 229 CHF ; Optima 2026, SOC senior : 88 000 à 118 000 CHF ; × 0,80 |
| T06 | Pharmacien adjoint d'officine × salarié × France | 38 / 45 kEUR | 10 % | 34 / 34 | 39 / 39 | officielle (grille) | convention collective de l'officine 2026 (S127) : point 5,278 €, coefficient 500 (mi-carrière, estimé), 151,67 h par mois ; minimum conventionnel × 0,78 ; salaires réels non trouvés |
| T19 | Vétérinaire praticien × libéral × France | 57 / 92 kEUR | 19 % | 46 / 46 | 69 / 69 | relayée | Insee 2024 (S01) : vétérinaires, 6 370 €/mois moy. ; × 0,874 × 0,85 |
| T45 | Technicien systèmes et réseaux × salarié × France | 34 / 42 kEUR | 8 % | 31 / 31 | 37 / 37 | non re-sourcée | non re-sourcé, valeur v3 : S08 (PI mediane 2 440 EUR, D9 3 680 EUR) ; estime 2 800 EUR/mois |
| T29f | Médecin hospitalier (chef de clinique à médecin adjoint) × salarié (hôpital) × Suisse (frontalier) | 164 / 212 kCHF | 28 % | 126 / 114 | 159 / 144 | officielle ancienne | BASS pour l'OFSP (S110) : revenu AVS médian des médecins salariés 197 100 CHF, 2014 ; × 0,83 |
| C10 | Analyste SOC (niveaux 1 et 2) × salarié × Suisse (résident) | 78 / 101 kCHF | 20 % | 67 / 42 | 84 / 52 | non officielle | sites de salaires (S178) : environ 97 000 CHF brut en 2025 ; Glassdoor, SOC Analyst I : médiane 90 000, quartiles 71 804 et 109 229 CHF ; Optima 2026, SOC senior : 88 000 à 118 000 CHF ; × 0,80 |
| T29 | Médecin hospitalier (chef de clinique à médecin adjoint) × salarié (hôpital) × Suisse (résident) | 164 / 212 kCHF | 28 % | 126 / 79 | 159 / 99 | officielle ancienne | BASS pour l'OFSP (S110) : revenu AVS médian des médecins salariés 197 100 CHF, 2014 ; × 0,83 |
| T84 | Analyste SOC (niveaux 1 et 2) × salarié × France | 37 / 43 kEUR | 10 % | 34 / 34 | 38 / 38 | relayée, proxy | APEC (S134, relayée) : offres d'emploi en cybersécurité, salaire moyen proposé 48 000 € brut (proxy pour le SOC) ; × 0,78 |
| T79 | Opticien-lunetier × salarié × France | 27 / 32 kEUR | 5 % | 26 / 26 | 30 / 30 | non re-sourcée | non re-sourcé, valeur v3 : S08 (PI mediane 2 440 EUR) ; estime 2 250 EUR/mois |
| T74 | Pilote de ligne × salarié × France | 93 / 121 kEUR | 21 % | 73 / 73 | 91 / 91 | non officielle | non officielle : sites spécialisés (S129), environ 118 700 € brut annuel moyen à Air France, toutes anciennetés ; × 0,78 |
| T04 | Praticien hospitalier (spécialiste, grille commune à toutes les spécialités) × statut PH (public) × France | 83 / 100 kEUR | 20 % | 67 / 67 | 78 / 78 | officielle, champ plus large | Insee FPH 2024 (S09) : personnels médicaux, 6 926 €/mois net moyen en EQTP ; moyenne = médiane (grille) |
| T08 | Sage-femme hospitalière × fonctionnaire FPH × France | 41 / 50 kEUR | 11 % | 37 / 37 | 43 / 43 | officielle | DREES 2022 (S10) : sages-femmes salariées des hôpitaux, 3 442 €/mois net moyen (3 487 € dans le tableau) ; moyenne = médiane (grille) |
| T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | 42 / 48 kEUR | 12 % | 37 / 37 | 41 / 41 | non re-sourcée | non re-sourcé, valeur v3 : estime : grille IADE FPH ; ancrage S09 |
| T07 | Pharmacien titulaire d'officine × indépendant × France | 57 / 92 kEUR | 19 % | 46 / 46 | 69 / 69 | relayée | Insee 2024 (S99) : pharmaciens non salariés, 6 390 €/mois moy. ; × 0,874 × 0,85 |
| T17 | Manipulateur en électroradiologie médicale (MERM) × fonctionnaire FPH × France | 33 / 40 kEUR | 7 % | 31 / 31 | 35 / 35 | officielle, proxy | DGAFP 2025 (S128) : FPH, filière médico-technique, 2 749 €/mois net moyen en 2023 (proxy) |
| T24 | Infirmier en soins généraux hospitalier × salarié × Suisse (frontalier) | 76 / 90 kCHF | 20 % | 66 / 60 | 75 / 69 | officielle ancienne | OFSP (S23) : médiane des infirmiers diplômés 7 400 CHF/mois à temps plein, 13e compris (2018) ; × 1,074 × 0,80 |
| T54 | Mécanicien de locomotive (CFF) × salarié × Suisse (résident) | 74 / 85 kCHF | 19 % | 64 / 40 | 72 / 45 | relayée (grille d'entreprise) | modèle de calcul des CFF 2026 (S121, relayé) : 5 726 à 8 190 CHF/mois à 100 %, 13 salaires ; mi-carrière estimée 7 100 CHF ; × 0,80 |
| T49 | Électricien de montage (CFC) × salarié × Suisse (frontalier) | 59 / 69 kCHF | 15 % | 54 / 49 | 61 / 56 | relayée, proxy | OFS, ESS 2022 (S28) : titulaires d'un CFC, médiane 6 190 CHF/mois (proxy) ; × 12 × 0,80 |
| T53 | Conducteur de train × salarié (SNCF) × France | 37 / 46 kEUR | 10 % | 34 / 34 | 40 / 40 | non re-sourcée | non re-sourcé, valeur v3 : aucune source officielle ; reperes non officiels : 4 214 EUR brut par mois variables compris en 2023 (S129) |
| T47 | Électricien du bâtiment × salarié × France | 26 / 31 kEUR | 5 % | 25 / 25 | 29 / 29 | non re-sourcée | non re-sourcé, valeur v3 : S08 (INSEE 2023 : ouvriers mediane 1 920 EUR/mois) ; estime ouvrier qualifie 2 200 EUR |
| T23 | Infirmier en soins généraux hospitalier × salarié × Suisse (résident) | 76 / 90 kCHF | 20 % | 66 / 41 | 75 / 47 | officielle ancienne | OFSP (S23) : médiane des infirmiers diplômés 7 400 CHF/mois à temps plein, 13e compris, estimation OFS 2018 ; × 1,074 (hausse de la médiane ESS 2018-2024) × 0,80 |
| T49r | Électricien de montage (CFC) × salarié × Suisse (résident) | 59 / 69 kCHF | 15 % | 54 / 34 | 61 / 38 | relayée, proxy | OFS, ESS 2022 (S28) : titulaires d'un CFC, médiane 6 190 CHF/mois (proxy) ; × 12 × 0,80 |
| T52 | Frigoriste (froid et climatisation) × salarié × France | 30 / 36 kEUR | 6 % | 28 / 28 | 33 / 33 | non re-sourcée | non re-sourcé, valeur v3 : S08 (ouvriers et PI) ; estime 2 500 EUR/mois |
| T12 | Infirmier en soins généraux (IDE) hospitalier × fonctionnaire FPH × France | 33 / 40 kEUR | 7 % | 31 / 31 | 35 / 35 | officielle | DREES 2022 (S10) : infirmiers, 2 755 €/mois net moyen en EQTP, toutes structures ; moyenne = médiane (grille) ; FPH 2024, tous agents : moyenne 2 896 €, médiane 2 474 € (S100) |
| T73 | Agent immobilier × indépendant (mandataire) × France | 22 / 36 kEUR | 4 % | 21 / 21 | 31 / 31 | relayée, proxy | Insee 2024 (S106) : activités immobilières, 2 480 €/mois moy. (proxy), 27 % de revenus nuls ou déficitaires ; × 0,874 × 0,85 |
| T44 | Technicien de maintenance industrielle × salarié × France | 29 / 34 kEUR | 5 % | 27 / 27 | 31 / 31 | non re-sourcée | non re-sourcé, valeur v3 : S08 (INSEE 2023 : professions intermediaires mediane 2 440 EUR/mois) ; estime 2 400 EUR |
| T66 | Sous-officier de l'armée de Terre × militaire × France | 32 / 38 kEUR | 6 % | 30 / 30 | 34 / 34 | officielle | ministère des Armées, EcoDef n° 266 (S125) : solde nette médiane des sous-officiers 2 637 €/mois en 2023, toutes armées hors gendarmerie |
| T48 | Électricien du bâtiment × artisan × France | 27 / 43 kEUR | 7 % | 25 / 25 | 37 / 37 | relayée, proxy | Insee 2024 (S01) : construction, non-salariés classiques, 3 050 €/mois moy. (proxy) ; × 0,864 × 0,85 |
| T51 | Plombier-chauffagiste × artisan × France | 27 / 43 kEUR | 7 % | 25 / 25 | 37 / 37 | relayée, proxy | Insee 2024 (S01) : construction, non-salariés classiques, 3 050 €/mois moy. (proxy) ; × 0,864 × 0,85 |
| T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France | 36 / 44 kEUR | 9 % | 33 / 33 | 38 / 38 | officielle, champ plus large | Insee 2023 (S102) : agents des SDIS, 3 030 €/mois net moyen en EQTP, sapeurs-pompiers et non-sapeurs-pompiers ; moyenne = médiane (grille) |
| T58 | Gardien de la paix × fonctionnaire × France | 34 / 41 kEUR | 8 % | 32 / 32 | 37 / 37 | relayée, proxy | catégorie B de la police, 2 870 €/mois net moyen (DGAFP 2025, relayé par un site tiers, proxy) ; grille 2026 : 2 162 à 3 917 € net/mois (S120) |
| T75 | Vendeur en magasin (référence) × salarié × France | 22 / 26 kEUR | 2 % | 21 / 21 | 25 / 25 | officielle | Insee 2023 (S08) : employés, médiane 1 800 €/mois net |
| T33 | Assistant en soins et santé communautaire (ASSC) × salarié × Suisse (frontalier) | 56 / 61 kCHF | 14 % | 52 / 47 | 56 / 51 | officielle, proxy | OFS, ESS 2024 (S22) : niveau de compétence 2, médiane 5 866 CHF/mois (proxy) ; × 12 × 0,80 |
| T21 | Aide-soignant hospitalier × fonctionnaire FPH × France | 26 / 31 kEUR | 4 % | 25 / 25 | 29 / 29 | officielle, champ plus large | DREES 2022 (S10) : aides-soignants et ASH, 2 184 €/mois net moyen ; moyenne = médiane (grille) |
| T33r | Assistant en soins et santé communautaire (ASSC) × salarié × Suisse (résident) | 56 / 61 kCHF | 14 % | 52 / 32 | 56 / 35 | officielle, proxy | OFS, ESS 2024 (S22) : niveau de compétence 2, médiane 5 866 CHF/mois (proxy) ; × 12 × 0,80 |
| T55 | Conducteur routier poids lourd × salarié × France | 22 / 26 kEUR | 2 % | 21 / 21 | 25 / 25 | officielle ancienne | SDES 2019 (S105) : ouvriers qualifiés du transport routier de marchandises, 1 830 €/mois net en EQTP (non actualisé) |

Lecture : « X / Y » = milliers d'euros au change 2025 sans ajustement, puis en parité de pouvoir d'achat au niveau des prix français ; le score utilise Y. Impôt = part de la cellule (nette de cotisations) prélevée par l'impôt sur le revenu. Bornes de l'échelle logarithmique du classement 1 : médiane 20 à 180 k€, P80 25 à 272 k€ PPA.

### Classement 1, partie C : provenance des notes hors revenu

Sur 666 notes : 12 sourcées (S), 311 mixtes (M, dont les 111 notes CA), 343 estimées (E). Codes d'ancrage : section 1.13 et 1,14.

| ID | Triplet | EP | IT | QT | ES | CA | PS |
|---|---|---|---|---|---|---|---|
| T15 | Orthophoniste × libéral × France | E | E | E | M (S2), tension S2 | M | M (P7) |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| F03 | Ophtalmologue × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| F13 | Psychiatre × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| F06 | Cancérologue (oncologie médicale et radiothérapie) × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| F09 | Cardiologue × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| C02 | Pédiatre × indépendant × Suisse (résident) | E | E | M (Q10, Q15) | E | M | M (P8) |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | E | E | M (Q10, Q15) | E | M | S (P8) |
| F16 | Ingénieur sécurité cloud × salarié × France | M (E1, E9) | E | M (Q19), tension Q19 | E | M | S (P2, P3, P4) |
| C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| C03 | Ophtalmologue × indépendant × Suisse (résident) | E | E | M (Q15) | E | M | E |
| C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| T09 | Sage-femme × libéral × France | E | E | E | M (S2), tension S2 | M | E |
| T46 | Actuaire × salarié × France | M (E1) | E | E | E | M | M (P2) |
| F07 | Médecin nucléaire × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| F17 | Consultant GRC (gouvernance, risques et conformité) × salarié × France | M (E1, E9) | E | M (Q19), tension Q19 | E | M | S (P2, P3, P4) |
| F19 | Notaire × libéral × France | E | E | E | E | M | E |
| F10 | Dermatologue × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| T37 | Développeur logiciel × salarié × Suisse (frontalier) | M (E1) | E | E | E | M | M (P12) |
| T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | M (E1) | E | E | E | M | M (P12) |
| T16 | Orthoptiste × salarié × France | E | E | E | M (S2), tension S2 | M | E |
| F12 | Rhumatologue × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| F02 | Radiologue × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| F15 | Pentesteur (auditeur en tests d'intrusion) × salarié × France | M (E1, E9) | E | M (Q19), tension Q19 | E | M | S (P2, P3, P4) |
| F05 | Anatomopathologiste × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| T85 | Data engineer (ingénieur des données) × salarié × France | M (E1, E9) | E | E | E | M | S (P2, P3) |
| C01 | Psychiatre × indépendant × Suisse (résident) | E | E | M (Q15) | E | M | E |
| C19 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × Suisse (frontalier) | M (E1) | E | M (Q19) | E | M | M (P4, P12) |
| F01 | Médecin généraliste × libéral × France | E | E | M (Q1, Q2, Q18) | E | M | M (P6) |
| T91 | Médecin-dentiste × indépendant × Suisse (résident) | M (E8) | E | M (Q12, Q16) | E | M | M (P11), tension P11 |
| F14 | Pédiatre × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| T35 | Développeur logiciel (études et développement) × salarié × France | M (E1, E9) | E | E | E | M | S (P2, P3) |
| T05 | Chirurgien-dentiste omnipraticien × libéral × France | M (E8) | E | M (Q17) | E | M | E |
| F08 | Gastro-entérologue × libéral × France | E | E | M (Q2, Q18) | E | M | M (P6) |
| T10 | Masseur-kinésithérapeute × libéral × France | E | E | M (Q9) | M (S2), tension S2 | M | E |
| T71 | Magistrat de l'ordre judiciaire × fonctionnaire × France | M (E1) | E | E | E | M | M (P1) |
| T37r | Développeur logiciel × salarié × Suisse (résident) | M (E1) | E | E | E | M | M (P12) |
| T86 | Ingénieur cloud DevOps × salarié × Suisse (résident) | M (E1) | E | E | E | M | M (P12) |
| T41 | Ingénieur méthodes et industrialisation × salarié × France | M (E1) | E | E | E | M | M (P2) |
| C22 | Enseignant du secondaire I (cycle d'orientation), Genève × fonctionnaire cantonal × Suisse (résident) | M (E7) | M (I3) | M (Q14) | M (S3), tension S3 | M | M (P1) |
| C18 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × Suisse (résident) | M (E1) | E | M (Q19) | E | M | M (P4, P12) |
| T81 | Ingénieur cloud DevOps × indépendant (freelance) × France | E | E | E | E | M | M (P3) |
| T76 | Pédicure-podologue × libéral × France | E | E | E | M (S2), tension S2 | M | E |
| T80 | Ingénieur cloud DevOps × salarié × France | M (E1, E9) | E | E | E | M | S (P2, P3) |
| T42 | Ingénieur méthodes et industrialisation × salarié × Suisse (frontalier) | M (E1) | E | E | E | M | E |
| T77 | Ergothérapeute hospitalier × fonctionnaire FPH × France | E | E | E | M (S2), tension S2 | M | M (P1) |
| T68 | Expert-comptable × libéral × France | E | E | E | E | M | E |
| T02 | Médecin généraliste × salarié (centre de santé) × France | E | E | M (Q2) | E | M | M (P2, P6) |
| F18 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × France | M (E1, E9) | E | M (Q19) | E | M | S (P2, P3, P4) |
| T56 | Professeur des écoles × fonctionnaire × France | M (E7) | M (I3) | M (Q14) | S (S3) | M | M (P1) |
| T20 | Psychologue hospitalier × contractuel FPH × France | E | E | E | E | M | E |
| T62 | Contrôleur des finances publiques × fonctionnaire × France | E | E | E | E | M | M (P1) |
| T60 | Attaché d'administration de l'État × fonctionnaire × France | M (E1) | E | E | E | M | M (P1) |
| T61 | Inspecteur des finances publiques × fonctionnaire × France | M (E1) | E | E | E | M | M (P1) |
| T42r | Ingénieur méthodes et industrialisation × salarié × Suisse (résident) | M (E1) | E | E | E | M | E |
| C21 | Administrateur de programme (P-3), Nations unies, Genève × fonctionnaire international × Suisse (frontalier) | M (E1) | E | E | E | M | E |
| T78 | Diététicien × libéral × France | E | E | E | M (S2), tension S2 | M | E |
| T34 | Physiothérapeute × salarié × Suisse (frontalier) | E | E | E | M (S2), tension S2 | M | E |
| F04 | Anesthésiste-réanimateur × libéral × France | E | E | M (Q3) | E | M | M (P6) |
| T36 | Développeur logiciel × indépendant (freelance) × France | E | E | E | E | M | M (P3), tension P3 |
| T57 | Professeur certifié (collège et lycée) × fonctionnaire × France | M (E7) | M (I3) | M (Q14) | S (S3) | M | M (P1) |
| C20 | Administrateur de programme (P-3), Nations unies, Genève × fonctionnaire international × Suisse (résident) | M (E1) | E | E | E | M | E |
| T34r | Physiothérapeute × salarié × Suisse (résident) | E | E | E | M (S2), tension S2 | M | E |
| T63 | Contrôleur aérien (ICNA) × fonctionnaire × France | M (E1) | E | E | E | M | M (P1) |
| T18 | Audioprothésiste × salarié × France | E | E | E | M (S2), tension S2 | M | E |
| F11 | Gynécologue-obstétricien × libéral × France | E | E | M (Q3) | E | M | M (P6) |
| T11 | Masseur-kinésithérapeute hospitalier × fonctionnaire FPH × France | E | E | E | M (S2), tension S2 | M | M (P1) |
| T22 | Ostéopathe × libéral × France | E | E | E | E | M | E |
| T72 | Attaché commercial B2B × salarié × France | E | E | E | E | M | E |
| T13 | Infirmier en soins généraux (IDE) × libéral × France | E | E | E | M (S2), tension S2 | M | E |
| T69 | Comptable × salarié × France | E | E | E | E | M | E |
| T67 | Avocat × libéral × France | E | E | E | E | M | E |
| C11 | Analyste SOC (niveaux 1 et 2) × salarié × Suisse (frontalier) | M (E1) | E | M (Q19) | E | M | M (P2, P4, P12) |
| T06 | Pharmacien adjoint d'officine × salarié × France | E | E | E | E | M | M (P2) |
| T19 | Vétérinaire praticien × libéral × France | E | E | E | E | M | E |
| T45 | Technicien systèmes et réseaux × salarié × France | E | E | E | E | M | M (P4) |
| T29f | Médecin hospitalier (chef de clinique à médecin adjoint) × salarié (hôpital) × Suisse (frontalier) | E | M (I2) | M (Q3, Q11) | E | M | E |
| C10 | Analyste SOC (niveaux 1 et 2) × salarié × Suisse (résident) | M (E1) | E | M (Q19) | E | M | M (P2, P4, P12) |
| T29 | Médecin hospitalier (chef de clinique à médecin adjoint) × salarié (hôpital) × Suisse (résident) | E | M (I2) | M (Q3, Q11) | E | M | E |
| T84 | Analyste SOC (niveaux 1 et 2) × salarié × France | M (E1) | E | E | E | M | S (P2, P4) |
| T79 | Opticien-lunetier × salarié × France | E | E | E | M (S2) | M | E |
| T74 | Pilote de ligne × salarié × France | E | E | E | M (S4) | M | E |
| T04 | Praticien hospitalier (spécialiste, grille commune à toutes les spécialités) × statut PH (public) × France | E | M (I2) | M (Q3) | E | M | M (P1, P6) |
| T08 | Sage-femme hospitalière × fonctionnaire FPH × France | M (E6), tension E6 | M (I1) | M (Q4) | M (S2) | M | M (P1) |
| T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | M (E6), tension E6 | M (I1) | M (Q4) | M (S2) | M | M (P1) |
| T07 | Pharmacien titulaire d'officine × indépendant × France | E | E | E | E | M | E |
| T17 | Manipulateur en électroradiologie médicale (MERM) × fonctionnaire FPH × France | E | E | E | M (S2) | M | M (P1) |
| T24 | Infirmier en soins généraux hospitalier × salarié × Suisse (frontalier) | M (E6) | M (I1) | M (Q4) | M (S2) | M | E |
| T54 | Mécanicien de locomotive (CFF) × salarié × Suisse (résident) | M (E5), tension E5 | E | E | M (S4) | M | E |
| T49 | Électricien de montage (CFC) × salarié × Suisse (frontalier) | M (E2, E3, E4) | E | E | E | M | E |
| T53 | Conducteur de train × salarié (SNCF) × France | M (E5), tension E5 | E | E | M (S4) | M | E |
| T47 | Électricien du bâtiment × salarié × France | M (E2, E4) | E | E | E | M | E |
| T23 | Infirmier en soins généraux hospitalier × salarié × Suisse (résident) | M (E6) | M (I1) | M (Q4) | M (S2) | M | E |
| T49r | Électricien de montage (CFC) × salarié × Suisse (résident) | M (E2, E3, E4) | E | E | E | M | E |
| T52 | Frigoriste (froid et climatisation) × salarié × France | M (E2, E4) | E | E | E | M | E |
| T12 | Infirmier en soins généraux (IDE) hospitalier × fonctionnaire FPH × France | M (E6) | M (I1) | M (Q4) | M (S2) | M | M (P1) |
| T73 | Agent immobilier × indépendant (mandataire) × France | E | E | E | E | M | E |
| T44 | Technicien de maintenance industrielle × salarié × France | E | E | E | E | M | E |
| T66 | Sous-officier de l'armée de Terre × militaire × France | E | E | M (Q6) | E | M | E |
| T48 | Électricien du bâtiment × artisan × France | M (E2, E4) | E | E | E | M | E |
| T51 | Plombier-chauffagiste × artisan × France | M (E2, E4) | E | E | E | M | E |
| T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France | E | E | M (Q6) | E | M | M (P1) |
| T58 | Gardien de la paix × fonctionnaire × France | E | E | M (Q6) | S (S1) | M | M (P1) |
| T75 | Vendeur en magasin (référence) × salarié × France | E | E | M (Q8), tension Q8 | E | M | E |
| T33 | Assistant en soins et santé communautaire (ASSC) × salarié × Suisse (frontalier) | M (E6) | E | M (Q5) | E | M | E |
| T21 | Aide-soignant hospitalier × fonctionnaire FPH × France | M (E6) | E | M (Q5) | E | M | M (P1) |
| T33r | Assistant en soins et santé communautaire (ASSC) × salarié × Suisse (résident) | M (E6) | E | M (Q5) | E | M | E |
| T55 | Conducteur routier poids lourd × salarié × France | M (E2, E5) | E | M (Q7) | M (S4) | M | E |

### Classement 1, partie D : rang dans chacune des 8 pondérations (30 premiers)

| ID | Triplet | Poids égaux | environnement physique ×2 | intensité du travail ×2 | qualité du temps de travail ×2 | environnement social ×2 | compétences et autonomie ×2 | perspectives et sécurité ×2 | revenu ×2 | Étendue |
|---|---|---|---|---|---|---|---|---|---|---|
| T15 | Orthophoniste × libéral × France | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 19 | 1 à 19 |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 5 | 2 à 12 |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 10 | 2 à 12 |
| F03 | Ophtalmologue × libéral × France | 2 | 11 | 2 | 11 | 2 | 2 | 2 | 2 | 2 à 11 |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 2 | 2 | 2 | 2 | 2 | 2 | 12 | 10 | 2 à 12 |
| F13 | Psychiatre × libéral × France | 2 | 2 | 2 | 14 | 2 | 2 | 2 | 10 | 2 à 14 |
| F06 | Cancérologue (oncologie médicale et radiothérapie) × libéral × France | 7 | 17 | 26 | 14 | 2 | 2 | 2 | 1 | 1 à 26 |
| F09 | Cardiologue × libéral × France | 7 | 17 | 8 | 14 | 8 | 8 | 2 | 3 | 2 à 17 |
| C02 | Pédiatre × indépendant × Suisse (résident) | 9 | 24 | 8 | 20 | 8 | 8 | 6 | 5 | 5 à 24 |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | 9 | 24 | 8 | 20 | 8 | 8 | 6 | 5 | 5 à 24 |
| F16 | Ingénieur sécurité cloud × salarié × France | 9 | 6 | 12 | 5 | 11 | 12 | 25 | 19 | 5 à 25 |
| C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | 9 | 6 | 12 | 5 | 11 | 12 | 25 | 19 | 5 à 25 |
| C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | 13 | 6 | 12 | 5 | 11 | 12 | 25 | 26 | 5 à 26 |
| C03 | Ophtalmologue × indépendant × Suisse (résident) | 13 | 27 | 12 | 44 | 11 | 12 | 8 | 3 | 3 à 44 |
| C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | 13 | 6 | 12 | 5 | 11 | 12 | 25 | 26 | 5 à 26 |
| T09 | Sage-femme × libéral × France | 13 | 27 | 12 | 5 | 11 | 8 | 8 | 34 | 5 à 34 |
| T46 | Actuaire × salarié × France | 13 | 6 | 12 | 5 | 11 | 12 | 31 | 26 | 5 à 31 |
| F07 | Médecin nucléaire × libéral × France | 13 | 40 | 19 | 23 | 18 | 19 | 8 | 5 | 5 à 40 |
| F17 | Consultant GRC (gouvernance, risques et conformité) × salarié × France | 13 | 11 | 19 | 11 | 18 | 19 | 31 | 32 | 11 à 32 |
| F19 | Notaire × libéral × France | 13 | 11 | 19 | 23 | 38 | 19 | 31 | 5 | 5 à 38 |
| F10 | Dermatologue × libéral × France | 21 | 33 | 19 | 29 | 18 | 19 | 8 | 16 | 8 à 33 |
| T37 | Développeur logiciel × salarié × Suisse (frontalier) | 21 | 11 | 19 | 11 | 18 | 19 | 49 | 19 | 11 à 49 |
| T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | 21 | 11 | 19 | 29 | 18 | 19 | 35 | 19 | 11 à 35 |
| T16 | Orthoptiste × salarié × France | 21 | 11 | 2 | 29 | 18 | 37 | 12 | 45 | 2 à 45 |
| F12 | Rhumatologue × libéral × France | 21 | 33 | 26 | 29 | 24 | 27 | 12 | 19 | 12 à 33 |
| F02 | Radiologue × libéral × France | 21 | 48 | 26 | 29 | 24 | 27 | 12 | 10 | 10 à 48 |
| F15 | Pentesteur (auditeur en tests d'intrusion) × salarié × France | 21 | 17 | 26 | 14 | 24 | 27 | 35 | 39 | 14 à 39 |
| F05 | Anatomopathologiste × libéral × France | 21 | 48 | 26 | 29 | 24 | 27 | 12 | 10 | 10 à 48 |
| T85 | Data engineer (ingénieur des données) × salarié × France | 21 | 17 | 26 | 14 | 24 | 27 | 35 | 39 | 14 à 39 |
| C01 | Psychiatre × indépendant × Suisse (résident) | 30 | 17 | 26 | 51 | 24 | 27 | 12 | 26 | 12 à 51 |

### Classement 1, partie E : robustesse aux notes et au revenu, 10 000 tirages

Variantes : A notes estimées, tirages indépendants (consigne) ; B notes estimées, EP et IT communs au groupe de postes ; C notes estimées et mixtes, CA à ± 0,5 ; D notes estimées comme en A et revenu à ± 20 % (cellule incertaine) ou ± 5 % ; E notes estimées, écart commun à toutes les occurrences d'un même poste (informatif). La variante E a été ajoutée après le premier calcul du classement 2, à titre informatif : un même poste transposé dans plusieurs pays porte la même note estimée, son écart doit donc être commun. La règle de désignation d'un 1er reste celle de la variante A (1.15).

| ID | Triplet | P(10 premiers) A | B | C | D | E | P(1er) A | B | D | E | Rang médian A [5e à 95e centile] | Notes tirées (A) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 49 % | 51 % | 35 % | 47 % | 53 % | 9,2 % | 14,6 % | 8,0 % | 11,1 % | 11 [1 à 40] | 2 |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 48 % | 50 % | 35 % | 45 % | 52 % | 7,8 % | 9,9 % | 6,6 % | 9,4 % | 11 [1 à 40] | 2 |
| F03 | Ophtalmologue × libéral × France | 47 % | 51 % | 43 % | 46 % | 48 % | 10,8 % | 13,5 % | 10,7 % | 11,8 % | 11 [1 à 44] | 3 |
| T15 | Orthophoniste × libéral × France | 44 % | 46 % | 36 % | 44 % | 43 % | 4,2 % | 10,1 % | 4,4 % | 4,2 % | 14 [2 à 35] | 3 |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 41 % | 45 % | 34 % | 43 % | 45 % | 5,6 % | 5,0 % | 6,3 % | 6,0 % | 12 [1 à 41] | 2 |
| F06 | Cancérologue (oncologie médicale et radiothérapie) × libéral × France | 39 % | 40 % | 38 % | 40 % | 40 % | 7,7 % | 6,5 % | 7,6 % | 7,9 % | 15 [1 à 47] | 3 |
| F09 | Cardiologue × libéral × France | 37 % | 37 % | 36 % | 39 % | 37 % | 6,6 % | 4,2 % | 7,3 % | 7,3 % | 16 [1 à 49] | 3 |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | 36 % | 36 % | 41 % | 37 % | 36 % | 5,6 % | 2,2 % | 5,9 % | 5,9 % | 17 [1 à 50] | 3 |
| C02 | Pédiatre × indépendant × Suisse (résident) | 36 % | 35 % | 33 % | 36 % | 36 % | 5,2 % | 2,3 % | 5,9 % | 5,8 % | 17 [1 à 51] | 3 |
| F16 | Ingénieur sécurité cloud × salarié × France | 30 % | 31 % | 20 % | 28 % | 29 % | 1,7 % | 2,1 % | 1,7 % | 0,0 % | 18 [2 à 48] | 2 |
| C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | 30 % | 30 % | 23 % | 29 % | 27 % | 1,5 % | 1,0 % | 1,5 % | 0,0 % | 18 [3 à 49] | 2 |
| F13 | Psychiatre × libéral × France | 30 % | 32 % | 32 % | 31 % | 30 % | 3,2 % | 3,2 % | 3,4 % | 3,0 % | 16 [2 à 47] | 3 |
| C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | 29 % | 29 % | 21 % | 27 % | 28 % | 1,5 % | 0,8 % | 1,2 % | 0,0 % | 19 [3 à 50] | 2 |
| F07 | Médecin nucléaire × libéral × France | 29 % | 26 % | 26 % | 28 % | 28 % | 4,0 % | 0,9 % | 3,6 % | 4,5 % | 21 [2 à 55] | 3 |
| C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | 28 % | 26 % | 19 % | 26 % | 25 % | 0,9 % | 0,6 % | 0,9 % | 0,0 % | 20 [3 à 51] | 2 |
| F10 | Dermatologue × libéral × France | 27 % | 24 % | 24 % | 25 % | 27 % | 3,5 % | 0,4 % | 3,0 % | 4,7 % | 23 [2 à 56] | 3 |
| C03 | Ophtalmologue × indépendant × Suisse (résident) | 25 % | 21 % | 27 % | 23 % | 24 % | 2,9 % | 0,7 % | 2,6 % | 0,0 % | 23 [2 à 62] | 4 |
| F19 | Notaire × libéral × France | 24 % | 24 % | 25 % | 23 % | 25 % | 4,2 % | 7,2 % | 3,7 % | 5,5 % | 25 [2 à 66] | 5 |
| F17 | Consultant GRC (gouvernance, risques et conformité) × salarié × France | 23 % | 22 % | 14 % | 23 % | 21 % | 0,7 % | 0,4 % | 0,6 % | 0,0 % | 22 [3 à 53] | 2 |
| T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | 21 % | 22 % | 23 % | 21 % | 23 % | 2,1 % | 2,1 % | 2,4 % | 2,2 % | 24 [3 à 57] | 3 |
| F12 | Rhumatologue × libéral × France | 19 % | 19 % | 22 % | 20 % | 20 % | 1,8 % | 0,1 % | 1,9 % | 2,1 % | 25 [3 à 59] | 3 |
| T46 | Actuaire × salarié × France | 19 % | 20 % | 18 % | 18 % | 19 % | 0,6 % | 2,3 % | 0,7 % | 1,1 % | 24 [4 à 54] | 3 |
| F02 | Radiologue × libéral × France | 19 % | 17 % | 21 % | 19 % | 20 % | 1,7 % | 0,0 % | 2,0 % | 1,8 % | 26 [3 à 59] | 3 |
| F05 | Anatomopathologiste × libéral × France | 18 % | 16 % | 21 % | 19 % | 19 % | 1,5 % | 0,0 % | 1,6 % | 1,5 % | 26 [3 à 59] | 3 |
| F14 | Pédiatre × libéral × France | 16 % | 12 % | 19 % | 18 % | 15 % | 1,1 % | 0,0 % | 1,4 % | 0,0 % | 29 [4 à 60] | 3 |
| F01 | Médecin généraliste × libéral × France | 16 % | 13 % | 19 % | 17 % | 15 % | 1,2 % | 0,0 % | 1,2 % | 0,0 % | 28 [4 à 60] | 3 |
| T09 | Sage-femme × libéral × France | 15 % | 16 % | 16 % | 15 % | 15 % | 0,4 % | 2,1 % | 0,5 % | 0,9 % | 31 [5 à 63] | 4 |
| F15 | Pentesteur (auditeur en tests d'intrusion) × salarié × France | 15 % | 14 % | 11 % | 17 % | 13 % | 0,1 % | 0,0 % | 0,2 % | 0,0 % | 26 [5 à 56] | 2 |
| F08 | Gastro-entérologue × libéral × France | 14 % | 10 % | 17 % | 14 % | 14 % | 0,8 % | 0,0 % | 0,9 % | 0,9 % | 31 [5 à 63] | 3 |
| T71 | Magistrat de l'ordre judiciaire × fonctionnaire × France | 14 % | 15 % | 9 % | 13 % | 14 % | 0,7 % | 1,7 % | 0,6 % | 0,7 % | 32 [5 à 64] | 3 |

Plus forte probabilité d'être 1er : A F03 (10,8 %) ; B C15 (14,6 %) ; C F03 (8,3 %) ; D F03 (10,7 %) ; E F03 (11,8 %). Aucune ne dépasse 50 % : pas de 1er désigné.

### Classement 1, partie F : égalités, frontières de palier, scénario IA fort, sensibilité aux tensions

Égalités déclarées (écart inférieur à 0,03 avec le premier du groupe) : rang 2 : C15, C17, F03, C13, F13 ; rang 7 : F06, F09 ; rang 9 : C02, T30, F16, C14 ; rang 13 : C16, C03, C12, T09, T46, F07, F17, F19 ; rang 21 : F10, T37, T82, T16, F12, F02, F15, F05, T85 ; rang 30 : C01, C19, F01, T91, F14, T35, T05 ; rang 37 : F08, T10, T71 ; rang 40 : T37r, T86, T41, C22, C18 ; rang 45 : T81, T76, T80, T42 ; rang 49 : T77, T68, T02, F18 ; rang 54 : T20, T62, T60, T61, T42r ; rang 59 : C21, T78, T34, F04.

À moins de 0,1 d'une frontière : 23 triplets ; dans les 30 premiers : T15 (A), C15 (A).

| ID | Triplet | Exposition IA | Palier | Palier, IA fort (informatif) | Rang | Rang, tensions résolues (informatif) |
|---|---|---|---|---|---|---|
| T15 | Orthophoniste × libéral × France | faible | A* | A | 1 | 4 |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | moyenne | A* | A | 2= | 12 |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | élevée | A | A | 2= | 12 |
| F03 | Ophtalmologue × libéral × France | faible | A | A | 2= | 1 |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | moyenne | A | A | 2= | 12 |
| F13 | Psychiatre × libéral × France | faible | A | A | 2= | 1 |
| F06 | Cancérologue (oncologie médicale et radiothérapie) × libéral × France | faible | A | A | 7= | 1 |
| F09 | Cardiologue × libéral × France | faible | A | A | 7= | 4 |
| C02 | Pédiatre × indépendant × Suisse (résident) | faible | A | A | 9= | 4 |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | faible | A | A | 9= | 4 |
| F16 | Ingénieur sécurité cloud × salarié × France | moyenne | A | A | 9= | 28 |
| C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | moyenne | A | A | 9= | 28 |
| C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | élevée | A | A | 13= | 32 |
| C03 | Ophtalmologue × indépendant × Suisse (résident) | faible | A | A | 13= | 8 |
| C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | moyenne | A | A | 13= | 32 |
| T09 | Sage-femme × libéral × France | faible | A | A | 13= | 32 |
| T46 | Actuaire × salarié × France | élevée | A | A | 13= | 8 |
| F07 | Médecin nucléaire × libéral × France | moyenne | A | A | 13= | 8 |
| F17 | Consultant GRC (gouvernance, risques et conformité) × salarié × France | élevée | A | A | 13= | 32 |
| F19 | Notaire × libéral × France | moyenne | A | A | 13= | 8 |
| F10 | Dermatologue × libéral × France | moyenne | A | A | 21= | 12 |
| T37 | Développeur logiciel × salarié × Suisse (frontalier) | élevée | A | A | 21= | 12 |
| T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | moyenne | A | A | 21= | 12 |
| T16 | Orthoptiste × salarié × France | moyenne | A | A | 21= | 40 |
| F12 | Rhumatologue × libéral × France | faible | A | A | 21= | 12 |
| F02 | Radiologue × libéral × France | moyenne | A | A | 21= | 12 |
| F15 | Pentesteur (auditeur en tests d'intrusion) × salarié × France | moyenne | A | A | 21= | 40 |
| F05 | Anatomopathologiste × libéral × France | moyenne | A | A | 21= | 12 |
| T85 | Data engineer (ingénieur des données) × salarié × France | élevée | A | A | 21= | 12 |
| C01 | Psychiatre × indépendant × Suisse (résident) | faible | A | A | 30= | 22 |

### Classement 1, partie G : modifications par rapport à la version 6 (triplets repris)

| ID | Poste | Rang v6 (93 triplets, 7 pays) | Rang v7 (classement 1) | RE v6 (avant impôt) | RE v7 (après impôt) | Palier v6 | Palier v7 | Notes hors revenu |
|---|---|---|---|---|---|---|---|---|
| T15 | Orthophoniste | 1 | 1 | 1,5 | 1,3 | S | A | identiques |
| T30 | Médecin de famille (médecine interne générale) | 1 | 9= | 5,0 | 3,8 | S | A | identiques |
| T09 | Sage-femme | 14 | 13= | 2,4 | 1,9 | A | A | identiques |
| T46 | Actuaire | 6 | 13= | 3,1 | 2,4 | A | A | identiques |
| T16 | Orthoptiste | 16 | 21= | 1,8 | 1,6 | A | A | identiques |
| T85 | Data engineer (ingénieur des données) | 16 | 21= | 2,5 | 2,0 | A | A | identiques |
| T37 | Développeur logiciel | 6 | 21= | 4,2 | 3,1 | A | A | identiques |
| T82 | Ingénieur cloud DevOps | 6 | 21= | 4,1 | 3,1 | A | A | identiques |
| T05 | Chirurgien-dentiste omnipraticien | 6 | 30= | 4,6 | 3,3 | A | A | identiques |
| T35 | Développeur logiciel (études et développement) | 21 | 30= | 2,3 | 1,9 | A | A | identiques |
| T91 | Médecin-dentiste | 6 | 30= | 4,5 | 3,4 | A | A | identiques |
| T10 | Masseur-kinésithérapeute | 21 | 37= | 2,8 | 2,2 | A | A | identiques |
| T71 | Magistrat de l'ordre judiciaire | 16 | 37= | 3,4 | 2,6 | A | A | identiques |
| T41 | Ingénieur méthodes et industrialisation | 25 | 40= | 3,1 | 2,4 | A | A | identiques |
| T86 | Ingénieur cloud DevOps | 21 | 40= | 3,3 | 2,5 | A | A | identiques |
| T76 | Pédicure-podologue | 29 | 45= | 2,1 | 1,7 | A | A | identiques |
| T80 | Ingénieur cloud DevOps | 29 | 45= | 2,6 | 2,1 | A | A | identiques |
| T81 | Ingénieur cloud DevOps | 21 | 45= | 3,7 | 2,8 | A | A | identiques |
| T42 | Ingénieur méthodes et industrialisation | 25 | 45= | 4,1 | 3,1 | A | A | identiques |
| T02 | Médecin généraliste | 29 | 49= | 3,2 | 2,5 | A | A | identiques |
| T77 | Ergothérapeute hospitalier | 33 | 49= | 1,7 | 1,5 | A | A | identiques |
| T68 | Expert-comptable | 25 | 49= | 4,1 | 3,0 | A | A | identiques |
| T56 | Professeur des écoles | 33 | 53 | 2,2 | 1,8 | A | A | identiques |
| T20 | Psychologue hospitalier | 40 | 54= | 1,8 | 1,5 | A | A | identiques |
| T60 | Attaché d'administration de l'État | 37 | 54= | 2,5 | 2,0 | A | A | identiques |
| T61 | Inspecteur des finances publiques | 37 | 54= | 2,5 | 2,0 | A | A | identiques |
| T62 | Contrôleur des finances publiques | 40 | 54= | 2,0 | 1,7 | A | A | modifiées |
| T78 | Diététicien | 44 | 59= | 1,4 | 1,3 | A | A | identiques |
| T34 | Physiothérapeute | 37 | 59= | 3,6 | 2,7 | A | A | identiques |
| T36 | Développeur logiciel | 40 | 63= | 3,3 | 2,5 | A | A | identiques |
| T57 | Professeur certifié (collège et lycée) | 44 | 63= | 2,4 | 1,9 | A | A | identiques |
| T63 | Contrôleur aérien (ICNA) | 40 | 65= | 4,3 | 3,2 | A | B | modifiées |
| T18 | Audioprothésiste | 48 | 68 | 2,2 | 1,9 | A | B | identiques |
| T11 | Masseur-kinésithérapeute hospitalier | 50 | 69= | 1,9 | 1,6 | B | B | identiques |
| T22 | Ostéopathe | 54 | 71 | 1,2 | 1,1 | B | B | identiques |
| T13 | Infirmier en soins généraux (IDE) | 52 | 72= | 3,1 | 2,3 | B | B | identiques |
| T67 | Avocat | 50 | 72= | 3,7 | 2,8 | B | B | identiques |
| T69 | Comptable | 56 | 72= | 1,7 | 1,5 | B | B | modifiées |
| T72 | Attaché commercial B2B | 54 | 72= | 2,5 | 2,0 | B | B | modifiées |
| T06 | Pharmacien adjoint d'officine | 58 | 76= | 2,3 | 1,9 | B | B | identiques |
| T19 | Vétérinaire praticien | 56 | 78= | 3,5 | 2,6 | B | B | identiques |
| T45 | Technicien systèmes et réseaux | 60 | 78= | 2,1 | 1,8 | B | B | modifiées |
| T79 | Opticien-lunetier | 64 | 82= | 1,6 | 1,4 | B | B | modifiées |
| T84 | Analyste SOC (niveaux 1 et 2) | 63 | 82= | 2,2 | 1,9 | B | B | identiques |
| T29 | Médecin hospitalier (chef de clinique à médecin adjoint) | 58 | 82= | 4,7 | 3,4 | B | B | identiques |
| T04 | Praticien hospitalier (spécialiste, grille commune à toutes les spécialités) | 61 | 85= | 4,0 | 3,1 | B | B | identiques |
| T08 | Sage-femme hospitalière | 64 | 85= | 2,5 | 2,0 | B | B | identiques |
| T14 | Infirmier anesthésiste (IADE) | 64 | 85= | 2,5 | 2,0 | B | B | identiques |
| T74 | Pilote de ligne | 61 | 85= | 4,4 | 3,3 | B | B | modifiées |
| T07 | Pharmacien titulaire d'officine | 64 | 89= | 3,5 | 2,6 | B | B | identiques |
| T17 | Manipulateur en électroradiologie médicale (MERM) | 72 | 89= | 2,0 | 1,7 | B | B | modifiées |
| T24 | Infirmier en soins généraux hospitalier | 69 | 91= | 3,8 | 2,9 | B | B | identiques |
| T49 | Électricien de montage (CFC) | 72 | 91= | 3,2 | 2,5 | B | B | modifiées |
| T54 | Mécanicien de locomotive (CFF) | 72 | 91= | 2,9 | 2,1 | B | B | modifiées |
| T47 | Électricien du bâtiment | 78 | 94= | 1,5 | 1,4 | B | B | modifiées |
| T53 | Conducteur de train | 76 | 94= | 2,3 | 1,9 | B | B | modifiées |
| T23 | Infirmier en soins généraux hospitalier | 76 | 96= | 2,9 | 2,2 | B | C | identiques |
| T12 | Infirmier en soins généraux (IDE) hospitalier | 80 | 98= | 2,0 | 1,7 | C | C | identiques |
| T52 | Frigoriste (froid et climatisation) | 80 | 98= | 1,8 | 1,6 | C | C | modifiées |
| T73 | Agent immobilier | 82 | 98= | 1,4 | 1,3 | C | C | modifiées |
| T44 | Technicien de maintenance industrielle | 85 | 101= | 1,7 | 1,5 | C | C | modifiées |
| T48 | Électricien du bâtiment | 85 | 101= | 1,9 | 1,6 | C | C | modifiées |
| T51 | Plombier-chauffagiste | 85 | 101= | 1,9 | 1,6 | C | C | modifiées |
| T66 | Sous-officier de l'armée de Terre | 82 | 101= | 1,9 | 1,6 | C | C | modifiées |
| T59 | Sapeur-pompier professionnel | 88 | 105 | 2,2 | 1,8 | C | C | modifiées |
| T58 | Gardien de la paix | 89 | 106 | 2,1 | 1,8 | C | C | modifiées |
| T21 | Aide-soignant hospitalier | 91 | 107= | 1,5 | 1,4 | C | C | modifiées |
| T75 | Vendeur en magasin (référence) | 91 | 107= | 1,1 | 1,1 | C | C | modifiées |
| T33 | Assistant en soins et santé communautaire (ASSC) | 90 | 107= | 3,0 | 2,4 | C | C | modifiées |
| T55 | Conducteur routier poids lourd | 93 | 110= | 1,1 | 1,1 | C | C | modifiées |

Causes déclarées : (1) revenu après impôt sur le revenu (1.15) ; (2) nouveau pool (postes précis, pays limités à la France et à la Suisse), donc nouvelles bornes de l'échelle de revenu ; (3) T01 devient F01 (source CARMF 2023 commune aux spécialités). Les notes hors revenu des triplets repris sont identiques à la v6 (contrôle automatique : 0 écart).

## 4. Classement 2 : les 10 pays retenus (341 triplets)

Lecture des colonnes : EP environnement physique, IT intensité du travail, QT qualité du temps de travail, ES environnement social, CA compétences et autonomie, PS perspectives et sécurité, RE revenu net après impôt ; notes de 1 (mauvais) à 5 (bon), poids égaux. CA et RE sont continues, les autres entières. Palier : S ≥ 4,2, A ≥ 3,6, B ≥ 3,0, C en dessous ; * = à moins de 0,1 d'une frontière. « 2= » : rang partagé (écart inférieur à 0,03). P(10 premiers) : part des 10 000 tirages de la variante A où le triplet est dans les 10 premiers.

### Classement 2, postes retenus et transposition

| Poste | Statut | Notes de base (classement 1) | Entrée | Pays |
|---|---|---|---|---|
| Orthophoniste | indépendant | T15 | 30 premiers | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Ingénieur sécurité cloud | salarié | C15 | 30 premiers | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |
| Consultant GRC (gouvernance, risques et conformité) | salarié | C17 | 30 premiers | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |
| Ophtalmologue | indépendant | F03 | 30 premiers | NL, CH, DE, LU, AT |
| Pentesteur (auditeur en tests d'intrusion) | salarié | C13 | 30 premiers | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |
| Psychiatre | indépendant | F13 | 30 premiers | NL, CH, DE, LU, AT |
| Cancérologue (oncologie médicale et radiothérapie) | indépendant | F06 | 30 premiers | NL, DE, LU, AT |
| Cardiologue | indépendant | F09 | 30 premiers | NL, DE, LU, AT |
| Pédiatre | indépendant | C02 | 30 premiers | NL, CH, DE, LU, AT |
| Médecin généraliste (médecin de famille) | indépendant | T30 | 30 premiers | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |
| Sage-femme | indépendant | T09 | 30 premiers | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Actuaire | salarié | T46 | 30 premiers | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Médecin nucléaire | indépendant | F07 | 30 premiers | NL, DE, LU, AT |
| Notaire | indépendant | F19 | 30 premiers | NL, DE, LU, AT, SI |
| Dermatologue | indépendant | F10 | 30 premiers | NL, DE, LU, AT |
| Développeur logiciel | salarié | T37 | 30 premiers | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |
| Ingénieur cloud DevOps | salarié | T82 | 30 premiers | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |
| Orthoptiste | salarié | T16 | 30 premiers | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Rhumatologue | indépendant | F12 | 30 premiers | NL, DE, LU, AT |
| Radiologue | indépendant | F02 | 30 premiers | NL, DE, LU, AT |
| Anatomopathologiste | indépendant | F05 | 30 premiers | NL, DE, LU, AT |
| Data engineer (ingénieur des données) | salarié | T85 | 30 premiers | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Responsable de la sécurité des systèmes d'information (RSSI) | salarié | C19 | 30 premiers | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |
| Chirurgien-dentiste omnipraticien | indépendant | T05 | 30 premiers | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |
| Médecin généraliste (médecin de famille) | salarié | T02 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Masseur-kinésithérapeute | indépendant | T10 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Psychologue hospitalier | salarié | T20 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Pédicure-podologue | indépendant | T76 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Ergothérapeute hospitalier | fonctionnaire | T77 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Diététicien | indépendant | T78 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Ingénieur cloud DevOps | indépendant (freelance) | T81 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Ingénieur méthodes et industrialisation | salarié | T41 | contrôle | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |
| Professeur des écoles | fonctionnaire | T56 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Attaché d'administration de l'État | fonctionnaire | T60 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Inspecteur des finances publiques | fonctionnaire | T61 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Contrôleur des finances publiques | fonctionnaire | T62 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Magistrat de l'ordre judiciaire | fonctionnaire | T71 | contrôle | NL, NO, DE, LU, IS, DK, GB, AT, SI |
| Enseignant du secondaire I (cycle d'orientation), Genève | fonctionnaire | C22 | contrôle | NL, CH, NO, DE, LU, IS, DK, GB, AT, SI |

38 postes, dont 14 ajoutés par le contrôle (score maximal possible supérieur ou égal au 10e score du classement 2) ; 341 triplets. Spécialistes hospitaliers (grille commune) en Norvège, Danemark, Royaume-Uni, Islande, Slovénie ; administrateur de l'UE à Luxembourg.

### Classement 2, revenus : données lues et règle de structure

| ID | Triplet | Brut médian | Fiabilité | Source |
|---|---|---|---|---|
| M103 | Développeur logiciel × salarié × Allemagne | 73 400 EUR | relayée | Bundesagentur für Arbeit (S33) : informatique, médiane 6 114 € brut par mois à temps plein |
| M062 | Médecin généraliste (médecin de famille) × indépendant × Allemagne | 218 000 EUR | relayée (par cabinet, site secondaire) | Destatis 2023 relayé (S188) : médecine générale, revenu net de cabinet (Reinertrag) médian 218 000 € par cabinet |
| M302 | Médecin spécialiste hospitalier (grille commune aux spécialités) × salarié (hôpital) × Danemark | 1 100 500 DKK | relayée | Danmarks Statistik 2024 relayé (S185) : overlæger, quartiles 87 932 et 118 110 DKK par mois, retraite comprise ; médiane log 101 900 ; × 0,90 (part patronale de retraite, estimée) |
| M108 | Développeur logiciel × salarié × Royaume-Uni | 56 900 GBP | relayée (site secondaire) | ONS, ASHE 2025 relayé (S187) : programmeurs et développeurs, médiane 56 914 £ à temps plein |
| M066 | Médecin généraliste (médecin de famille) × indépendant × Royaume-Uni | 119 200 GBP | relayée (moyenne, 2022/23) | NHS Digital 2022/23 relayé (S187) : généralistes associés (contractors), revenu moyen avant impôt 140 200 £ ; médiane = moyenne × 0,85 (règle 1.4) |
| M303 | Médecin spécialiste hospitalier (grille commune aux spécialités) × salarié (hôpital) × Royaume-Uni | 127 600 GBP | connue (grille) | NHS, barème des consultants 2025/26 (connu, hausse de 4 % confirmée, S187) : 109 725 à 145 478 £ ; milieu |
| M306 | Administrateur (AD), institutions de l'Union européenne × fonctionnaire européen × Luxembourg (résident) | 102 600 EUR | relayée (grille), impôt estimé | grille au 1er juillet 2025 (S119, relayée) : AD7 échelon 2 = 8 207,25 € + indemnité de dépaysement 16 %, moins pension 10,1 % et maladie 1,7 % (taux estimés) ; avant impôt de l'UE ; impôt de l'UE et prélèvement de solidarité : 18 % (estimé) |
| M101 | Développeur logiciel × salarié × Pays-Bas | 78 200 EUR | relayée (site secondaire) | CBS 2024 relayé (S186) : développeur de logiciels, médiane 6 032 € par mois à 40 h ; × 12 × 1,08 (pécule de vacances) |
| M102 | Développeur logiciel × salarié × Norvège | 929 000 NOK | relayée (site secondaire) | SSB 2025 relayé (S184) : développeurs de logiciels, médiane 77 420 NOK par mois (moyenne 81 050) |
| M301 | Médecin spécialiste hospitalier (grille commune aux spécialités) × salarié (hôpital) × Norvège | 1 475 800 NOK | officielle (moyenne) | SSB, tableau 13848, 4e trimestre 2025 (S184) : médecins spécialistes à temps plein, 122 980 NOK par mois |

| Poste | Statut | Rapport au salaire moyen appliqué | Base |
|---|---|---|---|
| Orthophoniste | indépendant | 0,63 | estimé (structure) : rapport au salaire moyen 0,63 (FR) |
| Ingénieur sécurité cloud | salarié | 1,46 | estimé (structure) : rapport au salaire moyen 1,46 (FR+CH) |
| Consultant GRC (gouvernance, risques et conformité) | salarié | 1,26 | estimé (structure) : rapport au salaire moyen 1,26 (FR+CH) |
| Ophtalmologue | indépendant | 3,85 | estimé (structure) : rapport au salaire moyen 3,85 (FR+CH) |
| Pentesteur (auditeur en tests d'intrusion) | salarié | 1,15 | estimé (structure) : rapport au salaire moyen 1,15 (FR+CH) |
| Psychiatre | indépendant | 1,64 | estimé (structure) : rapport au salaire moyen 1,64 (FR+CH) |
| Cancérologue (oncologie médicale et radiothérapie) | indépendant | 5,00 | estimé (structure) : rapport au salaire moyen 8,33 (FR), plafonné à 5 |
| Cardiologue | indépendant | 3,89 | estimé (structure) : rapport au salaire moyen 3,89 (FR) |
| Pédiatre | indépendant | 2,01 | estimé (structure) : rapport au salaire moyen 2,01 (FR+CH) |
| Médecin généraliste (médecin de famille) | indépendant | 2,05 | estimé (structure) : rapport au salaire moyen 2,05 (FR+CH) |
| Sage-femme | indépendant | 0,96 | estimé (structure) : rapport au salaire moyen 0,96 (FR) |
| Actuaire | salarié | 1,45 | estimé (structure) : rapport au salaire moyen 1,45 (FR) |
| Médecin nucléaire | indépendant | 5,00 | estimé (structure) : rapport au salaire moyen 5,27 (FR), plafonné à 5 |
| Notaire | indépendant | 5,12 | estimé (structure) : rapport au salaire moyen 5,12 (FR) |
| Dermatologue | indépendant | 2,44 | estimé (structure) : rapport au salaire moyen 2,44 (FR) |
| Développeur logiciel | salarié | 1,09 | estimé (structure) : rapport au salaire moyen 1,09 (FR+CH) |
| Ingénieur cloud DevOps | salarié | 1,16 | estimé (structure) : rapport au salaire moyen 1,16 (FR+CH) |
| Orthoptiste | salarié | 0,87 | estimé (structure) : rapport au salaire moyen 0,87 (FR) |
| Rhumatologue | indépendant | 2,17 | estimé (structure) : rapport au salaire moyen 2,17 (FR) |
| Radiologue | indépendant | 4,38 | estimé (structure) : rapport au salaire moyen 4,38 (FR) |
| Anatomopathologiste | indépendant | 4,34 | estimé (structure) : rapport au salaire moyen 4,34 (FR) |
| Data engineer (ingénieur des données) | salarié | 1,17 | estimé (structure) : rapport au salaire moyen 1,17 (FR) |
| Responsable de la sécurité des systèmes d'information (RSSI) | salarié | 1,97 | estimé (structure) : rapport au salaire moyen 1,97 (FR+CH) |
| Chirurgien-dentiste omnipraticien | indépendant | 2,10 | estimé (structure) : rapport au salaire moyen 2,10 (FR+CH) |
| Masseur-kinésithérapeute | indépendant | 1,16 | estimé (structure) : rapport au salaire moyen 1,16 (FR) |
| Psychologue hospitalier | salarié | 0,84 | estimé (structure) : rapport au salaire moyen 0,84 (FR) |
| Pédicure-podologue | indépendant | 0,92 | estimé (structure) : rapport au salaire moyen 0,92 (FR) |
| Ergothérapeute hospitalier | salarié du secteur public | 0,84 | estimé (structure) : rapport au salaire moyen 0,84 (FR) |
| Diététicien | indépendant | 0,67 | estimé (structure) : rapport au salaire moyen 0,67 (FR) |
| Ingénieur méthodes et industrialisation | salarié | 1,25 | estimé (structure) : rapport au salaire moyen 1,25 (FR+CH) |
| Professeur des écoles | salarié du secteur public | 0,99 | estimé (structure) : rapport au salaire moyen 0,99 (FR) |
| Attaché d'administration de l'État | salarié du secteur public | 1,13 | estimé (structure) : rapport au salaire moyen 1,13 (FR) |
| Inspecteur des finances publiques | salarié du secteur public | 1,13 | estimé (structure) : rapport au salaire moyen 1,13 (FR) |
| Contrôleur des finances publiques | salarié du secteur public | 0,91 | estimé (structure) : rapport au salaire moyen 0,91 (FR) |
| Magistrat de l'ordre judiciaire | salarié du secteur public | 1,70 | estimé (structure) : rapport au salaire moyen 1,70 (FR) |
| Enseignant du secondaire I (cycle d'orientation), Genève | salarié du secteur public | 1,08 | estimé (structure) : rapport au salaire moyen 1,08 (CH) |
| Médecin spécialiste hospitalier (grille commune aux spécialités) | salarié (hôpital) | 2,17 | estimé (structure) : rapport au salaire moyen 2,17 (FR praticien hospitalier  CH médecin hospitalier) |

| Pays | Salaire moyen OCDE 2025 | Provenance | Niveau des prix 2024 (UE = 100) | Provenance | € PPA France par unité locale |
|---|---|---|---|---|---|
| France | 45 964 EUR | relayé (OCDE via Euronews, S167) | 111 | v6 (Eurostat 2024) | 1,000 |
| Pays-Bas | 69 028 EUR | relayé (S167) | 118 | connu | 0,941 |
| Suisse | 100 700 CHF | imputé : 107 487 € (OCDE via Euronews) × 0,937 | 174 | lu (S190) | 0,670 |
| Norvège | 801 695 NOK | relayé (S167) | 124 | lu (S190) | 0,077 |
| Allemagne | 66 700 EUR | lu (S167) | 109 | v6 (Eurostat 2024) ; 108,3 relayé (S190) | 1,018 |
| Luxembourg | 77 844 EUR | lu (S167) | 133 | lu (S190) | 0,835 |
| Islande | 12 433 527 ISK | lu (S167) | 162 | lu (S190) | 0,005 |
| Danemark | 537 071 DKK | lu (S167) | 143 | lu (S190) | 0,104 |
| Royaume-Uni | 55 983 GBP | lu (S167) | 115 | connu | 1,140 |
| Autriche | 63 054 EUR | lu (S167) | 111,7 | lu (S190) | 0,994 |
| Slovénie | 31 000 EUR | imputé : 53 697 USD PPA (S167), parité estimée | 90 | connu | 1,233 |

296 cellules sur 341 viennent de la règle de structure (estimées), toutes hors Suisse ; les 35 triplets suisses reprennent les cellules du classement 1.

### Classement 2, partie A : notes, palier et probabilité d'être dans les 10 premiers (60 premiers)

| Rang | ID | Triplet | EP | IT | QT | ES | CA | PS | RE | Palier | Top 10 (sur 8 pondérations) | P(10 premiers), variante A |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M004 | Orthophoniste × indépendant × Luxembourg (résident) | 5 | 4 | 5 | 4 | 5,0 | 5 | 2,1 | S* | 7 | 43 % |
| 2= | M007 | Orthophoniste × indépendant × Royaume-Uni | 5 | 4 | 5 | 3 | 5,0 | 5 | 2,2 | A* | 6 | 15 % |
| 2= | M001 | Orthophoniste × indépendant × Pays-Bas | 5 | 4 | 5 | 3 | 5,0 | 5 | 2,1 | A* | 6 | 14 % |
| 2= | M054 | Cardiologue × indépendant × Luxembourg (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 4,5 | A* | 6 | 35 % |
| 2= | M032 | Ophtalmologue × indépendant × Luxembourg (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 4,5 | A* | 6 | 35 % |
| 2= | M002 | Orthophoniste × indépendant × Norvège | 5 | 4 | 5 | 3 | 5,0 | 5 | 2,0 | A* | 6 | 14 % |
| 7= | M008 | Orthophoniste × indépendant × Autriche | 5 | 4 | 5 | 3 | 5,0 | 5 | 1,9 | A* | 6 | 12 % |
| 7= | M003 | Orthophoniste × indépendant × Allemagne | 5 | 4 | 5 | 3 | 5,0 | 5 | 1,9 | A* | 6 | 11 % |
| 7= | M005 | Orthophoniste × indépendant × Islande | 5 | 4 | 5 | 3 | 5,0 | 5 | 1,8 | A* | 6 | 11 % |
| 7= | M046 | Psychiatre × indépendant × Luxembourg (résident) | 5 | 3 | 4 | 4 | 4,5 | 5 | 3,3 | A* | 4 | 21 % |
| 7= | C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,2 | A* | 4 | 26 % |
| 12= | C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,1 | A | 3 | 25 % |
| 12= | M006 | Orthophoniste × indépendant × Danemark | 5 | 4 | 5 | 3 | 5,0 | 5 | 1,6 | A | 4 | 9 % |
| 12= | M082 | Actuaire × salarié × Luxembourg (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,1 | A | 3 | 19 % |
| 12= | C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,1 | A | 3 | 22 % |
| 12= | M014 | Ingénieur sécurité cloud × salarié × Luxembourg (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 3,1 | A | 3 | 21 % |
| 12= | M072 | Sage-femme × indépendant × Luxembourg (résident) | 4 | 3 | 5 | 4 | 5,0 | 5 | 2,6 | A | 3 | 10 % |
| 12= | M125 | Orthoptiste × salarié × Luxembourg (frontalier) | 5 | 4 | 4 | 4 | 4,0 | 5 | 2,5 | A | 2 | 9 % |
| 12= | M094 | Notaire × indépendant × Luxembourg (résident) | 5 | 3 | 4 | 3 | 4,5 | 4 | 4,9 | A | 2 | 19 % |
| 20= | M081 | Actuaire × salarié × Luxembourg (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,9 | A | 2 | 11 % |
| 20= | M024 | Consultant GRC (gouvernance, risques et conformité) × salarié × Luxembourg (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,9 | A | 2 | 15 % |
| 20= | M090 | Médecin nucléaire × indépendant × Luxembourg (résident) | 3 | 3 | 4 | 4 | 4,5 | 5 | 4,9 | A | 1 | 18 % |
| 20= | M050 | Cancérologue (oncologie médicale et radiothérapie) × indépendant × Luxembourg (résident) | 4 | 2 | 4 | 4 | 4,5 | 5 | 4,9 | A | 1 | 18 % |
| 20= | M013 | Ingénieur sécurité cloud × salarié × Luxembourg (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,9 | A | 0 | 13 % |
| 20= | M099 | Dermatologue × indépendant × Luxembourg (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,8 | A | 0 | 16 % |
| 20= | M038 | Pentesteur (auditeur en tests d'intrusion) × salarié × Luxembourg (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,8 | A | 0 | 12 % |
| 20= | M124 | Orthoptiste × salarié × Luxembourg (résident) | 5 | 4 | 4 | 4 | 4,0 | 5 | 2,2 | A | 1 | 6 % |
| 20= | C02 | Pédiatre × indépendant × Suisse (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,7 | A | 0 | 15 % |
| 20= | T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,7 | A | 0 | 15 % |
| 30= | M023 | Consultant GRC (gouvernance, risques et conformité) × salarié × Luxembourg (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,7 | A | 0 | 11 % |
| 30= | M137 | Radiologue × indépendant × Luxembourg (résident) | 3 | 3 | 4 | 4 | 4,5 | 5 | 4,7 | A | 1 | 15 % |
| 30= | M141 | Anatomopathologiste × indépendant × Luxembourg (résident) | 3 | 3 | 4 | 4 | 4,5 | 5 | 4,7 | A | 1 | 15 % |
| 30= | M133 | Rhumatologue × indépendant × Luxembourg (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,7 | A | 0 | 15 % |
| 30= | C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,6 | A | 0 | 11 % |
| 30= | M037 | Pentesteur (auditeur en tests d'intrusion) × salarié × Luxembourg (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,6 | A | 0 | 11 % |
| 30= | M009 | Orthophoniste × indépendant × Slovénie | 5 | 4 | 5 | 3 | 5,0 | 5 | 1,1 | A | 1 | 0 % |
| 30= | M053 | Cardiologue × indépendant × Allemagne | 4 | 3 | 4 | 3 | 4,5 | 5 | 4,6 | A | 1 | 15 % |
| 30= | M063 | Médecin généraliste (médecin de famille) × indépendant × Luxembourg (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,6 | A | 0 | 15 % |
| 30= | M031 | Ophtalmologue × indépendant × Allemagne | 4 | 3 | 4 | 3 | 4,5 | 5 | 4,6 | A | 1 | 14 % |
| 30= | M058 | Pédiatre × indépendant × Luxembourg (résident) | 4 | 3 | 4 | 4 | 4,5 | 5 | 3,6 | A | 0 | 15 % |
| 30= | C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,6 | A | 0 | 10 % |
| 30= | M055 | Cardiologue × indépendant × Autriche | 4 | 3 | 4 | 3 | 4,5 | 5 | 4,5 | A | 1 | 14 % |
| 30= | M033 | Ophtalmologue × indépendant × Autriche | 4 | 3 | 4 | 3 | 4,5 | 5 | 4,5 | A | 1 | 13 % |
| 30= | C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | 5 | 3 | 5 | 4 | 4,5 | 4 | 2,5 | A | 0 | 10 % |
| 45= | M052 | Cardiologue × indépendant × Pays-Bas | 4 | 3 | 4 | 3 | 4,5 | 5 | 4,4 | A | 0 | 13 % |
| 45= | M030 | Ophtalmologue × indépendant × Pays-Bas | 4 | 3 | 4 | 3 | 4,5 | 5 | 4,4 | A | 0 | 13 % |
| 45= | C03 | Ophtalmologue × indépendant × Suisse (résident) | 4 | 3 | 3 | 4 | 4,5 | 5 | 4,4 | A | 0 | 9 % |
| 45= | M185 | Masseur-kinésithérapeute × indépendant × Luxembourg (résident) | 2 | 4 | 5 | 4 | 5,0 | 5 | 2,8 | A | 0 | 6 % |
| 45= | M062 | Médecin généraliste (médecin de famille) × indépendant × Allemagne | 4 | 3 | 4 | 3 | 4,5 | 5 | 4,3 | A | 0 | 11 % |
| 45= | M045 | Psychiatre × indépendant × Allemagne | 5 | 3 | 4 | 3 | 4,5 | 5 | 3,2 | A | 0 | 5 % |
| 45= | M047 | Psychiatre × indépendant × Autriche | 5 | 3 | 4 | 3 | 4,5 | 5 | 3,2 | A | 0 | 5 % |
| 52= | M075 | Sage-femme × indépendant × Royaume-Uni | 4 | 3 | 5 | 3 | 5,0 | 5 | 2,7 | A | 0 | 3 % |
| 52= | M044 | Psychiatre × indépendant × Pays-Bas | 5 | 3 | 4 | 3 | 4,5 | 5 | 3,2 | A | 0 | 5 % |
| 52= | T37 | Développeur logiciel × salarié × Suisse (frontalier) | 5 | 3 | 5 | 4 | 4,5 | 3 | 3,1 | A | 0 | 4 % |
| 52= | T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | 5 | 3 | 4 | 4 | 4,5 | 4 | 3,1 | A | 0 | 10 % |
| 52= | M166 | Chirurgien-dentiste omnipraticien × indépendant × Luxembourg (résident) | 3 | 3 | 4 | 4 | 5,0 | 5 | 3,6 | A | 0 | 4 % |
| 52= | M286 | Magistrat de l'ordre judiciaire × fonctionnaire × Luxembourg (résident) | 5 | 3 | 4 | 3 | 4,5 | 5 | 3,1 | A | 0 | 9 % |
| 52= | M085 | Actuaire × salarié × Royaume-Uni | 5 | 3 | 5 | 3 | 4,5 | 4 | 3,1 | A | 0 | 3 % |
| 52= | M069 | Sage-femme × indépendant × Pays-Bas | 4 | 3 | 5 | 3 | 5,0 | 5 | 2,6 | A | 0 | 2 % |
| 52= | M070 | Sage-femme × indépendant × Norvège | 4 | 3 | 5 | 3 | 5,0 | 5 | 2,6 | A | 0 | 2 % |

Paliers sur les 341 triplets : S 1, A 281, B 54, C 5. Tableau complet dans `resultats_v7.json`.

### Classement 2, partie B : meilleur triplet de chaque pays et part des 10 premières places

| Pays | Places attendues dans les 10 premiers (somme des probabilités, A) | Rang du meilleur | ID | Meilleur triplet | Palier | P(10 premiers) | Enquête européenne 2021 |
|---|---|---|---|---|---|---|---|
| Luxembourg | 4,7 | 1 | M004 | Orthophoniste × indépendant × Luxembourg (résident) | S* | 43 % | couvert |
| Suisse | 1,7 | 7= | C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | A* | 26 % | couvert |
| Allemagne | 1,0 | 7= | M003 | Orthophoniste × indépendant × Allemagne | A* | 11 % | couvert |
| Autriche | 0,9 | 7= | M008 | Orthophoniste × indépendant × Autriche | A* | 12 % | couvert |
| Pays-Bas | 0,8 | 2= | M001 | Orthophoniste × indépendant × Pays-Bas | A* | 14 % | couvert |
| Royaume-Uni | 0,3 | 2= | M007 | Orthophoniste × indépendant × Royaume-Uni | A* | 15 % | non couvert par l'EWCTS 2021 |
| Norvège | 0,2 | 2= | M002 | Orthophoniste × indépendant × Norvège | A* | 14 % | couvert |
| Islande | 0,2 | 7= | M005 | Orthophoniste × indépendant × Islande | A* | 11 % | non couvert par l'EWCTS 2021 |
| Danemark | 0,1 | 12= | M006 | Orthophoniste × indépendant × Danemark | A | 9 % | couvert |
| Slovénie | 0,0 | 30= | M009 | Orthophoniste × indépendant × Slovénie | A | 0 % | couvert |

### Classement 2, partie C : revenu net après impôt (60 premiers)

| ID | Triplet | Cellule avant impôt, médiane / P80 | Impôt (médiane) | Médiane après impôt, k€ change / PPA | P80 après impôt, k€ change / PPA | Fiabilité | Source de la médiane |
|---|---|---|---|---|---|---|---|
| M004 | Orthophoniste × indépendant × Luxembourg (résident) | 49 / 79 kEUR | 23 % | 38 / 32 | 54 / 45 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,63 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M007 | Orthophoniste × indépendant × Royaume-Uni | 35 / 57 kGBP | 18 % | 34 / 33 | 51 / 50 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,63 (FR) × salaire moyen OCDE 2025 (55 983 GBP  lu (S167)) |
| M001 | Orthophoniste × indépendant × Pays-Bas | 43 / 70 kEUR | 18 % | 35 / 33 | 49 / 46 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,63 (FR) × salaire moyen OCDE 2025 (69 028 EUR  relayé (S167)) |
| M054 | Cardiologue × indépendant × Luxembourg (résident) | 302 / 489 kEUR | 43 % | 172 / 144 | 272 / 227 | estimé (structure) | estimé (structure) : rapport au salaire moyen 3,89 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M032 | Ophtalmologue × indépendant × Luxembourg (résident) | 299 / 481 kEUR | 43 % | 171 / 142 | 268 / 224 | estimé (structure) | estimé (structure) : rapport au salaire moyen 3,85 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M002 | Orthophoniste × indépendant × Norvège | 503 / 812 kNOK | 23 % | 33 / 30 | 50 / 45 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,63 (FR) × salaire moyen OCDE 2025 (801 695 NOK  relayé (S167)) |
| M008 | Orthophoniste × indépendant × Autriche | 40 / 64 kEUR | 27 % | 29 / 29 | 42 / 42 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,63 (FR) × salaire moyen OCDE 2025 (63 054 EUR  lu (S167)) |
| M003 | Orthophoniste × indépendant × Allemagne | 42 / 68 kEUR | 34 % | 28 / 28 | 41 / 42 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,63 (FR) × salaire moyen OCDE 2025 (66 700 EUR  lu (S167)) |
| M005 | Orthophoniste × indépendant × Islande | 7803 / 12589 kISK | 25 % | 40 / 27 | 60 / 40 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,63 (FR) × salaire moyen OCDE 2025 (12 433 527 ISK  lu (S167)) |
| M046 | Psychiatre × indépendant × Luxembourg (résident) | 128 / 206 kEUR | 38 % | 79 / 66 | 120 / 100 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,64 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 99 / 112 kCHF | 22 % | 82 / 75 | 92 / 83 | non officielle | Paymetric Labs 2026 (S178) : médiane 124 000 CHF, quartiles 120 000 et 131 000, senior 162 000 ; Optima, senior : 125 000 à 168 000 ; × 0,80 |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 92 / 107 kCHF | 22 % | 77 / 70 | 88 / 80 | non officielle | ERI SalaryExpert (S178) : consultant en cybersécurité, médiane 114 716 CHF (proxy) ; × 0,80 |
| M006 | Orthophoniste × indépendant × Danemark | 337 / 544 kDKK | 33 % | 30 / 23 | 47 / 36 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,63 (FR) × salaire moyen OCDE 2025 (537 071 DKK  lu (S167)) |
| M082 | Actuaire × salarié × Luxembourg (frontalier) | 113 / 143 kEUR | 37 % | 71 / 68 | 87 / 83 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,45 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 90 / 104 kCHF | 22 % | 75 / 69 | 86 / 78 | non officielle | ERI SalaryExpert, décembre 2025 (S178) : moyenne 114 262 CHF, 80 331 en début, 141 304 après 8 ans ; × 0,80 |
| M014 | Ingénieur sécurité cloud × salarié × Luxembourg (frontalier) | 114 / 128 kEUR | 37 % | 72 / 68 | 79 / 76 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,46 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M072 | Sage-femme × indépendant × Luxembourg (résident) | 75 / 121 kEUR | 31 % | 52 / 43 | 75 / 63 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,96 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M125 | Orthoptiste × salarié × Luxembourg (frontalier) | 68 / 78 kEUR | 29 % | 48 / 46 | 54 / 51 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,87 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M094 | Notaire × indépendant × Luxembourg (résident) | 399 / 644 kEUR | 44 % | 224 / 187 | 355 / 296 | estimé (structure) | estimé (structure) : rapport au salaire moyen 5,12 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M081 | Actuaire × salarié × Luxembourg (résident) | 113 / 143 kEUR | 37 % | 71 / 60 | 87 / 72 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,45 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M024 | Consultant GRC (gouvernance, risques et conformité) × salarié × Luxembourg (frontalier) | 98 / 117 kEUR | 35 % | 64 / 61 | 74 / 70 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,26 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M090 | Médecin nucléaire × indépendant × Luxembourg (résident) | 389 / 629 kEUR | 44 % | 219 / 182 | 347 / 289 | estimé (structure) | estimé (structure) : rapport au salaire moyen 5,27 (FR), plafonné à 5 × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M050 | Cancérologue (oncologie médicale et radiothérapie) × indépendant × Luxembourg (résident) | 389 / 629 kEUR | 44 % | 219 / 182 | 347 / 289 | estimé (structure) | estimé (structure) : rapport au salaire moyen 8,33 (FR), plafonné à 5 × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M013 | Ingénieur sécurité cloud × salarié × Luxembourg (résident) | 114 / 128 kEUR | 37 % | 72 / 60 | 79 / 66 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,46 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M099 | Dermatologue × indépendant × Luxembourg (résident) | 190 / 307 kEUR | 41 % | 111 / 93 | 175 / 146 | estimé (structure) | estimé (structure) : rapport au salaire moyen 2,44 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M038 | Pentesteur (auditeur en tests d'intrusion) × salarié × Luxembourg (frontalier) | 90 / 105 kEUR | 34 % | 59 / 57 | 67 / 64 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,15 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M124 | Orthoptiste × salarié × Luxembourg (résident) | 68 / 78 kEUR | 29 % | 48 / 40 | 54 / 45 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,87 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| C02 | Pédiatre × indépendant × Suisse (résident) | 167 / 268 kCHF | 21 % | 140 / 88 | 216 / 135 | relayée, groupe | OFS 2019 (S176) : groupe premier recours (médecine interne générale et pédiatrie)  médiane 172 000 CHF nets d'AVS et de 2e pilier ; moins la prime LAMal |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | 167 / 268 kCHF | 21 % | 140 / 88 | 216 / 135 | relayée | OFS 2019 (S24, S108) : premier recours, médiane 172 000 CHF nets d'AVS et de 2e pilier (relayée par la presse) ; moins la prime LAMal |
| M023 | Consultant GRC (gouvernance, risques et conformité) × salarié × Luxembourg (résident) | 98 / 117 kEUR | 35 % | 64 / 53 | 74 / 61 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,26 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M137 | Radiologue × indépendant × Luxembourg (résident) | 341 / 552 kEUR | 43 % | 193 / 161 | 305 / 255 | estimé (structure) | estimé (structure) : rapport au salaire moyen 4,38 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M141 | Anatomopathologiste × indépendant × Luxembourg (résident) | 338 / 546 kEUR | 43 % | 191 / 159 | 302 / 252 | estimé (structure) | estimé (structure) : rapport au salaire moyen 4,34 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M133 | Rhumatologue × indépendant × Luxembourg (résident) | 169 / 272 kEUR | 40 % | 100 / 84 | 156 / 130 | estimé (structure) | estimé (structure) : rapport au salaire moyen 2,17 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | 99 / 112 kCHF | 22 % | 82 / 52 | 92 / 57 | non officielle | Paymetric Labs 2026 (S178) : médiane 124 000 CHF, quartiles 120 000 et 131 000, senior 162 000 ; Optima, senior : 125 000 à 168 000 ; × 0,80 |
| M037 | Pentesteur (auditeur en tests d'intrusion) × salarié × Luxembourg (résident) | 90 / 105 kEUR | 34 % | 59 / 50 | 67 / 56 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,15 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M009 | Orthophoniste × indépendant × Slovénie | 20 / 31 kEUR | 31 % | 14 / 17 | 20 / 25 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,63 (FR) × salaire moyen OCDE 2025 (31 000 EUR  imputé : 53 697 USD PPA (S167)  parité estimée) |
| M053 | Cardiologue × indépendant × Allemagne | 259 / 419 kEUR | 44 % | 146 / 148 | 231 / 235 | estimé (structure) | estimé (structure) : rapport au salaire moyen 3,89 (FR) × salaire moyen OCDE 2025 (66 700 EUR  lu (S167)) |
| M063 | Médecin généraliste (médecin de famille) × indépendant × Luxembourg (résident) | 160 / 257 kEUR | 40 % | 95 / 79 | 148 / 123 | estimé (structure) | estimé (structure) : rapport au salaire moyen 2,05 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M031 | Ophtalmologue × indépendant × Allemagne | 257 / 412 kEUR | 44 % | 144 / 147 | 227 / 231 | estimé (structure) | estimé (structure) : rapport au salaire moyen 3,85 (FR+CH) × salaire moyen OCDE 2025 (66 700 EUR  lu (S167)) |
| M058 | Pédiatre × indépendant × Luxembourg (résident) | 157 / 253 kEUR | 40 % | 94 / 78 | 146 / 121 | estimé (structure) | estimé (structure) : rapport au salaire moyen 2,01 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | 92 / 107 kCHF | 22 % | 77 / 48 | 88 / 55 | non officielle | ERI SalaryExpert (S178) : consultant en cybersécurité, médiane 114 716 CHF (proxy) ; × 0,80 |
| M055 | Cardiologue × indépendant × Autriche | 245 / 396 kEUR | 41 % | 145 / 144 | 230 / 228 | estimé (structure) | estimé (structure) : rapport au salaire moyen 3,89 (FR) × salaire moyen OCDE 2025 (63 054 EUR  lu (S167)) |
| M033 | Ophtalmologue × indépendant × Autriche | 243 / 390 kEUR | 41 % | 143 / 143 | 226 / 225 | estimé (structure) | estimé (structure) : rapport au salaire moyen 3,85 (FR+CH) × salaire moyen OCDE 2025 (63 054 EUR  lu (S167)) |
| C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | 90 / 104 kCHF | 22 % | 75 / 47 | 86 / 54 | non officielle | ERI SalaryExpert, décembre 2025 (S178) : moyenne 114 262 CHF, 80 331 en début, 141 304 après 8 ans ; × 0,80 |
| M052 | Cardiologue × indépendant × Pays-Bas | 268 / 434 kEUR | 46 % | 145 / 137 | 229 / 215 | estimé (structure) | estimé (structure) : rapport au salaire moyen 3,89 (FR) × salaire moyen OCDE 2025 (69 028 EUR  relayé (S167)) |
| M030 | Ophtalmologue × indépendant × Pays-Bas | 266 / 427 kEUR | 46 % | 144 / 135 | 225 / 212 | estimé (structure) | estimé (structure) : rapport au salaire moyen 3,85 (FR+CH) × salaire moyen OCDE 2025 (69 028 EUR  relayé (S167)) |
| C03 | Ophtalmologue × indépendant × Suisse (résident) | 261 / 417 kCHF | 25 % | 210 / 131 | 327 / 204 | relayée, groupe | OFS 2019 (S176) : groupe à activité chirurgicale (ophtalmologie  ORL  chirurgie)  médiane 266 000 CHF nets d'AVS et de 2e pilier ; moins la prime LAMal |
| M185 | Masseur-kinésithérapeute × indépendant × Luxembourg (résident) | 90 / 146 kEUR | 34 % | 60 / 50 | 88 / 74 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,16 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M062 | Médecin généraliste (médecin de famille) × indépendant × Allemagne | 218 / 352 kEUR | 46 % | 118 / 120 | 191 / 195 | relayée (par cabinet, site secondaire) | Destatis 2023 relayé (S188) : médecine générale, revenu net de cabinet (Reinertrag) médian 218 000 € par cabinet |
| M045 | Psychiatre × indépendant × Allemagne | 109 / 177 kEUR | 43 % | 63 / 64 | 100 / 101 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,64 (FR+CH) × salaire moyen OCDE 2025 (66 700 EUR  lu (S167)) |
| M047 | Psychiatre × indépendant × Autriche | 103 / 167 kEUR | 38 % | 64 / 64 | 101 / 100 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,64 (FR+CH) × salaire moyen OCDE 2025 (63 054 EUR  lu (S167)) |
| M075 | Sage-femme × indépendant × Royaume-Uni | 54 / 87 kGBP | 22 % | 49 / 48 | 71 / 69 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,96 (FR) × salaire moyen OCDE 2025 (55 983 GBP  lu (S167)) |
| M044 | Psychiatre × indépendant × Pays-Bas | 113 / 183 kEUR | 40 % | 68 / 64 | 102 / 96 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,64 (FR+CH) × salaire moyen OCDE 2025 (69 028 EUR  relayé (S167)) |
| T37 | Développeur logiciel × salarié × Suisse (frontalier) | 91 / 108 kCHF | 22 % | 76 / 70 | 89 / 81 | relayée | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois ; × 12 × 0,80 |
| T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | 91 / 106 kCHF | 22 % | 76 / 70 | 87 / 79 | relayée, proxy | OFS, ESS 2024 (S26) : spécialistes TIC, médiane 9 490 CHF/mois (aucune donnée propre au cloud) ; × 12 × 0,80 |
| M166 | Chirurgien-dentiste omnipraticien × indépendant × Luxembourg (résident) | 163 / 264 kEUR | 40 % | 97 / 81 | 152 / 127 | estimé (structure) | estimé (structure) : rapport au salaire moyen 2,10 (FR+CH) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M286 | Magistrat de l'ordre judiciaire × fonctionnaire × Luxembourg (résident) | 132 / 159 kEUR | 39 % | 81 / 68 | 95 / 79 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,70 (FR) × salaire moyen OCDE 2025 (77 844 EUR  lu (S167)) |
| M085 | Actuaire × salarié × Royaume-Uni | 81 / 103 kGBP | 29 % | 67 / 66 | 82 / 80 | estimé (structure) | estimé (structure) : rapport au salaire moyen 1,45 (FR) × salaire moyen OCDE 2025 (55 983 GBP  lu (S167)) |
| M069 | Sage-femme × indépendant × Pays-Bas | 66 / 107 kEUR | 29 % | 47 / 44 | 65 / 62 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,96 (FR) × salaire moyen OCDE 2025 (69 028 EUR  relayé (S167)) |
| M070 | Sage-femme × indépendant × Norvège | 769 / 1243 kNOK | 27 % | 48 / 43 | 70 / 63 | estimé (structure) | estimé (structure) : rapport au salaire moyen 0,96 (FR) × salaire moyen OCDE 2025 (801 695 NOK  relayé (S167)) |

Bornes de l'échelle du classement 2 : médiane 17 à 194 k€, P80 23 à 306 k€ PPA.

### Classement 2, partie D : provenance des notes (60 premiers)

Sur 2046 notes : 1 sourcées, 1043 mixtes, 1002 estimées. Hors Suisse, aucune note n'est sourcée : les ancrages viennent de France, de Suisse ou de l'UE, donc au mieux mixtes (1.13).

| ID | Triplet | EP | IT | QT | ES | CA | PS |
|---|---|---|---|---|---|---|---|
| M004 | Orthophoniste × indépendant × Luxembourg (résident) | E | E | E | M (S2), tension S2 | M | M (P7) |
| M007 | Orthophoniste × indépendant × Royaume-Uni | E | E | E | M (S2), tension S2 | M | M (P7) |
| M001 | Orthophoniste × indépendant × Pays-Bas | E | E | E | M (S2), tension S2 | M | M (P7) |
| M054 | Cardiologue × indépendant × Luxembourg (résident) | E | E | M (Q2, Q18) | E | M | M (P6) |
| M032 | Ophtalmologue × indépendant × Luxembourg (résident) | E | E | M (Q2, Q18) | E | M | M (P6) |
| M002 | Orthophoniste × indépendant × Norvège | E | E | E | M (S2), tension S2 | M | M (P7) |
| M008 | Orthophoniste × indépendant × Autriche | E | E | E | M (S2), tension S2 | M | M (P7) |
| M003 | Orthophoniste × indépendant × Allemagne | E | E | E | M (S2), tension S2 | M | M (P7) |
| M005 | Orthophoniste × indépendant × Islande | E | E | E | M (S2), tension S2 | M | M (P7) |
| M046 | Psychiatre × indépendant × Luxembourg (résident) | E | E | M (Q2, Q18) | E | M | M (P6) |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M006 | Orthophoniste × indépendant × Danemark | E | E | E | M (S2), tension S2 | M | M (P7) |
| M082 | Actuaire × salarié × Luxembourg (frontalier) | M (E1) | E | E | E | M | M (P2) |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M014 | Ingénieur sécurité cloud × salarié × Luxembourg (frontalier) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M072 | Sage-femme × indépendant × Luxembourg (résident) | E | E | E | M (S2), tension S2 | M | E |
| M125 | Orthoptiste × salarié × Luxembourg (frontalier) | E | E | E | M (S2), tension S2 | M | E |
| M094 | Notaire × indépendant × Luxembourg (résident) | E | E | E | E | M | E |
| M081 | Actuaire × salarié × Luxembourg (résident) | M (E1) | E | E | E | M | M (P2) |
| M024 | Consultant GRC (gouvernance, risques et conformité) × salarié × Luxembourg (frontalier) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M090 | Médecin nucléaire × indépendant × Luxembourg (résident) | E | E | M (Q2, Q18) | E | M | M (P6) |
| M050 | Cancérologue (oncologie médicale et radiothérapie) × indépendant × Luxembourg (résident) | E | E | M (Q2, Q18) | E | M | M (P6) |
| M013 | Ingénieur sécurité cloud × salarié × Luxembourg (résident) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M099 | Dermatologue × indépendant × Luxembourg (résident) | E | E | M (Q2, Q18) | E | M | M (P6) |
| M038 | Pentesteur (auditeur en tests d'intrusion) × salarié × Luxembourg (frontalier) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M124 | Orthoptiste × salarié × Luxembourg (résident) | E | E | E | M (S2), tension S2 | M | E |
| C02 | Pédiatre × indépendant × Suisse (résident) | E | E | M (Q10, Q15) | E | M | M (P8) |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | E | E | M (Q10, Q15) | E | M | S (P8) |
| M023 | Consultant GRC (gouvernance, risques et conformité) × salarié × Luxembourg (résident) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M137 | Radiologue × indépendant × Luxembourg (résident) | E | E | M (Q2, Q18) | E | M | M (P6) |
| M141 | Anatomopathologiste × indépendant × Luxembourg (résident) | E | E | M (Q2, Q18) | E | M | M (P6) |
| M133 | Rhumatologue × indépendant × Luxembourg (résident) | E | E | M (Q2, Q18) | E | M | M (P6) |
| C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M037 | Pentesteur (auditeur en tests d'intrusion) × salarié × Luxembourg (résident) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M009 | Orthophoniste × indépendant × Slovénie | E | E | E | M (S2), tension S2 | M | M (P7) |
| M053 | Cardiologue × indépendant × Allemagne | E | E | M (Q2, Q18) | E | M | M (P6) |
| M063 | Médecin généraliste (médecin de famille) × indépendant × Luxembourg (résident) | E | E | M (Q10, Q15) | E | M | M (P8) |
| M031 | Ophtalmologue × indépendant × Allemagne | E | E | M (Q2, Q18) | E | M | M (P6) |
| M058 | Pédiatre × indépendant × Luxembourg (résident) | E | E | M (Q10, Q15) | E | M | M (P8) |
| C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M055 | Cardiologue × indépendant × Autriche | E | E | M (Q2, Q18) | E | M | M (P6) |
| M033 | Ophtalmologue × indépendant × Autriche | E | E | M (Q2, Q18) | E | M | M (P6) |
| C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | M (E1) | E | M (Q19), tension Q19 | E | M | M (P4, P12) |
| M052 | Cardiologue × indépendant × Pays-Bas | E | E | M (Q2, Q18) | E | M | M (P6) |
| M030 | Ophtalmologue × indépendant × Pays-Bas | E | E | M (Q2, Q18) | E | M | M (P6) |
| C03 | Ophtalmologue × indépendant × Suisse (résident) | E | E | M (Q15) | E | M | E |
| M185 | Masseur-kinésithérapeute × indépendant × Luxembourg (résident) | E | E | M (Q9) | M (S2), tension S2 | M | E |
| M062 | Médecin généraliste (médecin de famille) × indépendant × Allemagne | E | E | M (Q10, Q15) | E | M | M (P8) |
| M045 | Psychiatre × indépendant × Allemagne | E | E | M (Q2, Q18) | E | M | M (P6) |
| M047 | Psychiatre × indépendant × Autriche | E | E | M (Q2, Q18) | E | M | M (P6) |
| M075 | Sage-femme × indépendant × Royaume-Uni | E | E | E | M (S2), tension S2 | M | E |
| M044 | Psychiatre × indépendant × Pays-Bas | E | E | M (Q2, Q18) | E | M | M (P6) |
| T37 | Développeur logiciel × salarié × Suisse (frontalier) | M (E1) | E | E | E | M | M (P12) |
| T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | M (E1) | E | E | E | M | M (P12) |
| M166 | Chirurgien-dentiste omnipraticien × indépendant × Luxembourg (résident) | M (E8) | E | M (Q17) | E | M | E |
| M286 | Magistrat de l'ordre judiciaire × fonctionnaire × Luxembourg (résident) | M (E1) | E | E | E | M | M (P1) |
| M085 | Actuaire × salarié × Royaume-Uni | M (E1) | E | E | E | M | M (P2) |
| M069 | Sage-femme × indépendant × Pays-Bas | E | E | E | M (S2), tension S2 | M | E |
| M070 | Sage-femme × indépendant × Norvège | E | E | E | M (S2), tension S2 | M | E |

### Classement 2, partie E : rang dans les 8 pondérations (30 premiers)

| ID | Triplet | Poids égaux | environnement physique ×2 | intensité du travail ×2 | qualité du temps de travail ×2 | environnement social ×2 | compétences et autonomie ×2 | perspectives et sécurité ×2 | revenu ×2 | Étendue |
|---|---|---|---|---|---|---|---|---|---|---|
| M004 | Orthophoniste × indépendant × Luxembourg (résident) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 22 | 1 à 22 |
| M007 | Orthophoniste × indépendant × Royaume-Uni | 2 | 2 | 2 | 2 | 23 | 2 | 2 | 44 | 2 à 44 |
| M001 | Orthophoniste × indépendant × Pays-Bas | 2 | 2 | 2 | 2 | 23 | 2 | 2 | 44 | 2 à 44 |
| M054 | Cardiologue × indépendant × Luxembourg (résident) | 2 | 24 | 10 | 21 | 2 | 8 | 2 | 1 | 1 à 24 |
| M032 | Ophtalmologue × indépendant × Luxembourg (résident) | 2 | 24 | 10 | 21 | 2 | 8 | 2 | 1 | 1 à 24 |
| M002 | Orthophoniste × indépendant × Norvège | 2 | 2 | 2 | 2 | 23 | 2 | 2 | 53 | 2 à 53 |
| M008 | Orthophoniste × indépendant × Autriche | 7 | 2 | 2 | 2 | 35 | 2 | 2 | 63 | 2 à 63 |
| M003 | Orthophoniste × indépendant × Allemagne | 7 | 6 | 6 | 6 | 35 | 6 | 8 | 63 | 6 à 63 |
| M005 | Orthophoniste × indépendant × Islande | 7 | 6 | 6 | 6 | 35 | 6 | 8 | 63 | 6 à 63 |
| M046 | Psychiatre × indépendant × Luxembourg (résident) | 7 | 6 | 14 | 27 | 4 | 12 | 8 | 22 | 4 à 27 |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 7 | 6 | 14 | 6 | 4 | 12 | 33 | 22 | 4 à 33 |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 12 | 10 | 14 | 9 | 4 | 12 | 33 | 34 | 4 à 34 |
| M006 | Orthophoniste × indépendant × Danemark | 12 | 10 | 8 | 9 | 40 | 8 | 11 | 93 | 8 à 93 |
| M082 | Actuaire × salarié × Luxembourg (frontalier) | 12 | 10 | 14 | 9 | 4 | 12 | 33 | 34 | 4 à 34 |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 12 | 10 | 14 | 9 | 4 | 12 | 33 | 34 | 4 à 34 |
| M014 | Ingénieur sécurité cloud × salarié × Luxembourg (frontalier) | 12 | 10 | 14 | 9 | 4 | 12 | 33 | 41 | 4 à 41 |
| M072 | Sage-femme × indépendant × Luxembourg (résident) | 12 | 30 | 21 | 9 | 4 | 8 | 11 | 53 | 4 à 53 |
| M125 | Orthoptiste × salarié × Luxembourg (frontalier) | 12 | 10 | 8 | 32 | 11 | 50 | 11 | 53 | 8 à 53 |
| M094 | Notaire × indépendant × Luxembourg (résident) | 12 | 10 | 21 | 32 | 40 | 19 | 46 | 1 | 1 à 46 |
| M081 | Actuaire × salarié × Luxembourg (résident) | 20 | 10 | 21 | 9 | 11 | 19 | 46 | 44 | 9 à 46 |
| M024 | Consultant GRC (gouvernance, risques et conformité) × salarié × Luxembourg (frontalier) | 20 | 10 | 21 | 9 | 11 | 19 | 46 | 44 | 9 à 46 |
| M090 | Médecin nucléaire × indépendant × Luxembourg (résident) | 20 | 119 | 21 | 32 | 11 | 19 | 11 | 1 | 1 à 119 |
| M050 | Cancérologue (oncologie médicale et radiothérapie) × indépendant × Luxembourg (résident) | 20 | 40 | 74 | 32 | 11 | 19 | 11 | 1 | 1 à 74 |
| M013 | Ingénieur sécurité cloud × salarié × Luxembourg (résident) | 20 | 19 | 21 | 17 | 11 | 19 | 46 | 44 | 11 à 46 |
| M099 | Dermatologue × indépendant × Luxembourg (résident) | 20 | 40 | 21 | 32 | 11 | 19 | 16 | 22 | 11 à 40 |
| M038 | Pentesteur (auditeur en tests d'intrusion) × salarié × Luxembourg (frontalier) | 20 | 19 | 30 | 17 | 11 | 19 | 66 | 53 | 11 à 66 |
| M124 | Orthoptiste × salarié × Luxembourg (résident) | 20 | 19 | 10 | 54 | 11 | 50 | 16 | 78 | 10 à 78 |
| C02 | Pédiatre × indépendant × Suisse (résident) | 20 | 61 | 30 | 54 | 11 | 19 | 16 | 22 | 11 à 61 |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | 20 | 61 | 30 | 54 | 11 | 19 | 16 | 22 | 11 à 61 |
| M023 | Consultant GRC (gouvernance, risques et conformité) × salarié × Luxembourg (résident) | 30 | 19 | 30 | 17 | 11 | 19 | 66 | 53 | 11 à 66 |

### Classement 2, partie F : robustesse aux notes et au revenu, 10 000 tirages

| ID | Triplet | P(10 premiers) A | B | C | D | E | P(1er) A | B | D | E | Rang médian A [5e à 95e centile] | Notes tirées (A) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M004 | Orthophoniste × indépendant × Luxembourg (résident) | 43 % | 48 % | 28 % | 42 % | 42 % | 8,4 % | 18,2 % | 8,3 % | 11,8 % | 20 [1 à 71] | 3 |
| M054 | Cardiologue × indépendant × Luxembourg (résident) | 35 % | 36 % | 26 % | 34 % | 34 % | 8,7 % | 11,7 % | 9,3 % | 10,5 % | 25 [1 à 129] | 3 |
| M032 | Ophtalmologue × indépendant × Luxembourg (résident) | 35 % | 34 % | 26 % | 35 % | 35 % | 7,9 % | 8,2 % | 9,0 % | 10,0 % | 26 [1 à 132] | 3 |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 26 % | 28 % | 16 % | 25 % | 27 % | 2,8 % | 8,5 % | 2,8 % | 5,1 % | 31 [2 à 141] | 2 |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 25 % | 27 % | 14 % | 22 % | 25 % | 2,6 % | 5,0 % | 2,3 % | 4,4 % | 32 [2 à 144] | 2 |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 22 % | 25 % | 13 % | 21 % | 24 % | 2,2 % | 2,7 % | 2,1 % | 3,1 % | 34 [2 à 147] | 2 |
| M046 | Psychiatre × indépendant × Luxembourg (résident) | 21 % | 20 % | 16 % | 19 % | 20 % | 2,2 % | 2,2 % | 2,0 % | 3,5 % | 34 [2 à 147] | 3 |
| M014 | Ingénieur sécurité cloud × salarié × Luxembourg (frontalier) | 21 % | 24 % | 13 % | 21 % | 22 % | 1,7 % | 1,7 % | 1,7 % | 0,0 % | 35 [2 à 150] | 2 |
| M094 | Notaire × indépendant × Luxembourg (résident) | 19 % | 23 % | 18 % | 17 % | 22 % | 5,4 % | 7,0 % | 4,6 % | 6,6 % | 44 [1 à 228] | 5 |
| M082 | Actuaire × salarié × Luxembourg (frontalier) | 19 % | 21 % | 14 % | 17 % | 19 % | 1,7 % | 4,1 % | 1,6 % | 2,6 % | 38 [3 à 154] | 3 |
| M090 | Médecin nucléaire × indépendant × Luxembourg (résident) | 18 % | 21 % | 17 % | 18 % | 22 % | 4,0 % | 2,8 % | 3,8 % | 5,7 % | 41 [2 à 166] | 3 |
| M050 | Cancérologue (oncologie médicale et radiothérapie) × indépendant × Luxembourg (résident) | 18 % | 20 % | 17 % | 18 % | 22 % | 3,8 % | 1,7 % | 3,5 % | 4,8 % | 41 [2 à 167] | 3 |
| M099 | Dermatologue × indépendant × Luxembourg (résident) | 16 % | 18 % | 16 % | 18 % | 21 % | 3,4 % | 1,2 % | 3,4 % | 5,1 % | 45 [2 à 173] | 3 |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | 15 % | 16 % | 19 % | 15 % | 19 % | 3,2 % | 0,6 % | 2,6 % | 4,2 % | 50 [2 à 181] | 3 |
| M024 | Consultant GRC (gouvernance, risques et conformité) × salarié × Luxembourg (frontalier) | 15 % | 20 % | 11 % | 16 % | 18 % | 0,9 % | 0,9 % | 1,1 % | 0,0 % | 41 [3 à 159] | 2 |
| C02 | Pédiatre × indépendant × Suisse (résident) | 15 % | 16 % | 14 % | 16 % | 18 % | 3,3 % | 0,7 % | 2,9 % | 4,3 % | 50 [2 à 180] | 3 |
| M063 | Médecin généraliste (médecin de famille) × indépendant × Luxembourg (résident) | 15 % | 13 % | 12 % | 14 % | 14 % | 2,5 % | 0,1 % | 2,2 % | 0,0 % | 60 [3 à 193] | 3 |
| M141 | Anatomopathologiste × indépendant × Luxembourg (résident) | 15 % | 15 % | 13 % | 15 % | 17 % | 2,6 % | 0,3 % | 2,7 % | 3,7 % | 53 [3 à 184] | 3 |
| M053 | Cardiologue × indépendant × Allemagne | 15 % | 13 % | 12 % | 14 % | 14 % | 2,3 % | 0,2 % | 2,0 % | 0,0 % | 60 [4 à 194] | 3 |
| M058 | Pédiatre × indépendant × Luxembourg (résident) | 15 % | 11 % | 12 % | 14 % | 14 % | 2,1 % | 0,0 % | 2,1 % | 0,0 % | 61 [4 à 196] | 3 |
| M133 | Rhumatologue × indépendant × Luxembourg (résident) | 15 % | 14 % | 14 % | 15 % | 17 % | 2,4 % | 0,1 % | 2,4 % | 3,9 % | 54 [3 à 185] | 3 |
| M137 | Radiologue × indépendant × Luxembourg (résident) | 15 % | 15 % | 14 % | 15 % | 17 % | 3,0 % | 0,4 % | 2,8 % | 3,9 % | 52 [3 à 185] | 3 |
| M007 | Orthophoniste × indépendant × Royaume-Uni | 15 % | 21 % | 12 % | 15 % | 16 % | 0,2 % | 1,4 % | 0,3 % | 0,0 % | 49 [4 à 119] | 3 |
| M001 | Orthophoniste × indépendant × Pays-Bas | 14 % | 19 % | 10 % | 14 % | 14 % | 0,1 % | 0,4 % | 0,3 % | 0,0 % | 52 [5 à 124] | 3 |
| M002 | Orthophoniste × indépendant × Norvège | 14 % | 14 % | 10 % | 14 % | 9 % | 0,0 % | 0,0 % | 0,1 % | 0,0 % | 59 [7 à 134] | 3 |
| M031 | Ophtalmologue × indépendant × Allemagne | 14 % | 12 % | 12 % | 14 % | 14 % | 2,2 % | 0,0 % | 1,9 % | 0,0 % | 61 [4 à 196] | 3 |
| M055 | Cardiologue × indépendant × Autriche | 14 % | 11 % | 11 % | 13 % | 12 % | 1,6 % | 0,0 % | 1,8 % | 0,0 % | 64 [5 à 199] | 3 |
| M033 | Ophtalmologue × indépendant × Autriche | 13 % | 10 % | 11 % | 13 % | 12 % | 1,5 % | 0,0 % | 1,7 % | 0,0 % | 64 [5 à 198] | 3 |
| M013 | Ingénieur sécurité cloud × salarié × Luxembourg (résident) | 13 % | 17 % | 10 % | 14 % | 16 % | 0,7 % | 0,5 % | 0,9 % | 0,0 % | 44 [3 à 163] | 2 |
| M052 | Cardiologue × indépendant × Pays-Bas | 13 % | 9 % | 11 % | 13 % | 10 % | 1,6 % | 0,0 % | 1,8 % | 0,0 % | 68 [5 à 203] | 3 |

Plus forte probabilité d'être 1er : A M054 (8,7 %) ; B M004 (18,2 %) ; C M054 (6,3 %) ; D M054 (9,3 %) ; E M004 (11,8 %). Aucune ne dépasse 50 % : pas de 1er désigné.

### Classement 2, partie G : sensibilité sans la règle de langue (informatif)

| Rang sans la règle | ID | Triplet | Rang avec la règle |
|---|---|---|---|
| 1 | M001 | Orthophoniste × indépendant × Pays-Bas | 2= |
| 1 | M002 | Orthophoniste × indépendant × Norvège | 2= |
| 1 | M004 | Orthophoniste × indépendant × Luxembourg (résident) | 1 |
| 1 | M007 | Orthophoniste × indépendant × Royaume-Uni | 2= |
| 5 | M003 | Orthophoniste × indépendant × Allemagne | 7= |
| 5 | M005 | Orthophoniste × indépendant × Islande | 7= |
| 5 | M008 | Orthophoniste × indépendant × Autriche | 7= |
| 8 | M006 | Orthophoniste × indépendant × Danemark | 12= |
| 9 | M009 | Orthophoniste × indépendant × Slovénie | 30= |
| 9 | M030 | Ophtalmologue × indépendant × Pays-Bas | 45= |
| 9 | M031 | Ophtalmologue × indépendant × Allemagne | 30= |
| 9 | M032 | Ophtalmologue × indépendant × Luxembourg (résident) | 2= |
| 9 | M033 | Ophtalmologue × indépendant × Autriche | 30= |
| 9 | M052 | Cardiologue × indépendant × Pays-Bas | 45= |
| 9 | M053 | Cardiologue × indépendant × Allemagne | 30= |
| 9 | M054 | Cardiologue × indépendant × Luxembourg (résident) | 2= |
| 9 | M055 | Cardiologue × indépendant × Autriche | 30= |
| 18 | C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 12= |
| 18 | C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 7= |
| 18 | C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 12= |

### Classement 2, partie H : égalités et frontières

Égalités dans les 40 premiers : rang 2 : M007, M001, M054, M032, M002 ; rang 7 : M008, M003, M005, M046, C15 ; rang 12 : C17, M006, M082, C13, M014, M072, M125, M094 ; rang 20 : M081, M024, M090, M050, M013, M099, M038, M124, C02, T30 ; rang 30 : M023, M137, M141, M133, C14, M037, M009, M053, M063, M031, M058, C16, M055, M033, C12.

À moins de 0,1 d'une frontière dans les 40 premiers : M004 (S), M007 (A), M001 (A), M054 (A), M032 (A), M002 (A), M008 (A), M003 (A), M005 (A), M046 (A), C15 (A).

## 5. Vérification des barèmes fiscaux

### Vérification des barèmes au salaire moyen

| Pays | Salaire moyen 2025 (monnaie locale) | Impôt et cotisations salariales calculés | Cible OCDE | Écart (points) | Provenance de la cible |
|---|---|---|---|---|---|
| Luxembourg | 77 844 | 31,4 % | 32,0 % | moins 0,6 | taux lu |
| Pays-Bas | 69 028 | 30,2 % | 27,9 % | plus 2,3 | taux lu ; salaire moyen relayé |
| Norvège | 801 695 | 28,1 % | 28,1 % | plus 0,0 | taux lu ; salaire moyen relayé |
| Allemagne | 66 700 | 39,1 % | 38,7 % | plus 0,4 | déduit du coin fiscal de 49,3 % |
| Autriche | 63 054 | 33,4 % | 33,3 % | plus 0,1 | lu, colonne incertaine |
| Danemark | 537 071 | 35,6 % | 35,5 % | plus 0,1 | déduit du coin fiscal de 35,8 % |
| Islande | 12 433 527 | 30,9 % | 31,2 % | moins 0,3 | déduit du coin fiscal de 31,5 % (27,2 %), plus 4 % de pension obligatoire |
| Royaume-Uni | 55 983 | 23,1 % | 23,1 % | plus 0,0 | déduit du coin fiscal de 32,4 % |
| Slovénie | 31 000 | 35,0 % | 36,5 % | moins 1,5 | déduit du coin fiscal de 45,3 % ; salaire moyen imputé |

Cibles : taux moyen publié (S167) ou déduit du coin fiscal publié (S183) avec une part patronale estimée. Genève : points lus 16,5 % à 100 000 CHF, 22,5 % à 200 000, 25 % à 300 000 (S179). France : contrôle à 100 000 € de bénéfice libéral, impôt de 26,7 %.

## 6. Cellules signalées

### Cellules revenu signalées (classement 1)

| ID | Triplet | Fiabilité | Temps de travail réel connu |
|---|---|---|---|
| T15 | Orthophoniste × libéral × France | non officielle | non : 38 à 39 actes par semaine et 10 h de tâches administratives (FNO) ; durée totale non trouvée |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | non officielle | oui |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | non officielle | oui |
| F03 | Ophtalmologue × libéral × France | relayée | non : temps de travail non trouvé |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | non officielle | oui |
| F13 | Psychiatre × libéral × France | relayée | non : temps de travail non trouvé |
| F06 | Cancérologue (oncologie médicale et radiothérapie) × libéral × France | relayée | non : temps de travail non trouvé |
| F09 | Cardiologue × libéral × France | relayée (2024, site secondaire) | non : temps de travail non trouvé |
| C02 | Pédiatre × indépendant × Suisse (résident) | relayée, groupe | non : temps de travail non trouvé |
| F16 | Ingénieur sécurité cloud × salarié × France | non officielle | oui |
| C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | non officielle | oui |
| C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | non officielle | oui |
| C03 | Ophtalmologue × indépendant × Suisse (résident) | relayée, groupe | non : temps de travail non trouvé |
| C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | non officielle | oui |
| T09 | Sage-femme × libéral × France | officielle | non : temps de travail non trouvé |
| T46 | Actuaire × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| F07 | Médecin nucléaire × libéral × France | relayée | non : temps de travail non trouvé |
| F17 | Consultant GRC (gouvernance, risques et conformité) × salarié × France | relayée, proxy | oui |
| F19 | Notaire × libéral × France | relayée (site secondaire) | non : temps de travail non trouvé |
| F10 | Dermatologue × libéral × France | relayée (2024, site secondaire) | non : temps de travail non trouvé |
| T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | relayée, proxy | oui |
| T16 | Orthoptiste × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| F12 | Rhumatologue × libéral × France | relayée | non : temps de travail non trouvé |
| F02 | Radiologue × libéral × France | relayée | non : temps de travail non trouvé |
| F15 | Pentesteur (auditeur en tests d'intrusion) × salarié × France | non officielle | oui |
| F05 | Anatomopathologiste × libéral × France | relayée | non : temps de travail non trouvé |
| T85 | Data engineer (ingénieur des données) × salarié × France | relayée, proxy | oui |
| C01 | Psychiatre × indépendant × Suisse (résident) | relayée, groupe | non : temps de travail non trouvé |
| C19 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × Suisse (frontalier) | non officielle | oui |
| F14 | Pédiatre × libéral × France | relayée (année non confirmée) | non : temps de travail non trouvé |
| T35 | Développeur logiciel (études et développement) × salarié × France | relayée | non : champ temps complet non précisé (DARES) |
| T05 | Chirurgien-dentiste omnipraticien × libéral × France | relayée | non : temps de travail non trouvé |
| F08 | Gastro-entérologue × libéral × France | relayée (site secondaire) | non : temps de travail non trouvé |
| T86 | Ingénieur cloud DevOps × salarié × Suisse (résident) | relayée, proxy | oui |
| T41 | Ingénieur méthodes et industrialisation × salarié × France | relayée, proxy | oui |
| C22 | Enseignant du secondaire I (cycle d'orientation), Genève × fonctionnaire cantonal × Suisse (résident) | non officielle | oui |
| C18 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × Suisse (résident) | non officielle | oui |
| T81 | Ingénieur cloud DevOps × indépendant (freelance) × France | non officielle | oui |
| T76 | Pédicure-podologue × libéral × France | non re-sourcée | non : temps de travail non trouvé |
| T80 | Ingénieur cloud DevOps × salarié × France | relayée, proxy | oui |
| T42 | Ingénieur méthodes et industrialisation × salarié × Suisse (frontalier) | relayée, proxy | oui |
| T68 | Expert-comptable × libéral × France | relayée, proxy | non : temps de travail non trouvé |
| T02 | Médecin généraliste × salarié (centre de santé) × France | non officielle | oui |
| F18 | Responsable de la sécurité des systèmes d'information (RSSI) × salarié × France | non officielle | oui |
| T20 | Psychologue hospitalier × contractuel FPH × France | non re-sourcée | non : temps de travail non trouvé |
| T62 | Contrôleur des finances publiques × fonctionnaire × France | officielle, proxy | oui |
| T60 | Attaché d'administration de l'État × fonctionnaire × France | officielle, proxy | oui |
| T61 | Inspecteur des finances publiques × fonctionnaire × France | officielle, proxy | oui |
| T42r | Ingénieur méthodes et industrialisation × salarié × Suisse (résident) | relayée, proxy | oui |
| C21 | Administrateur de programme (P-3), Nations unies, Genève × fonctionnaire international × Suisse (frontalier) | relayée, estimée | oui |
| T78 | Diététicien × libéral × France | non re-sourcée | non : temps de travail non trouvé |
| T34 | Physiothérapeute × salarié × Suisse (frontalier) | officielle, proxy | oui |
| F04 | Anesthésiste-réanimateur × libéral × France | relayée | non : temps de travail non trouvé |
| T36 | Développeur logiciel × indépendant (freelance) × France | non officielle | oui |
| C20 | Administrateur de programme (P-3), Nations unies, Genève × fonctionnaire international × Suisse (résident) | relayée, estimée | oui |
| T34r | Physiothérapeute × salarié × Suisse (résident) | officielle, proxy | oui |
| T18 | Audioprothésiste × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| F11 | Gynécologue-obstétricien × libéral × France | relayée (année incertaine) | non : temps de travail non trouvé |
| T11 | Masseur-kinésithérapeute hospitalier × fonctionnaire FPH × France | officielle, proxy | oui |
| T22 | Ostéopathe × libéral × France | non officielle | non : temps de travail non trouvé |
| T72 | Attaché commercial B2B × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| T13 | Infirmier en soins généraux (IDE) × libéral × France | officielle | non : temps de travail non trouvé |
| T69 | Comptable × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| T67 | Avocat × libéral × France | relayée | non : temps de travail non trouvé |
| C11 | Analyste SOC (niveaux 1 et 2) × salarié × Suisse (frontalier) | non officielle | oui |
| T19 | Vétérinaire praticien × libéral × France | relayée | non : temps de travail non trouvé |
| T45 | Technicien systèmes et réseaux × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| T29f | Médecin hospitalier (chef de clinique à médecin adjoint) × salarié (hôpital) × Suisse (frontalier) | officielle ancienne | oui |
| C10 | Analyste SOC (niveaux 1 et 2) × salarié × Suisse (résident) | non officielle | oui |
| T29 | Médecin hospitalier (chef de clinique à médecin adjoint) × salarié (hôpital) × Suisse (résident) | officielle ancienne | oui |
| T84 | Analyste SOC (niveaux 1 et 2) × salarié × France | relayée, proxy | oui |
| T79 | Opticien-lunetier × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| T74 | Pilote de ligne × salarié × France | non officielle | oui |
| T04 | Praticien hospitalier (spécialiste, grille commune à toutes les spécialités) × statut PH (public) × France | officielle, champ plus large | oui |
| T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | non re-sourcée | non : temps de travail non trouvé |
| T07 | Pharmacien titulaire d'officine × indépendant × France | relayée | non : temps de travail non trouvé |
| T17 | Manipulateur en électroradiologie médicale (MERM) × fonctionnaire FPH × France | officielle, proxy | oui |
| T24 | Infirmier en soins généraux hospitalier × salarié × Suisse (frontalier) | officielle ancienne | oui |
| T49 | Électricien de montage (CFC) × salarié × Suisse (frontalier) | relayée, proxy | oui |
| T53 | Conducteur de train × salarié (SNCF) × France | non re-sourcée | non : temps de travail non trouvé |
| T47 | Électricien du bâtiment × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| T23 | Infirmier en soins généraux hospitalier × salarié × Suisse (résident) | officielle ancienne | oui |
| T49r | Électricien de montage (CFC) × salarié × Suisse (résident) | relayée, proxy | oui |
| T52 | Frigoriste (froid et climatisation) × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| T73 | Agent immobilier × indépendant (mandataire) × France | relayée, proxy | non : temps de travail non trouvé |
| T44 | Technicien de maintenance industrielle × salarié × France | non re-sourcée | non : temps de travail non trouvé |
| T48 | Électricien du bâtiment × artisan × France | relayée, proxy | non : temps de travail non trouvé |
| T51 | Plombier-chauffagiste × artisan × France | relayée, proxy | non : temps de travail non trouvé |
| T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France | officielle, champ plus large | oui |
| T58 | Gardien de la paix × fonctionnaire × France | relayée, proxy | oui |
| T33 | Assistant en soins et santé communautaire (ASSC) × salarié × Suisse (frontalier) | officielle, proxy | oui |
| T21 | Aide-soignant hospitalier × fonctionnaire FPH × France | officielle, champ plus large | oui |
| T33r | Assistant en soins et santé communautaire (ASSC) × salarié × Suisse (résident) | officielle, proxy | oui |
| T55 | Conducteur routier poids lourd × salarié × France | officielle ancienne | oui |

## 7. Conclusions (version 7)

### 7.1 Classement 1, France et Suisse : pas de 1er, un groupe de tête de 20 triplets

| Constat | Valeur | Où le lire |
|---|---|---|
| 1er désigné | Aucun : la plus forte probabilité d'être 1er est 10,8 % (F03, ophtalmologue libéral en France, variante A) ; 14,6 % au mieux toutes variantes confondues (C15, variante B). Seuil de la règle : 50 %. | 3, partie E |
| Groupe de tête (P(10 premiers) ≥ 20 %, variante A) | 20 triplets, de 49 % (C15) à 21 % (T82) ; aucun ne dépasse 53 % dans aucune variante. | 7.4, tableau « Classement 1, groupe de tête » |
| Familles du groupe | Médecins libéraux français à revenu élevé (ophtalmologue, cancérologue, cardiologue, médecin nucléaire, dermatologue, psychiatre) et médecins indépendants suisses (médecin de famille, pédiatre, ophtalmologue) : 9 triplets ; postes de cybersécurité en Suisse et en France (ingénieur sécurité cloud, consultant GRC, pentesteur), frontaliers devant résidents : 8 triplets ; orthophoniste libéral en France, notaire, ingénieur cloud DevOps frontalier : 3 triplets. | 3, partie A |
| Places attendues dans les 10 premiers | France 5,8 ; Suisse en résident 2,3 ; Suisse en frontalier 1,9 (somme des probabilités, variante A). | calcul de la partie E |
| Palier | Aucun triplet en S ; T15 (orthophoniste) à moins de 0,1 de S ; 64 triplets en A, 31 en B, 16 en C. | 3, partie A |
| Effet de l'impôt (changement déclaré en 1.15) | Il resserre les écarts de revenu : les médecins libéraux français perdent 22 % à 40 % de leur cellule, les salariés suisses environ 22 %, les fonctionnaires internationaux rien. | 3, partie B |
| Scénario IA fort | Les postes de cybersécurité (exposition moyenne ou élevée) sortent des 10 premiers, sauf C15 au 10e rang partagé ; les médecins, l'orthophoniste et la sage-femme libérale (exposition faible) les remplacent. | 7.4, « Classement 1, deux scénarios IA » |

### 7.2 Classement 2, 10 pays retenus : pas de 1er, un groupe de tête de 8 triplets

| Constat | Valeur | Où le lire |
|---|---|---|
| Tri des pays | Pays-Bas, Suisse, Norvège, Allemagne, Luxembourg, Islande, Danemark, Royaume-Uni, Autriche, Slovénie. Les 8 premiers sont retenus dans au moins 85 % des tirages ; l'Autriche (78 %) et la Slovénie (69 %) sont fragiles, la Suède (29 %) est la première exclue. La France (34e) et tous les pays hors Europe, Singapour et les Émirats compris, sont exclus. | 2 |
| 1er désigné | Aucun : 8,7 % au plus (M054, cardiologue indépendant au Luxembourg, variante A) ; 18,2 % au mieux toutes variantes (M004, orthophoniste au Luxembourg, variante B). | 4, partie F |
| Groupe de tête (≥ 20 %) | Orthophoniste au Luxembourg 43 % ; cardiologue et ophtalmologue indépendants au Luxembourg 35 % ; ingénieur sécurité cloud, consultant GRC et pentesteur frontaliers en Suisse 26 %, 25 % et 22 % ; psychiatre indépendant au Luxembourg 21 % ; ingénieur sécurité cloud frontalier au Luxembourg 21 %. | 7.4, « Classement 2, groupe de tête » |
| Places attendues dans les 10 premiers, par pays | Luxembourg 4,7 ; Suisse 1,7 ; Allemagne 1,0 ; Autriche 0,9 ; Pays-Bas 0,85 ; Royaume-Uni 0,3 ; Norvège 0,2 ; Islande 0,15 ; Danemark 0,1 ; Slovénie 0,0. | 4, partie B |
| Ce qui fait gagner le Luxembourg et la Suisse | La règle de langue (ES moins 1 hors pays francophones, 1.10) : sans elle, l'orthophoniste est 1er à égalité au Luxembourg, au Royaume-Uni, aux Pays-Bas et en Norvège. Au Luxembourg s'ajoutent un salaire moyen élevé et un impôt modéré, appliqués par la règle de structure. | 4, partie G |
| Palier | 1 triplet en S (M004, à moins de 0,1 de la frontière), 281 en A, 54 en B, 5 en C. | 4, partie A |
| Scénario IA fort | Les 10 premiers sont identiques : ce sont tous des postes à exposition faible. | 7.4, « Classement 2, deux scénarios IA » |
| Dimensions sans donnée comparable | Aucun pays hors Europe ne passe le tri. Parmi les 10 retenus, l'Islande et le Royaume-Uni ne sont pas couverts par l'enquête européenne de 2021 (EWCTS) : leurs notes hors revenu sont transposées sans aucune mesure locale. Pour les 8 autres, l'enquête existe mais aucun de ses chiffres par métier n'a pu être lu. | 2, 4 partie B |

### 7.3 Ce qui est vérifié par des données, et ce qui dépend d'estimations

| Élément | Vérifié par des données | Dépend d'estimations |
|---|---|---|
| Tri des pays | Revenu net au salaire moyen lu pour 9 pays (OCDE 2026), heures lues pour 18 pays, tension au travail lue pour 3 pays (S167, S170, S171, S173) | Valeurs « imputées » ou « connues » pour les autres ; tension bornée par bandes (moins de 10 %, 11 à 15 %) pour 21 pays, absente pour 16 (médiane) ; poids égaux des trois piliers (choix normatif) |
| Impôt | Barèmes légaux 2025 ; écart au taux moyen de l'OCDE au salaire moyen compris entre moins 1,5 et plus 2,3 points | Simplifications (une part, sans crédits ni déductions personnelles) ; Genève : points intermédiaires du barème à la source ; indépendants suisses et allemands : approximations ; impôt de l'UE (18 %) |
| Revenu, classement 1 | Spécialités libérales : moyennes CARMF 2023 relayées par la presse médicale pour 9 des 13 spécialités et le généraliste (année non confirmée pour la pédiatrie) ; médecins suisses : médianes OFS 2019 par groupe ; postes repris de la v6 : sources de la v6 | Médiane = moyenne × 0,85 pour les libéraux ; 4 spécialités sur des montants de sites secondaires ou d'année incertaine ; postes de cybersécurité suisses et 3 français : sites de salaires et cabinets de recrutement (« non officielle ») ; surcoût de 10 % pour les frontaliers de Genève |
| Revenu, classement 2 | 10 cellules lues hors Suisse (SSB, Danmarks Statistik, NHS, ONS, Destatis, Bundesagentur, CBS), presque toutes par des relais | 296 cellules sur 341 viennent de la règle de structure : tout le Luxembourg sauf l'administrateur de l'UE, toute l'Autriche, l'Islande, la Slovénie, et la plupart des postes ailleurs ; plafond de 5 fois le salaire moyen pour les spécialistes |
| Prix | Niveaux des prix 2024 lus pour 7 des 10 pays (S190) ; change BCE (S191) | Pays-Bas, Slovénie, Royaume-Uni : valeurs connues, non revérifiées |
| Notes hors revenu, classement 1 | 12 notes sourcées sur 666 ; 3 modifiées par un chiffre ; facteurs de garde (F3) fondés sur des textes légaux | 343 estimées, 311 mixtes (dont les 111 notes CA) ; 29 tensions avec un chiffre de groupe |
| Notes hors revenu, classement 2 | 1 note sourcée sur 2 046 (en Suisse) | Toutes les notes hors Suisse sont transposées du poste français ou suisse ; règle de langue normative ; statut transposé sans vérifier l'existence de l'exercice libéral pays par pays (sauf spécialités et notariat) |
| Robustesse | 8 pondérations et 10 000 tirages par variante, graine fixe (20261029), reproductibles | Les tirages ne testent que des écarts de plus ou moins 1 sur les notes estimées et de plus ou moins 20 % sur les revenus incertains ; une erreur de structure (revenu luxembourgeois, conditions de travail transposées) n'est pas couverte |

### 7.4 Groupes de tête et scénarios IA (tableaux générés)

#### Classement 1, groupe de tête

| ID | Triplet | P(10 premiers), A | Étendue sur A à E | P(1er), A | Rang | Palier | Palier, IA fort | Médiane après impôt, k€ change / PPA | Fiabilité du revenu | Notes hors revenu |
|---|---|---|---|---|---|---|---|---|---|---|
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 49 % | 35 % à 53 % | 9,2 % | 2= | A* | A | 82 / 75 | non officielle | S 0, M 4, E 2 |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 48 % | 35 % à 52 % | 7,8 % | 2= | A | A | 77 / 70 | non officielle | S 0, M 4, E 2 |
| F03 | Ophtalmologue × libéral × France | 47 % | 43 % à 51 % | 10,8 % | 2= | A | A | 110 / 110 | relayée | S 0, M 3, E 3 |
| T15 | Orthophoniste × libéral × France | 44 % | 36 % à 46 % | 4,2 % | 1 | A* | A | 21 / 21 | non officielle | S 0, M 3, E 3 |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 41 % | 34 % à 45 % | 5,6 % | 2= | A | A | 75 / 69 | non officielle | S 0, M 4, E 2 |
| F06 | Cancérologue (oncologie médicale et radiothérapie) × libéral × France | 39 % | 38 % à 40 % | 7,7 % | 7= | A | A | 180 / 180 | relayée | S 0, M 3, E 3 |
| F09 | Cardiologue × libéral × France | 37 % | 36 % à 39 % | 6,6 % | 7= | A | A | 96 / 96 | relayée (2024, site secondaire) | S 0, M 3, E 3 |
| T30 | Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) | 36 % | 36 % à 41 % | 5,6 % | 9= | A | A | 140 / 88 | relayée | S 1, M 2, E 3 |
| C02 | Pédiatre × indépendant × Suisse (résident) | 36 % | 33 % à 36 % | 5,2 % | 9= | A | A | 140 / 88 | relayée, groupe | S 0, M 3, E 3 |
| F16 | Ingénieur sécurité cloud × salarié × France | 30 % | 20 % à 31 % | 1,7 % | 9= | A | A | 52 / 52 | non officielle | S 1, M 3, E 2 |
| C14 | Ingénieur sécurité cloud × salarié × Suisse (résident) | 30 % | 23 % à 30 % | 1,5 % | 9= | A | A | 82 / 52 | non officielle | S 0, M 4, E 2 |
| F13 | Psychiatre × libéral × France | 30 % | 30 % à 32 % | 3,2 % | 2= | A | A | 59 / 59 | relayée | S 0, M 3, E 3 |
| C16 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (résident) | 29 % | 21 % à 29 % | 1,5 % | 13= | A | A | 77 / 48 | non officielle | S 0, M 4, E 2 |
| F07 | Médecin nucléaire × libéral × France | 29 % | 26 % à 29 % | 4,0 % | 13= | A | A | 124 / 124 | relayée | S 0, M 3, E 3 |
| C12 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (résident) | 28 % | 19 % à 28 % | 0,9 % | 13= | A | A | 75 / 47 | non officielle | S 0, M 4, E 2 |
| F10 | Dermatologue × libéral × France | 27 % | 24 % à 27 % | 3,5 % | 21= | A | A | 66 / 66 | relayée (2024, site secondaire) | S 0, M 3, E 3 |
| C03 | Ophtalmologue × indépendant × Suisse (résident) | 25 % | 21 % à 27 % | 2,9 % | 13= | A | A | 210 / 131 | relayée, groupe | S 0, M 2, E 4 |
| F19 | Notaire × libéral × France | 24 % | 23 % à 25 % | 4,2 % | 13= | A | A | 121 / 121 | relayée (site secondaire) | S 0, M 1, E 5 |
| F17 | Consultant GRC (gouvernance, risques et conformité) × salarié × France | 23 % | 14 % à 23 % | 0,7 % | 13= | A | A | 43 / 43 | relayée, proxy | S 1, M 3, E 2 |
| T82 | Ingénieur cloud DevOps × salarié × Suisse (frontalier) | 21 % | 21 % à 23 % | 2,1 % | 21= | A | A | 76 / 70 | relayée, proxy | S 0, M 3, E 3 |

Seuil de présentation : 20 % de chances d'être dans les 10 premiers (variante A), choix d'affichage aussi arbitraire qu'une frontière de palier ; 20 triplets. Plus forte probabilité d'être 1er : F03, 10,8 % : sous 50 %, aucun 1er n'est désigné (règle 1.15).

#### Classement 1, deux scénarios IA

| Place | Scénario 1 : IA sans effet sur l'emploi (classement de base) | Scénario 2 : IA fort (PS moins 1 ou 2, revenu brut × 0,9 ou × 0,8 selon l'exposition) | Rang partagé, scénario 2 |
|---|---|---|---|
| 1 | T15 Orthophoniste × libéral × France (faible) | T15 Orthophoniste × libéral × France (faible, rang de base 1) | 1 |
| 2 | C15 Ingénieur sécurité cloud × salarié × Suisse (frontalier) (moyenne) | F03 Ophtalmologue × libéral × France (faible, rang de base 2=) | 2 |
| 3 | C17 Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) (élevée) | F13 Psychiatre × libéral × France (faible, rang de base 2=) | 2 |
| 4 | F03 Ophtalmologue × libéral × France (faible) | F06 Cancérologue (oncologie médicale et radiothérapie) × libéral × France (faible, rang de base 7=) | 2 |
| 5 | C13 Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) (moyenne) | F09 Cardiologue × libéral × France (faible, rang de base 7=) | 5 |
| 6 | F13 Psychiatre × libéral × France (faible) | C02 Pédiatre × indépendant × Suisse (résident) (faible, rang de base 9=) | 5 |
| 7 | F06 Cancérologue (oncologie médicale et radiothérapie) × libéral × France (faible) | T30 Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) (faible, rang de base 9=) | 5 |
| 8 | F09 Cardiologue × libéral × France (faible) | C03 Ophtalmologue × indépendant × Suisse (résident) (faible, rang de base 13=) | 8 |
| 9 | C02 Pédiatre × indépendant × Suisse (résident) (faible) | T09 Sage-femme × libéral × France (faible, rang de base 13=) | 8 |
| 10 | T30 Médecin de famille (médecine interne générale) × indépendant × Suisse (résident) (faible) | F12 Rhumatologue × libéral × France (faible, rang de base 21=) | 10 |

Scénarios bornés déclarés en v2 et inchangés ; exposition notée faible, moyenne ou élevée par poste (estimation, poids de preuve faible) ; fonctionnaires : choc réduit d'un cran.

#### Classement 2, groupe de tête

| ID | Triplet | P(10 premiers), A | Étendue sur A à E | P(1er), A | Rang | Palier | Palier, IA fort | Médiane après impôt, k€ change / PPA | Fiabilité du revenu | Notes hors revenu |
|---|---|---|---|---|---|---|---|---|---|---|
| M004 | Orthophoniste × indépendant × Luxembourg (résident) | 43 % | 28 % à 48 % | 8,4 % | 1 | S* | S | 38 / 32 | estimé (structure) | S 0, M 3, E 3 |
| M054 | Cardiologue × indépendant × Luxembourg (résident) | 35 % | 26 % à 36 % | 8,7 % | 2= | A* | A | 172 / 144 | estimé (structure) | S 0, M 3, E 3 |
| M032 | Ophtalmologue × indépendant × Luxembourg (résident) | 35 % | 26 % à 35 % | 7,9 % | 2= | A* | A | 171 / 142 | estimé (structure) | S 0, M 3, E 3 |
| C15 | Ingénieur sécurité cloud × salarié × Suisse (frontalier) | 26 % | 16 % à 28 % | 2,8 % | 7= | A* | A | 82 / 75 | non officielle | S 0, M 4, E 2 |
| C17 | Consultant GRC (gouvernance, risques et conformité) × salarié × Suisse (frontalier) | 25 % | 14 % à 27 % | 2,6 % | 12= | A | A | 77 / 70 | non officielle | S 0, M 4, E 2 |
| C13 | Pentesteur (auditeur en tests d'intrusion) × salarié × Suisse (frontalier) | 22 % | 13 % à 25 % | 2,2 % | 12= | A | A | 75 / 69 | non officielle | S 0, M 4, E 2 |
| M046 | Psychiatre × indépendant × Luxembourg (résident) | 21 % | 16 % à 21 % | 2,2 % | 7= | A* | A | 79 / 66 | estimé (structure) | S 0, M 3, E 3 |
| M014 | Ingénieur sécurité cloud × salarié × Luxembourg (frontalier) | 21 % | 13 % à 24 % | 1,7 % | 12= | A | A | 72 / 68 | estimé (structure) | S 0, M 4, E 2 |

Seuil de présentation : 20 % de chances d'être dans les 10 premiers (variante A), choix d'affichage aussi arbitraire qu'une frontière de palier ; 8 triplets. Plus forte probabilité d'être 1er : M054, 8,7 % : sous 50 %, aucun 1er n'est désigné (règle 1.15).

#### Classement 2, deux scénarios IA

| Place | Scénario 1 : IA sans effet sur l'emploi (classement de base) | Scénario 2 : IA fort (PS moins 1 ou 2, revenu brut × 0,9 ou × 0,8 selon l'exposition) | Rang partagé, scénario 2 |
|---|---|---|---|
| 1 | M004 Orthophoniste × indépendant × Luxembourg (résident) (faible) | M004 Orthophoniste × indépendant × Luxembourg (résident) (faible, rang de base 1) | 1 |
| 2 | M007 Orthophoniste × indépendant × Royaume-Uni (faible) | M007 Orthophoniste × indépendant × Royaume-Uni (faible, rang de base 2=) | 2 |
| 3 | M001 Orthophoniste × indépendant × Pays-Bas (faible) | M001 Orthophoniste × indépendant × Pays-Bas (faible, rang de base 2=) | 2 |
| 4 | M054 Cardiologue × indépendant × Luxembourg (résident) (faible) | M054 Cardiologue × indépendant × Luxembourg (résident) (faible, rang de base 2=) | 2 |
| 5 | M032 Ophtalmologue × indépendant × Luxembourg (résident) (faible) | M032 Ophtalmologue × indépendant × Luxembourg (résident) (faible, rang de base 2=) | 2 |
| 6 | M002 Orthophoniste × indépendant × Norvège (faible) | M002 Orthophoniste × indépendant × Norvège (faible, rang de base 2=) | 2 |
| 7 | M008 Orthophoniste × indépendant × Autriche (faible) | M008 Orthophoniste × indépendant × Autriche (faible, rang de base 7=) | 7 |
| 8 | M003 Orthophoniste × indépendant × Allemagne (faible) | M003 Orthophoniste × indépendant × Allemagne (faible, rang de base 7=) | 7 |
| 9 | M005 Orthophoniste × indépendant × Islande (faible) | M005 Orthophoniste × indépendant × Islande (faible, rang de base 7=) | 7 |
| 10 | M046 Psychiatre × indépendant × Luxembourg (résident) (faible) | M046 Psychiatre × indépendant × Luxembourg (résident) (faible, rang de base 7=) | 7 |

Scénarios bornés déclarés en v2 et inchangés ; exposition notée faible, moyenne ou élevée par poste (estimation, poids de preuve faible) ; fonctionnaires : choc réduit d'un cran.


### 7.5 Ce que l'on peut conclure, et ce que l'on ne peut pas

| Conclusion | Force |
|---|---|
| En France et en Suisse, aucun triplet ne se détache : 20 triplets ont chacun entre 21 % et 49 % de chances d'être dans les 10 premiers, et aucun n'a plus de 15 % de chances d'être 1er. | Vérifiée par le calcul, sous les règles déclarées |
| Les spécialités libérales françaises à revenu élevé et les médecins indépendants suisses tiennent la tête dans les deux scénarios d'IA ; les postes de cybersécurité suisses ne la tiennent que si l'IA n'a pas d'effet sur l'emploi. | Revenus relayés pour les médecins ; exposition à l'IA estimée |
| Le classement 2 désigne surtout un pays (le Luxembourg) et une règle (la langue), pas un poste : ses meilleurs triplets reposent sur un revenu estimé par structure et sur des notes transposées. | Faible : à confirmer par des salaires luxembourgeois par profession |
| Le tri des pays est plus solide que le classement 2 des triplets : 8 pays sur 10 sont retenus dans au moins 85 % des tirages. | Moyenne : 3 valeurs de tension lues sur 40 |
| Pour départager le groupe de tête, il faudrait d'abord : les heures et conditions de travail par spécialité (DREES), les salaires suisses par profession à 4 chiffres (ESS de l'OFS), les revenus des médecins et des orthophonistes au Luxembourg (CNS, IGSS, STATEC), et le tableau complet de la CARMF. | Domaines à ouvrir dans les réglages réseau de l'environnement |

## 8. Sources

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
| S155 | Suisse, services de garde des médecins : guide juridique de la FMH : https://leitfaden.fmh.ch/rechtlicher-leitfaden/2-rahmenbedingungen-des-arztes/24-berufspflichten-arzt.pdf?c=51717 ; taxe de dispense, Appenzell Rhodes-Extérieures : https://files.entscheidsuche.ch/chunks/AR/OG/004/OG-O4V-22-4_2022-10-27.pdf ; Vaud : https://www.vd.ch/fileadmin/user_upload/themes/sante/Professionnels/Formation/Syst%C3%A8me_de_la_garde_m%C3%A9dicale.pdf |
| S156 | Suisse, service d'urgence dentaire : Argovie : https://www.ag.ch/de/themen/gesundheit/gesundheitsversorgung/zahnmedizin ; règlement de Schwytz : https://sz.ch/public/upload/assets/38678/Reglement_der_Zahnaerztegesellschaft_des_Kantons_Schwyz_fuer_den_zahnaerztlichen_Notfalldienst.pdf?fp=3 ; Zurich : https://www.zh.ch/de/gesundheit/gesundheitsberufe/fachspezifische-informationen/zahnmedizin.html |
| S157 | France, permanence des soins dentaires : Conseil d'État, 29 mai 2020, n° 422956 : https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2020-05-29/422956 ; ARS PACA : https://www.paca.ars.sante.fr/lorganisation-de-la-permanence-et-la-continuite-des-soins-0 ; ARS Centre-Val de Loire : https://www.centre-val-de-loire.ars.sante.fr/media/3628/download ; ARS Grand Est : https://www.grand-est.paps.sante.fr/media/43674/download |
| S158 | France, permanence des soins des médecins : amendement citant l'Ordre des médecins (2025) : https://www.assemblee-nationale.fr/dyn/17/amendements/0966/CION-SOC/AS78.pdf ; loi de 2023 sans obligation individuelle : https://www.lequotidiendumedecin.fr/liberal-soins-de-ville/exercice/en-cas-dechec-des-discussions-nous-nhesiterons-pas-poser-une-obligation-de-garde-la-ou-cest |
| S159 | Cybersécurité, astreintes et horaires : France Travail : https://www.francetravail.fr/actualites/le-dossier/numerique-telecoms/informatique---web/travailler-dans-la-cybersecurite.html ; ANSSI, observatoire des métiers 2025 : https://cyber.gouv.fr/actualites/publication-de-la-4e-%C3%A9dition-de-lobservatoire-des-m%C3%A9tiers-2025/ ; relais : https://www.lemondeinformatique.fr/actualites/lire-l-evolution-des-metiers-de-la-cybersecurite-etudiee-par-l-anssi-97127.html ; https://www.solutions-numeriques.com/metiers-de-la-cybersecurite-une-cartographie-des-transformations/ ; enquête Bitdefender (relais) : https://www.techradar.com/pro/cybersecurity-workers-are-increasingly-working-over-the-weekends-and-many-are-ready-to-quit ; https://www.itpro.com/security/cyber-security-staff-are-working-weekends-more-than-ever-before-and-it-needs-to-stop |
| S160 | Obsan, besoins en médecins de premier recours (relais cantonaux) : https://kr-geschaefte.zug.ch/dokumente/202/13030_1794_1_Aerztemangel.pdf ; rapport Obsan 04/2022 : https://www.obsan.admin.ch/sites/default/files/2022-05/Obsan_04_2022_BERICHT.pdf ; étude Workforce 2025 : https://www.srf.ch/news/schweiz/studie-der-uni-basel-hausaerzteverband-schlaegt-wegen-fachkraeftemangel-alarm |
| S161 | HRSA, état des effectifs de santé 2024 : https://bhw.hrsa.gov/sites/default/files/bureau-health-workforce/state-of-the-health-workforce-report-2024.pdf ; contestation de l'ADA : https://www.drbicuspid.com/dental-hygiene/article/15370469/ada-disputes-hrsas-projection-of-dentist-shortage-in-2025 |
| S162 | BLS, orthophonistes, projections 2024 à 2034 : https://www.bls.gov/ooh/healthcare/speech-language-pathologists.htm |
| S163 | SSO, enquête 2016 sur l'utilisation des cabinets dentaires (relais) : https://www.zwp-online.info/zwpnews/dental-news/branchenmeldungen/umfrage-zur-auslastung-schweizer-zahnaerzte-stehen-unter-druck ; https://www.zm-online.de/news/detail/zahnarztpraxen-in-urbaner-schweiz-fehlen-patienten |
| S164 | Suisse, pénurie dans l'informatique : classement 2019 de l'Université de Zurich : https://www.stellenmarktmonitor.uzh.ch/dam/jcr:3e64333f-3678-4f1a-9216-59127d4f4d1d/Fachkraeftemangel_Rankings_2019.pdf ; système d'indicateurs du SECO : https://www.seco.admin.ch/seco/en/home/Publikationen_Dienstleistungen/Publikationen_und_Formulare/Arbeit/Arbeitsmarkt/Informationen_Arbeitsmarktforschung/fachkraeftemangel-in-der-schweiz---ein-indikatorensystem-zur-beu.html ; chômage des TIC : https://www.itreseller.ch/Artikel/103736/Zahl_der_arbeitslosen_Informatiker_steigt.html |
| S165 | DARES, critères ergonomiques par métier (Sumer 2017) : https://travail-emploi.gouv.fr/IMG/pdf/1a_-_expositions_aux_criteres_ergonomiques_par_metiers_sumer_17112023.pdf |
| S166 | Épuisement professionnel et projections : enquête CARPIMKO (relais) : https://www.caducee.net/actualite-medicale/15357/burnout-hyperstress-penibilite-les-chiffres-alarmants-de-la-souffrance-au-travail-des-soignants-liberaux.html ; https://www.previssima.fr/actualite/70-des-auxiliaires-medicaux-liberaux-presentent-un-epuisement-emotionnel-dont-40-de-maniere-severe-retour-sur-cette-etude-avec-l.html ; Ordre des chirurgiens-dentistes, lettre 166 (2018) : https://www.ordre-chirurgiens-dentistes.fr/wp-content/uploads/2020/12/La_Lettre_166_2018.pdf ; DREES, projections des chirurgiens-dentistes : https://drees.solidarites-sante.gouv.fr/publications/etudes-et-resultats/8-000-chirurgiennes-dentistes-supplementaires-dici-2040 ; https://drees.solidarites-sante.gouv.fr/communique-de-presse/medecins-sages-femmes-chirurgiens-dentistes-et-pharmaciens-combien-de |
| S167 | OCDE, Taxing Wages 2026 (données 2025) : https://www.oecd.org/en/publications/2026/04/taxing-wages-2026_d1f39986/full-report/overview_d93131c3.html ; annexe méthodologique (salaires moyens) : https://www.oecd.org/en/publications/taxing-wages-2026_3a5169ef-en/full-report/methodology-and-limitations_f25b8cbc.html ; Allemagne : https://www.oecd.org/en/publications/taxing-wages-2026_3a5169ef-en/full-report/germany_8f4270cd.html ; Royaume-Uni : https://www.oecd.org/en/publications/taxing-wages-2026_3a5169ef-en/full-report/united-kingdom-2025-2026-income-tax-year_98c92486.html ; salaires moyens en euros (relais) : https://www.euronews.com/2026/05/15/average-wages-across-europe-countries-with-the-highest-and-lowest-salaries ; Pays-Bas et Norvège (relais) : https://logos-pres.md/en/news/average-salaries-in-europe-differences-and-causes/ |
| S168 | Singapour, ministère de la Main-d'œuvre : https://stats.mom.gov.sg/Pages/IncomeTimeSeries.aspx ; https://stats.mom.gov.sg/pages/hours-worked-summary-table.aspx |
| S169 | Émirats arabes unis, salaire moyen attribué au FCSC (site secondaire) : https://wage.is/uae/ |
| S170 | Heures travaillées en 2024, données de l'OCDE (relais) : https://www.bamboohr.com/blog/working-hours-around-the-world-infographic |
| S171 | Heures travaillées en 2023, données de l'OCDE (relais) : https://www.visualcapitalist.com/annual-working-hours-in-countries-2023/ |
| S172 | OCDE, Compendium of Productivity Indicators 2024 : https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/02/oecd-compendium-of-productivity-indicators-2024_d224133f/b96cd88a-en.pdf |
| S173 | OCDE, Employment Outlook 2024, qualité de l'emploi et tension au travail en 2021 : https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/07/oecd-employment-outlook-2024_abc8ad82/ac8b3538-en.pdf |
| S174 | CARMF, revenus 2023 des médecins libéraux par spécialité (relais) : http://www.lequotidiendumedecin.fr/liberal-soins-de-ville/honoraires/revenus-2023-des-medecins-liberaux-121-000-euros-en-moyenne-le-palmares-des-specialites-tops-et ; https://www.whatsupdoc-lemag.fr/article/revenus-des-medecins-liberaux-les-specialites-qui-payent-le-mieux-et-le-moins-bien ; https://docteurimago.fr/actualite/socioprofessionnel/les-revenus-des-radiologues-ont-augmente-de-025-en-2023-selon-la-carmf/ ; https://www.egora.fr/actus-pro/remuneration/revenus-des-medecins-liberaux-top-et-flop-des-specialites-en-2023 |
| S175 | Spécialités, montants relayés par des sites secondaires : gastro-entérologie : https://www.hoppi.work/salaire-gastro-enterologue/ ; dermatologie : https://www.hoppi.work/salaire-dermatologue/ ; cardiologie : https://hayot-expertise.fr/secteurs/expert-comptable-cardiologue ; gynécologie-obstétrique : https://www.gpm.fr/revenu-moyen-des-medecins-liberaux/ |
| S176 | OFS, revenus des médecins indépendants en 2019 : https://www.bfs.admin.ch/asset/fr/19584629 ; https://dam-api.bfs.admin.ch/hub/api/dam/assets/19584629/master |
| S177 | Cybersécurité, salaires en France (baromètres privés relayés) : https://cyberini.com/salaires-cybersecurite-barometre-complet-par-metier-france/ ; https://www.blog-rh.com/2026/02/metiers-cybersecurite-2026/ ; https://www.zerodaycyberacademy.com/ressources/reconversion/salaire-rssi ; https://www.zerodaycyberacademy.com/ressources/reconversion/salaire-cybersecurite-france ; https://www.cyberskill.fr/salaires-cybersecurite |
| S178 | Cybersécurité, salaires en Suisse (sites de salaires et cabinets de recrutement) : https://www.salaryexpert.com/salary/job/penetration-tester/switzerland ; https://www.salaryexpert.com/salary/job/cyber-security-consultant/switzerland ; https://www.paymetriclabs.com/ch/salaries/cloud-security-engineer ; https://www.optimaeurope.com/recruitment-blog/cybersecurity-salary-benchmarks-europe ; https://www.trustinsoda.com/salary-guides/cyber-security-switzerland ; https://fr.glassdoor.ch/Salaires/soc-analyst-i-salaire-SRCH_KO0,13.htm ; https://www.levels.fyi/t/security-analyst/locations/switzerland |
| S179 | Genève, impôt à la source, barème A0 2026 (relais) : https://www.lesfrontaliers.ch/blog/bareme-impot-frontalier-geneve-2026/ ; comparaison : https://getrates.ch/en/taxes |
| S180 | Genève, salaires des enseignants (agrégateur) : https://upreer.ch/fr/salaires/enseignant/geneve/ ; État de Genève : https://www.ge.ch/devenir-enseignant/postuler-dans-enseignement-secondaire |
| S181 | Nations unies, barème P-3 et ajustement de poste à Genève (relais) : https://www.unjobnet.org/countries/switzerland/Geneva/salary/p-3 ; https://www.unjobnet.org/advice/un-post-adjustment-explained ; https://untalent.org/contract/p-3/in-geneva |
| S182 | Notaires, revenus (relais) : https://lessentieldeleco.fr/4774-combien-gagne-un-notaire/ ; https://www.journaldunet.com/business/salaire/notaire/salaire-00858 ; Autorité de la concurrence : https://www.autoritedelaconcurrence.fr/sites/default/files/integral_texts/2023-07/23a10.pdf |
| S183 | OCDE, coins fiscaux 2025 (relais) : https://www.oecd.org/en/publications/taxing-wages-2026_3a5169ef-en/full-report/effective-tax-rates-on-labour-income-in-2025_b7bb1854.html ; https://taxfoundation.org/data/all/eu/tax-burden-on-labor-europe/ |
| S184 | Norvège, SSB : https://www.ssb.no/en/statbank/table/13848 ; https://www.ssb.no/en/statbank/table/11658 ; https://www.ssb.no/en/arbeid-og-lonn/lonn-og-arbeidskraftkostnader/statistikk/lonn ; relais : https://www.querex.no/Norwegian_Wage_Analysis_SSB.html |
| S185 | Danemark : overlæger (Danmarks Statistik, relais) : https://loen.dk/overlaege ; barèmes de l'association des médecins : https://laeger.dk/media/uphlcb15/loenoversigt-1-november-2025-staten.pdf ; salaire moyen 2024 : https://www.dst.dk/nyt/51150 |
| S186 | Pays-Bas : https://werkcv.nl/salaris ; spécialistes salariés : https://salaristabel.nl/salarisschalen/zorg/ams |
| S187 | Royaume-Uni : revenus des généralistes, NHS Digital : https://digital.nhs.uk/data-and-information/publications/statistical/gp-earnings-and-expenses-estimates ; relais du chiffre 2022/23 : https://managementinpractice.com/news/a-17-real-terms-cut-to-income-for-gp-partners-in-one-year-nhs-figures-reveal/ ; NHS Employers, hausses 2025 : https://www.nhsemployers.org/news/pay-award-announcement-2025 ; ONS, ASHE 2025 : https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/latest ; relais par profession : https://gerajobs.com/reports/uk-salary-by-occupation |
| S188 | Allemagne, Destatis, revenus des cabinets médicaux (relais) : https://www.praktischarzt.de/arzt/reinertrag-von-arztpraxen/ ; https://www.aerzteblatt.de/news/reinertrage-von-arztpraxen-deutlich-gesunken-78a8e59b-021d-4637-80bd-3cfd053e2ad0 |
| S189 | OCDE, Health at a Glance 2025, rémunération des spécialistes : https://www.oecd.org/en/publications/2025/11/health-at-a-glance-2025_a894f72e/full-report/remuneration-of-specialists_a50d2aa8.html |
| S190 | Niveaux des prix 2024 : Eurostat : https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250619-1 ; Statistik Austria : https://www.statistik.at/en/statistics/national-economy-and-public-finance/prices-and-price-indices/price-levels/-purchasing-power-parities ; SSB, comparaison européenne : https://www.ssb.no/en/priser-og-prisindekser/konsumpriser/statistikk/sammenlikning-av-prisniva-i-europa ; relais : https://www.sciencenorway.no/economy-ntb-english-society/norway-is-europes-sixth-most-expensive-country-heres-where-its-cheaper/2525052 |
| S191 | Change de référence de la BCE, moyennes 2024 et 2025 (Banque de Finlande) : https://www.suomenpankki.fi/en/statistics/interest-rates-and-exchange-rates/exchange-rates/average-annual-exchange-rates-for-the-year-2024 ; https://www.suomenpankki.fi/en/statistics/interest-rates-and-exchange-rates/exchange-rates/average-annual-exchange-rates-for-the-year-2025/ |
