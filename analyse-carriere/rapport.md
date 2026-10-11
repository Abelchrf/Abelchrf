# Classement de triplets métier × statut × pays

Sujet de référence : 24 ans, nationalité française, bac général, aucun diplôme du supérieur, quelques années d'emploi peu qualifié, aptitudes moyennes, ni réseau ni capital, sans charge de famille. Date de l'analyse : 11 octobre 2026.

Reproductibilité : tout le calcul est dans `modele.py` (entrées) et `tableaux.py` (sorties). Changer une entrée et relancer `python3 tableaux.py` régénère tous les tableaux.

## 0. Limites d'accès aux données (à lire avant les chiffres)

| Limite | Effet |
|---|---|
| La politique réseau de cet environnement bloque insee.fr, drees, bfs.admin.ch, statistiques.public.lu ; l'outil de lecture de pages échoue sur tous les hôtes. | Aucun tableau primaire n'a été ouvert. Les chiffres viennent de résumés de moteur de recherche citant ces sources, avec un risque de transcription. Les codes S renvoient aux pages citées. |
| Pas de série officielle « revenu à 40 ans » par métier et par pays. | Le médian et le P80 à 40 ans sont reconstruits à partir de moyennes, médianes tous âges ou grilles, puis ajustés à l'ancienneté réelle du sujet (entrée tardive). Chaque cellule porte sa source et la mention « est. » quand elle est ajustée. |
| Contrôle, charge, relations, sens, sécurité : aucune série officielle par métier et par pays. | Estimations normatives, guidées par DARES, DREES, INSEE, DEPP (S58, S70, S71, S07). |

## 1. Entrées déclarées avant tout calcul

### 1.1 Calendrier et trajectoire de référence

| Entrée | Valeur |
|---|---|
| Début de formation | Rentrée 2027, à 25 ans, pour les cursus Parcoursup et les concours. L'année des 24 ans est l'emploi actuel. |
| Trajectoire de référence (emploi immédiat) | 18 000 € net à 24 ans (SMIC 2026 = 1 823,03 € brut, S43) puis montée linéaire à 21 000 € à 40 ans (médiane des employés 1 800 €/mois, S08), +0,5 %/an ensuite. |
| Revenus en formation | 0 € pour les études à temps plein ; stipendiums d'externat, salaire d'interne, apprentissage (53 % puis 100 % du SMIC, S43), traitements de stagiaire selon les règles de chaque voie. Frais de scolarité élevés comptés en négatif (ostéopathie, pilote, podologie). |
| Après l'entrée | Montée linéaire du revenu de début vers le médian à 40 ans, puis +0,5 %/an réel. |

### 1.2 Poids (opinion, pas consensus chiffré)

| Critère | Poids | Appui |
|---|---|---|
| Contrôle (autonomie de temps et de méthode) | 22 | Humphrey et al. 2007 (autonomie fortement liée à la satisfaction, ρ environ 0,48, valeur citée de mémoire, non revérifiée ici) ; modèle demande-latitude de Karasek |
| Charge et rythme | 20 | Karasek ; DARES sur l'intensité et les exigences émotionnelles (S58) |
| Relations et soutien | 15 | Soutien social du modèle de Karasek-Theorell |
| Sécurité et retour à l'emploi | 15 | Sverke et al. 2002 (insécurité et satisfaction, ρ environ -0,41, cité de mémoire, non revérifié) |
| Sens et utilité perçue | 13 | Humphrey et al. 2007 (significativité de la tâche) |
| Revenu | 15 | Judge et al. 2010 : corrélation niveau de salaire et satisfaction r = 0,15 (vérifié, S57) |

### 1.3 Grilles de notation normatives (1 à 5)

| Critère | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|
| Contrôle | Fixe ses horaires et ses méthodes (libéral avec clientèle propre) | Choisit l'essentiel du temps ou de la méthode (libéral sous pression de la demande, cadre autonome, enseignant) | Méthode autonome dans des protocoles, horaires imposés mais prévisibles | Horaires imposés (roulements) et méthodes prescrites | Rythme dicté par la hiérarchie ou le flux, sans marge |
| Modificateur contrôle | Affectation géographique nationale imposée pendant des années (certifiés, police, attachés issus des IRA, DGFiP, magistrats, ICNA, militaires) : moins 1 | | | | |
| Charge | 5 moins le nombre de facteurs marqués, plancher 1 : F1 plus de 45 h/semaine ; F2 forte intensité ou exigence émotionnelle ou décisionnelle (soignants, médecins et assimilés, enseignants, cadres, police, secours, commerciaux) ; F3 nuits, week-ends ou astreintes réguliers ; F4 pénibilité physique ; F5 trajet d'au moins 1 h par sens ou découchés (frontaliers, routiers, pilotes) | | | | |
| Relations | Soutien fort et clientèle reconnaissante, peu de conflits | Bonnes relations, conflits ponctuels | Soutien présent mais tensions fréquentes ou isolement | Conflits fréquents avec le public ou faible soutien (barrière de langue comprise) | Environnement hostile |
| Sécurité | Statut protégé ou profession réglementée en pénurie structurelle (retour à l'emploi quasi certain) | Forte demande sans statut, ou expatriation avec intégration à faire | Marché moyen, cyclique, ou indépendant à demande stable | Revenus ou contrats volatils | Très précaire |
| Sens | Soin direct, enseignement, secours, justice | Utilité claire mais moins directe (paramédical technique, artisans de l'énergie, transport public, police) | Utilité indirecte (ingénierie, administration, numérique, comptabilité) | Utilité perçue faible (vente, immobilier, finance) | Perçu comme inutile |

### 1.4 Revenu

| Entrée | Valeur |
|---|---|
| Définition | Revenu net annuel après cotisations sociales salariales, avant impôt sur le revenu (convention INSEE). Limite : l'impôt n'est pas déduit, ce qui favorise relativement les pays à impôt élevé (Allemagne, Luxembourg, Québec) et la fonction publique européenne. |
| Passage brut vers net | Suisse × 0,80 (AVS, AC, LPP, AANP et prime maladie LAMal, estimé) ; médecins suisses × 0,83 à 0,85 ; Luxembourg × 0,875 ; Allemagne × 0,78 ; Québec × 0,918 (RRQ, AE, RQAP ; la santé y est financée par l'impôt, donc net surestimé) ; libéraux français × 0,94 (CSG et CRDS non déductibles, estimé). |
| Change (valeur non ajustée) | Août à décembre 2025, Banque de France, référence BCE : 1 € = 0,933 CHF = 1,619 CAD (S38). |
| Parité de pouvoir d'achat | Indices de niveau de prix Eurostat 2024, consommation des ménages, UE27 = 100 : France 111, Allemagne 109, Luxembourg 133, Suisse 174 (S36). Canada 123, estimé par le ratio OCDE des niveaux de prix 2024 (Canada 105, France 95, S37). Valeur PPA exprimée en euros au niveau de prix français. Change moyen 2024 de la BCE utilisé pour la cohérence avec les indices : 0,9526 CHF, 1,4821 CAD (valeurs connues avant cette analyse, non revérifiées ici). |
| Frontaliers | Dépense en France au change courant, avec un surcoût régional estimé (pas de série officielle) : Genevois français 10 %, nord lorrain 5 %. |
| P80 à 40 ans | Estimé par un ratio P80/médian propre au statut, compris entre 1,09 (grilles publiques et suisses) et 1,92 (avocats), ancré sur les dispersions INSEE (D9/médiane des cadres 1,94 tous âges, S08) réduites pour un âge donné, sauf mention d'une source directe. |
| Cumul 24 à 45 ans | Somme des 22 revenus annuels nets de la trajectoire, en euros PPA, sans actualisation. |
| Score revenu | Pour chacun des trois indicateurs (médian à 40 ans, P80 à 40 ans, cumul) : 1 + 4 × (ln x - ln min) / (ln max - ln min), bornes du pool. Score revenu = moyenne des trois. Bornes : médian 21 000 à 109 601 € ; P80 25 000 à 146 134 € ; cumul 412 812 à 1 487 858 €. |

### 1.5 Agrégation, paliers, élimination, frontière

| Entrée | Valeur |
|---|---|
| Score interne | Moyenne pondérée des six notes (revenu continu, autres entières). Seul le palier est affiché. |
| Paliers | S ≥ 4,2 ; A ≥ 3,6 ; B ≥ 3,0 ; C en dessous. Frontières arbitraires (fixées par la consigne). Astérisque = à moins de 0,1 d'une frontière. |
| Barrière (hors pondération) | Quatre composantes : délai d'entrée (1 + 4 × min(1, (âge d'entrée - 24) / 12)), années de revenu perdues face à l'emploi immédiat (1 + 4 × min(1, pertes / 8)), probabilité de réussite (1 + 4 × min(1, ln(1/p) / ln 50)), capital nécessaire (1 à 5). Indice = moyenne simple, utilisé seulement pour la frontière de Pareto. |
| Probabilité p | Estimation personnelle pour un candidat moyen de 24 ans, ancrée sur les taux d'admission publiés quand ils existent (PASS 33,8 % en un an, IFSI 25 000 places pour 116 000 candidats, orthophonie 3,29 %, EPSO environ 3 %, ENM environ 10,5 %, CRFPA 25 à 35 %). |
| Élimination | Un triplet est retiré s'il existe un autre triplet au moins aussi bon sur les six critères ET sur chaque composante brute de la barrière (âge d'entrée, années perdues, p, capital), strictement meilleur sur au moins un point, et si cette domination tient dans les deux scénarios IA. |
| Frontière de Pareto | Triplets non dominés sur le couple (score interne, indice de barrière). |

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

## 2. Pool (79 triplets)

| ID | Triplet | ID | Triplet |
|---|---|---|---|
| T01 | Médecin généraliste × libéral × France | T41 | Ingénieur × salarié × France |
| T02 | Médecin généraliste × salarié (centre de santé) × France | T42 | Ingénieur × salarié × Suisse (frontalier) |
| T03 | Médecin spécialiste (rang médian) × libéral × France | T43 | Ingénieur × salarié × Allemagne |
| T04 | Praticien hospitalier × statut PH (public) × France | T44 | Technicien de maintenance industrielle × salarié × France |
| T05 | Chirurgien-dentiste × libéral × France | T45 | Technicien réseaux et cybersécurité × salarié × France |
| T06 | Pharmacien adjoint × salarié × France | T46 | Actuaire × salarié × France |
| T07 | Pharmacien titulaire × indépendant × France | T47 | Électricien × salarié × France |
| T08 | Sage-femme × fonctionnaire FPH × France | T48 | Électricien × artisan × France |
| T09 | Sage-femme × libéral × France | T49 | Électricien × salarié × Suisse (frontalier) |
| T10 | Masseur-kinésithérapeute × libéral × France | T50 | Électricien × salarié × Canada (Québec) |
| T11 | Masseur-kinésithérapeute × fonctionnaire FPH × France | T51 | Plombier-chauffagiste × artisan × France |
| T12 | Infirmier × fonctionnaire FPH × France | T52 | Frigoriste (CVC) × salarié × France |
| T13 | Infirmier × libéral × France | T53 | Conducteur de train × salarié (SNCF) × France |
| T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | T54 | Conducteur de train × salarié × Suisse (résident) |
| T15 | Orthophoniste × libéral × France | T55 | Conducteur poids lourd × salarié × France |
| T16 | Orthoptiste × salarié × France | T56 | Professeur des écoles × fonctionnaire × France |
| T17 | Manipulateur radio (MERM) × fonctionnaire FPH × France | T57 | Professeur certifié × fonctionnaire × France |
| T18 | Audioprothésiste × salarié × France | T58 | Gardien de la paix × fonctionnaire × France |
| T19 | Vétérinaire × libéral × France | T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France |
| T20 | Psychologue × contractuel FPH × France | T60 | Attaché d'administration × fonctionnaire × France |
| T21 | Aide-soignant × fonctionnaire FPH × France | T61 | Inspecteur des finances publiques × fonctionnaire × France |
| T22 | Ostéopathe × libéral × France | T62 | Contrôleur des finances publiques × fonctionnaire × France |
| T23 | Infirmier × salarié × Suisse (résident) | T63 | Contrôleur aérien (ICNA) × fonctionnaire × France |
| T24 | Infirmier × salarié × Suisse (frontalier) | T64 | Administrateur UE (AD) × fonctionnaire européen × Luxembourg (résident) |
| T25 | Infirmier × salarié × Luxembourg (frontalier) | T65 | Agent contractuel UE (GF II-III) × contractuel × Luxembourg (frontalier) |
| T26 | Infirmier × salarié × Luxembourg (résident) | T66 | Sous-officier × militaire × France |
| T27 | Infirmier × salarié × Allemagne | T67 | Avocat × libéral × France |
| T28 | Infirmier × salarié × Canada (Québec) | T68 | Expert-comptable × libéral × France |
| T29 | Médecin × salarié (hôpital) × Suisse (résident) | T69 | Comptable × salarié × France |
| T30 | Médecin généraliste × indépendant × Suisse (résident) | T70 | Comptable × salarié × Luxembourg (frontalier) |
| T31 | Médecin × salarié (hôpital) × Allemagne | T71 | Magistrat × fonctionnaire × France |
| T32 | Médecin de famille × libéral (RAMQ) × Canada (Québec) | T76 | Pédicure-podologue × libéral × France |
| T33 | Aide-soignant (ASSC) × salarié × Suisse (frontalier) | T77 | Ergothérapeute × fonctionnaire FPH × France |
| T34 | Masseur-kinésithérapeute × salarié × Suisse (frontalier) | T78 | Diététicien × libéral × France |
| T35 | Développeur × salarié × France | T79 | Opticien × salarié × France |
| T36 | Développeur × indépendant (freelance) × France | T72 | Commercial B2B × salarié × France |
| T37 | Développeur × salarié × Suisse (frontalier) | T73 | Agent immobilier × indépendant (mandataire) × France |
| T38 | Développeur × salarié × Allemagne | T74 | Pilote de ligne × salarié × France |
| T39 | Développeur × salarié × Luxembourg (frontalier) | T75 | Employé commerce ou accueil (référence) × salarié × France |
| T40 | Développeur × salarié × Canada (Québec) |  |  |

## 3. Élimination

Règle : section 1.5. Douze retraits ; un triplet dominé seulement sans IA est conservé.

| Éliminé | Dominé par | Pourquoi (le dominant fait au moins aussi bien partout, et mieux sur) |
|---|---|---|
| T04 Praticien hospitalier × statut PH (public) × France | T01, T03 | T01 : contrôle, charge, relations, revenu, entrée 35 ans au lieu de 38, p 10 % au lieu de 9 % |
| T07 Pharmacien titulaire × indépendant × France | T49 | T49 : charge, revenu, entrée 28 ans au lieu de 35, années perdues 0,5 au lieu de 5,8, p 45 % au lieu de 12 %, moins de capital |
| T11 Masseur-kinésithérapeute × fonctionnaire FPH × France | T77 | T77 : charge, revenu, entrée 28 ans au lieu de 30, années perdues 3,0 au lieu de 5,0, p 8 % au lieu de 7 %, moins de capital |
| T19 Vétérinaire × libéral × France | T13 | T13 : relations, sens, revenu, entrée 30 ans au lieu de 32, années perdues 2,8 au lieu de 7,0, p 22 % au lieu de 5 % |
| T23 Infirmier × salarié × Suisse (résident) | T26 | T26 : revenu |
| T25 Infirmier × salarié × Luxembourg (frontalier) | T24 | T24 : revenu |
| T27 Infirmier × salarié × Allemagne | T23, T26, T28 | T26 : relations, sécurité, revenu, entrée 28 ans au lieu de 29, p 22 % au lieu de 12 % |
| T28 Infirmier × salarié × Canada (Québec) | T23, T26 | T26 : sécurité, revenu, entrée 28 ans au lieu de 29, p 22 % au lieu de 18 % |
| T31 Médecin × salarié (hôpital) × Allemagne | T32 | T32 : relations, revenu, p 7 % au lieu de 6 % |
| T44 Technicien de maintenance industrielle × salarié × France | T52 | T52 : sens, revenu |
| T60 Attaché d'administration × fonctionnaire × France | T61 | T61 : revenu, p 15 % au lieu de 10 % |
| T67 Avocat × libéral × France | T49 | T49 : sens, revenu, entrée 28 ans au lieu de 32, années perdues 0,5 au lieu de 6,5, p 45 % au lieu de 25 % |
| (conservé) T42 Ingénieur × salarié × Suisse (frontalier) | T37 sans IA seulement | domination perdue dans le scénario IA fort |

## 4. Tableau final (67 triplets non dominés, triés par score interne décroissant)

Notes : nom. = euros nominaux au change 2025 ; PPA = euros au niveau de prix français ; est. = valeur ajustée ou estimée ; * = à moins de 0,1 d'une frontière de palier.

### Tableau final, partie A : paliers, revenus et critères

| ID | Triplet | Palier | Méd. 40 ans nom./PPA k€ | Src méd. | P80 nom./PPA k€ | Src P80 | Cumul 24-45 PPA k€ | C | Ch | R | Se | Sn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T05 | Chirurgien-dentiste × libéral × France | S | 92 / 92 | S03,S04 | 127 / 127 | S04 (écart moyenne/médiane) ; est. | 1226 | 5 | 3 | 4 | 5 | 5 |
| T15 | Orthophoniste × libéral × France | S | 31 / 31 | S06 ; est. | 42 / 42 | est. | 478 | 5 | 5 | 4 | 5 | 5 |
| T09 | Sage-femme × libéral × France | S* | 40 / 40 | S03 | 55 / 55 | est. | 586 | 5 | 4 | 4 | 5 | 5 |
| T30 | Médecin généraliste × indépendant × Suisse (résident) | A* | 146 / 91 | S24 ; est. | 200 / 125 | est. | 1057 | 4 | 3 | 4 | 5 | 5 |
| T10 | Masseur-kinésithérapeute × libéral × France | A* | 45 / 45 | S03,S06 ; est. | 60 / 60 | est. | 659 | 5 | 3 | 4 | 5 | 5 |
| T03 | Médecin spécialiste (rang médian) × libéral × France | A* | 82 / 82 | S02 ; est. | 130 / 130 | est. | 897 | 4 | 3 | 4 | 5 | 5 |
| T01 | Médecin généraliste × libéral × France | A | 76 / 76 | S02,S05 ; est. | 100 / 100 | est. | 932 | 4 | 3 | 4 | 5 | 5 |
| T02 | Médecin généraliste × salarié (centre de santé) × France | A | 64 / 64 | S09 ; est. | 76 / 76 | est. | 829 | 3 | 4 | 4 | 5 | 5 |
| T76 | Pédicure-podologue × libéral × France | A | 33 / 33 | S69 ; est. | 45 / 45 | est. | 528 | 5 | 4 | 4 | 4 | 4 |
| T77 | Ergothérapeute × fonctionnaire FPH × France | A | 30 / 30 | S65 | 34 / 34 | est. | 515 | 3 | 5 | 4 | 5 | 5 |
| T34 | Masseur-kinésithérapeute × salarié × Suisse (frontalier) | A | 80 / 73 | S22 ; est. | 89 / 81 | est. | 1124 | 3 | 3 | 4 | 5 | 5 |
| T56 | Professeur des écoles × fonctionnaire × France | A | 27 / 27 | S11,S12,S44 | 32 / 32 | est. | 484 | 4 | 4 | 3 | 5 | 5 |
| T13 | Infirmier × libéral × France | A | 50 / 50 | S03 | 66 / 66 | est. | 825 | 4 | 2 | 4 | 5 | 5 |
| T64 | Administrateur UE (AD) × fonctionnaire européen × Luxembourg (résident) | A* | 99 / 82 | S31 ; est. | 109 / 91 | est. | 1335 | 3 | 4 | 3 | 5 | 3 |
| T41 | Ingénieur × salarié × France | A* | 45 / 45 | S16 ; est. | 56 / 56 | est. | 736 | 4 | 4 | 4 | 4 | 3 |
| T43 | Ingénieur × salarié × Allemagne | A* | 58 / 60 | S33 ; est. | 70 / 71 | est. | 927 | 4 | 4 | 3 | 4 | 3 |
| T32 | Médecin de famille × libéral (RAMQ) × Canada (Québec) | A* | 111 / 110 | est. | 148 / 146 | est. | 1298 | 3 | 2 | 3 | 5 | 5 |
| T20 | Psychologue × contractuel FPH × France | A* | 30 / 30 | est. | 35 / 35 | est. | 467 | 4 | 4 | 4 | 3 | 5 |
| T40 | Développeur × salarié × Canada (Québec) | A* | 55 / 54 | S35 ; est. | 66 / 65 | est. | 940 | 4 | 4 | 4 | 3 | 3 |
| T46 | Actuaire × salarié × France | A* | 52 / 52 | est. | 66 / 66 | est. | 795 | 4 | 4 | 4 | 4 | 2 |
| T16 | Orthoptiste × salarié × France | A* | 31 / 31 | est. | 36 / 36 | est. | 535 | 3 | 4 | 4 | 5 | 4 |
| T37 | Développeur × salarié × Suisse (frontalier) | A* | 98 / 89 | S26 | 116 / 105 | est. | 1488 | 4 | 3 | 4 | 3 | 3 |
| T42 | Ingénieur × salarié × Suisse (frontalier) | B* | 98 / 89 | S28 ; est. | 120 / 109 | est. | 1354 | 4 | 3 | 4 | 3 | 3 |
| T22 | Ostéopathe × libéral × France | B* | 32 / 32 | est. | 45 / 45 | est. | 415 | 5 | 4 | 4 | 2 | 4 |
| T29 | Médecin × salarié (hôpital) × Suisse (résident) | B* | 151 / 94 | S25 ; est. | 196 / 122 | est. | 1102 | 3 | 2 | 3 | 5 | 5 |
| T36 | Développeur × indépendant (freelance) × France | B* | 58 / 58 | S19 | 76 / 76 | S19 (TJM 15 ans et plus : 672 €) ; est. | 969 | 5 | 4 | 3 | 2 | 3 |
| T57 | Professeur certifié × fonctionnaire × France | B* | 29 / 29 | S11 | 35 / 35 | est. | 509 | 3 | 4 | 3 | 5 | 5 |
| T71 | Magistrat × fonctionnaire × France | B* | 52 / 52 | est. | 60 / 60 | est. | 711 | 3 | 3 | 3 | 5 | 5 |
| T35 | Développeur × salarié × France | B* | 40 / 40 | S17 ; est. | 51 / 51 | est. | 745 | 4 | 4 | 4 | 3 | 3 |
| T18 | Audioprothésiste × salarié × France | B* | 36 / 36 | S21 | 45 / 45 | est. | 604 | 3 | 4 | 4 | 4 | 4 |
| T14 | Infirmier anesthésiste (IADE) × fonctionnaire FPH × France | B | 42 / 42 | S09 ; est. | 48 / 48 | est. | 699 | 3 | 3 | 3 | 5 | 5 |
| T38 | Développeur × salarié × Allemagne | B | 57 / 58 | S33 | 70 / 71 | est. | 995 | 4 | 4 | 3 | 3 | 3 |
| T68 | Expert-comptable × libéral × France | B | 65 / 65 | S20 ; est. | 103 / 103 | est. | 946 | 4 | 3 | 3 | 4 | 3 |
| T78 | Diététicien × libéral × France | B | 24 / 24 | est. | 32 / 32 | est. | 413 | 4 | 5 | 4 | 2 | 4 |
| T39 | Développeur × salarié × Luxembourg (frontalier) | B | 66 / 62 | S30 ; est. | 83 / 79 | est. | 1075 | 4 | 3 | 4 | 3 | 3 |
| T50 | Électricien × salarié × Canada (Québec) | B | 48 / 48 | S35 ; est. | 57 / 56 | est. | 832 | 3 | 4 | 3 | 4 | 4 |
| T08 | Sage-femme × fonctionnaire FPH × France | B | 40 / 40 | S10 | 45 / 45 | est. | 571 | 3 | 3 | 3 | 5 | 5 |
| T62 | Contrôleur des finances publiques × fonctionnaire × France | B | 31 / 31 | S66 ; est. | 36 / 36 | est. | 603 | 2 | 5 | 3 | 5 | 3 |
| T17 | Manipulateur radio (MERM) × fonctionnaire FPH × France | B | 34 / 34 | S09 ; est. | 38 / 38 | est. | 576 | 2 | 4 | 3 | 5 | 4 |
| T47 | Électricien × salarié × France | B | 26 / 26 | S08 ; est. | 31 / 31 | est. | 514 | 3 | 4 | 3 | 4 | 4 |
| T63 | Contrôleur aérien (ICNA) × fonctionnaire × France | B | 66 / 66 | S68 ; est. | 78 / 78 | est. | 1105 | 1 | 3 | 4 | 5 | 4 |
| T26 | Infirmier × salarié × Luxembourg (résident) | B | 75 / 63 | S29 ; est. | 91 / 76 | est. | 1083 | 2 | 2 | 3 | 5 | 5 |
| T45 | Technicien réseaux et cybersécurité × salarié × France | B | 34 / 34 | S08 ; est. | 42 / 42 | est. | 634 | 3 | 4 | 3 | 4 | 3 |
| T49 | Électricien × salarié × Suisse (frontalier) | B | 67 / 61 | S27,S28 ; est. | 78 / 71 | est. | 1103 | 3 | 3 | 3 | 3 | 4 |
| T69 | Comptable × salarié × France | B | 29 / 29 | S08 ; est. | 34 / 34 | est. | 554 | 3 | 5 | 3 | 3 | 3 |
| T61 | Inspecteur des finances publiques × fonctionnaire × France | B | 38 / 38 | S67 ; est. | 48 / 48 | est. | 646 | 2 | 4 | 3 | 5 | 3 |
| T59 | Sapeur-pompier professionnel × fonctionnaire territorial × France | B | 31 / 31 | est. | 34 / 34 | est. | 592 | 2 | 2 | 4 | 5 | 5 |
| T24 | Infirmier × salarié × Suisse (frontalier) | B | 83 / 76 | S22,S23,S64 ; est. | 96 / 87 | S64 haut de fourchette ; est. | 1312 | 2 | 1 | 3 | 5 | 5 |
| T52 | Frigoriste (CVC) × salarié × France | B | 30 / 30 | S08 ; est. | 36 / 36 | est. | 570 | 3 | 3 | 3 | 4 | 4 |
| T70 | Comptable × salarié × Luxembourg (frontalier) | B | 54 / 52 | S30 ; est. | 66 / 62 | est. | 915 | 3 | 4 | 3 | 3 | 2 |
| T54 | Conducteur de train × salarié × Suisse (résident) | B* | 78 / 49 | S22,S55 ; est. | 87 / 55 | est. | 958 | 2 | 3 | 3 | 4 | 4 |
| T72 | Commercial B2B × salarié × France | B* | 38 / 38 | S08 ; est. | 55 / 55 | est. | 706 | 4 | 3 | 3 | 3 | 2 |
| T48 | Électricien × artisan × France | B* | 31 / 31 | est. | 45 / 45 | est. | 581 | 4 | 2 | 3 | 3 | 4 |
| T51 | Plombier-chauffagiste × artisan × France | B* | 31 / 31 | est. | 45 / 45 | est. | 581 | 4 | 2 | 3 | 3 | 4 |
| T12 | Infirmier × fonctionnaire FPH × France | B* | 35 / 35 | S09,S10 | 40 / 40 | est. | 600 | 2 | 2 | 3 | 5 | 5 |
| T53 | Conducteur de train × salarié (SNCF) × France | C* | 37 / 37 | S15 ; est. | 46 / 46 | est. | 685 | 2 | 3 | 3 | 4 | 4 |
| T65 | Agent contractuel UE (GF II-III) × contractuel × Luxembourg (frontalier) | C* | 46 / 44 | S31 ; est. | 57 / 54 | est. | 827 | 2 | 4 | 3 | 3 | 3 |
| T79 | Opticien × salarié × France | C* | 27 / 27 | S08 ; est. | 32 / 32 | est. | 523 | 2 | 4 | 3 | 4 | 3 |
| T06 | Pharmacien adjoint × salarié × France | C* | 40 / 40 | est. | 48 / 48 | est. | 599 | 2 | 2 | 3 | 5 | 4 |
| T74 | Pilote de ligne × salarié × France | C | 84 / 84 | est. | 110 / 110 | est. | 1183 | 2 | 2 | 3 | 3 | 3 |
| T21 | Aide-soignant × fonctionnaire FPH × France | C | 27 / 27 | S12,S14 | 30 / 30 | est. | 523 | 1 | 2 | 3 | 5 | 5 |
| T66 | Sous-officier × militaire × France | C | 33 / 33 | est. | 40 / 40 | est. | 622 | 1 | 2 | 4 | 4 | 4 |
| T33 | Aide-soignant (ASSC) × salarié × Suisse (frontalier) | C | 61 / 56 | S22 ; est. | 67 / 61 | est. | 1084 | 1 | 1 | 3 | 4 | 5 |
| T73 | Agent immobilier × indépendant (mandataire) × France | C | 24 / 24 | est. | 45 / 45 | est. | 465 | 4 | 3 | 3 | 1 | 2 |
| T58 | Gardien de la paix × fonctionnaire × France | C | 34 / 34 | S13 | 40 / 40 | est. | 665 | 1 | 2 | 2 | 5 | 4 |
| T75 | Employé commerce ou accueil (référence) × salarié × France | C | 21 / 21 | S08,S43 | 25 / 25 | est. | 438 | 2 | 3 | 2 | 3 | 2 |
| T55 | Conducteur poids lourd × salarié × France | C | 26 / 26 | S08 ; est. | 31 / 31 | est. | 539 | 2 | 1 | 2 | 4 | 3 |

### Tableau final, partie B : barrière d'entrée et risque IA (même ordre)

| ID | Entrée | Formation et financement | Sélectivité | Années perdues | Indice barrière | IA : exposition, palier si IA fort |
|---|---|---|---|---|---|---|
| T05 | 31 ans | Licence portail santé + 5 ans ; prêt d'installation après collaboration | Places d'odontologie rares ; p estimé 5 % | 5,7 | 3,56 | faible, S |
| T15 | 30 ans | CFUO 5 ans (grade master) | 2025 : 3,29 % d'admis ; p estimé 3 % | 5,0 | 3,27 | faible, S |
| T09 | 31 ans | Licence portail santé + 5 ans (maïeutique en 6 ans) | p estimé 16 % | 5,8 | 3,02 | faible, S* |
| T30 | 38 ans | Médecine en France + 3 ans en établissement suisse (admission LAMal) | p estimé 7 % | 5,4 | 3,85 | faible, A* |
| T10 | 30 ans | Licence portail santé ou STAPS accès kiné + IFMK 4 ans ; IFMK privés 5 à 9 k€/an | Très sélectif ; p estimé 7 % | 5,0 | 3,30 | faible, A* |
| T03 | 38 ans | Idem T01 + internat 5 ans + clinicat 2 ans | Spécialité selon rang EDN ; p estimé 9 % | 5,4 | 3,54 | faible, A* |
| T01 | 35 ans | Licence portail santé (rentrée 2027) puis 9 ans ; internat rémunéré ; bourses | 2 candidatures ; PASS 2024 : 33,8 % admis en 1 an ; p estimé 10 % | 5,4 | 3,43 | faible, A |
| T02 | 35 ans | Idem T01 | p estimé 10 % | 5,4 | 3,43 | faible, A |
| T76 | 28 ans | DE 3 ans (instituts surtout privés, 6 à 8 k€/an) | p estimé 25 % | 3,8 | 2,66 | faible, A |
| T77 | 28 ans | DE 3 ans (Parcoursup ou après année santé) | Sélectif ; p estimé 8 % | 3,0 | 2,60 | faible, A |
| T34 | 30 ans | Kiné en France + reconnaissance | p estimé 6 % | 5,0 | 3,34 | faible, A |
| T56 | 30 ans | Licence puis CRPE à bac+3 + 2 ans de master rémunérés (1 400 puis 1 800 € net) | p estimé 40 % | 3,1 | 2,37 | moyenne, A |
| T13 | 30 ans | IFSI + 24 mois d'exercice salarié avant installation | p estimé 22 % | 2,8 | 2,49 | faible, A |
| T64 | 29 ans | Licence + concours EPSO AD5 (C1 + B2) | 2026 : environ 3 % de réussite ; p estimé 3 % | 3,0 | 2,94 | moyenne, A* |
| T41 | 31 ans | BUT puis école d'ingénieurs en apprentissage (29 ans révolus ; dérogation jusqu'à 35 ans en enchaînement) | p estimé 30 % | 1,2 | 2,04 | moyenne, B* |
| T43 | 31 ans | Idem T41 + allemand | p estimé 15 % | 1,2 | 2,47 | moyenne, B |
| T32 | 35 ans | Médecine en France (DES MG) + ARM + immigration | p estimé 7 % | 5,4 | 3,52 | faible, A* |
| T20 | 30 ans | Licence + master sélectif | p estimé 20 % | 5,0 | 2,79 | faible, A* |
| T40 | 29 ans | Idem T35 + immigration | p estimé 25 % | 0,5 | 2,08 | élevée, B |
| T46 | 30 ans | Licence de mathématiques + master d'actuariat | p estimé 6 % | 4,0 | 2,98 | élevée, B |
| T16 | 28 ans | Certificat de capacité 3 ans | Sélectif ; p estimé 10 % | 3,0 | 2,55 | moyenne, B |
| T37 | 30 ans | Idem T35 + 3 ans d'expérience ; permis G | p estimé 25 % | 0,5 | 2,16 | élevée, B |
| T42 | 31 ans | Idem T41 + permis G | p estimé 20 % | 1,2 | 2,39 | moyenne, B |
| T22 | 30 ans | École privée 5 ans, 7 à 10 k€/an (prêt) | Peu sélectif ; marché saturé ; p estimé 65 % | 7,2 | 3,25 | faible, B* |
| T29 | 35 ans | Médecine en France + autorisation MEBEKO | p estimé 8 % | 5,4 | 3,49 | faible, B* |
| T36 | 32 ans | Idem T35 + 5 ans salarié | p estimé 30 % | 0,5 | 2,03 | élevée, B |
| T57 | 30 ans | Licence puis CAPES à bac+3 + 2 ans rémunérés | p estimé 35 % | 3,1 | 2,41 | moyenne, B* |
| T71 | 33 ans | Licence + M1 + concours ENM + 31 mois rémunérés | Environ 10,5 % de réussite ; p estimé 8 % | 5,0 | 3,27 | faible, B* |
| T35 | 27 ans | BTS SIO ou BUT en alternance (rémunéré) | Marché junior tendu 2024-2026 ; p estimé 45 % | 0,5 | 1,51 | élevée, B |
| T18 | 28 ans | DE 3 ans | Peu de places ; p estimé 10 % | 3,0 | 2,55 | faible, B* |
| T14 | 32 ans | IFSI + 2 ans d'exercice + concours + 2 ans (promotion professionnelle rémunérée) | p estimé 9 % | 2,8 | 2,88 | faible, B |
| T38 | 28 ans | Idem T35 + allemand | p estimé 20 % | 0,5 | 2,05 | élevée, B |
| T68 | 33 ans | DCG + DSCG en alternance + stage 3 ans + DEC | p estimé 20 % | 0,6 | 2,23 | moyenne, B |
| T78 | 27 ans | BTS diététique ou BUT 2 à 3 ans | p estimé 50 % | 2,0 | 1,93 | moyenne, B |
| T39 | 29 ans | Idem T35 + mobilité | p estimé 25 % | 0,5 | 2,08 | élevée, B* |
| T50 | 28 ans | Idem T47 + certificat CCQ + immigration | p estimé 35 % | 0,5 | 1,91 | faible, B |
| T08 | 31 ans | Licence portail santé + 5 ans (maïeutique en 6 ans) | p estimé 18 % | 5,8 | 2,99 | faible, B |
| T62 | 26 ans | Concours de niveau bac + formation rémunérée | p estimé 30 % | 0,0 | 1,47 | moyenne, B |
| T17 | 28 ans | DE ou DTS 3 ans | p estimé 30 % | 3,0 | 2,27 | faible, B |
| T47 | 26 ans | Titre professionnel ou CAP adulte en moins d'un an (France Travail, CPF) | p estimé 85 % | 0,5 | 1,26 | faible, B |
| T63 | 30 ans | Concours externe : moins de 26 ans au 1er janvier, niveau CPGE ; formation rémunérée | Fenêtre 2027-2028 seulement ; p estimé 1 % | 0,0 | 2,50 | faible, B |
| T26 | 28 ans | IFSI + autorisation d'exercer (diplôme exempté de reconnaissance) | p estimé 22 % | 2,8 | 2,32 | faible, B |
| T45 | 27 ans | BTS SIO ou BUT R&T en alternance | p estimé 60 % | 0,5 | 1,44 | moyenne, B* |
| T49 | 28 ans | Idem T47 + reconnaissance SEFRI ; permis G | p estimé 45 % | 0,5 | 1,84 | faible, B |
| T69 | 27 ans | BTS CG en alternance | p estimé 75 % | 0,5 | 1,38 | élevée, C |
| T61 | 29 ans | Licence + concours + ENFiP rémunérée | p estimé 15 % | 3,0 | 2,53 | moyenne, B |
| T59 | 27 ans | Volontariat + concours + recrutement par un SDIS | p estimé 8 % | 0,0 | 1,90 | faible, B |
| T24 | 28 ans | IFSI + reconnaissance + permis G | p estimé 22 % | 2,8 | 2,32 | faible, B |
| T52 | 27 ans | CAP ou BTS froid en alternance | p estimé 70 % | 0,5 | 1,40 | faible, B |
| T70 | 27 ans | BTS CG + emploi au Luxembourg | p estimé 45 % | 0,5 | 1,51 | élevée, C |
| T54 | 26 ans | Formation 14 à 16 mois rémunérée ; résidence près du dépôt | p estimé 15 % | 0,0 | 1,90 | faible, B* |
| T72 | 27 ans | Embauche directe ou BTS NDRC en alternance | p estimé 80 % | 0,5 | 1,36 | moyenne, C |
| T48 | 31 ans | Idem T47 + 5 ans salarié + création (outillage, véhicule) | p estimé 45 % (survie à 5 ans) | 0,5 | 2,34 | faible, B* |
| T51 | 31 ans | CAP adulte + 5 ans salarié + création | p estimé 45 % | 0,5 | 2,34 | faible, B* |
| T12 | 28 ans | IFSI 3 ans (Parcoursup, ou voie FPC avec 3 ans de cotisations ; Transition Pro possible) | 2025 : 116 000 candidats pour 25 000 places ; p estimé 25 % | 2,8 | 2,29 | faible, B* |
| T53 | 26 ans | Recrutement + 12 mois de formation rémunérée | Tests psychotechniques ; p estimé 30 % | 0,0 | 1,47 | faible, C* |
| T65 | 26 ans | CAST permanent (bac + 3 ans d'expérience, C1 + B2), inscription continue | p estimé 15 % | 0,0 | 1,65 | élevée, C |
| T79 | 27 ans | BTS OL en alternance | p estimé 70 % | 0,5 | 1,40 | faible, C* |
| T06 | 31 ans | Licence portail santé + 5 ans | Places de pharmacie souvent non pourvues ; p estimé 25 % | 5,8 | 2,92 | faible, C* |
| T74 | 28 ans | ATPL intégré (environ 100 k€) ou EPL (condition d'âge non vérifiée) | p estimé 10 % | 8,5 | 3,92 | faible, C |
| T21 | 26 ans | IFAS 1 an (apprentissage possible) | p estimé 75 % | 1,0 | 1,37 | faible, C |
| T66 | 26 ans | École de sous-officiers 8 mois (moins de 32 ans, bac) | p estimé 70 % | 0,0 | 1,26 | faible, C |
| T33 | 26 ans | IFAS + reconnaissance Croix-Rouge suisse | p estimé 55 % | 1,0 | 1,44 | faible, C |
| T73 | 26 ans | Statut d'agent commercial, formation courte | p estimé 50 % (survie) | 0,5 | 1,40 | moyenne, C |
| T58 | 26 ans | Concours (bac) + 12 mois rémunérés (1 570 à 1 617 € net) | p estimé 30 % | 0,0 | 1,47 | faible, C |
| T75 | 24 ans | Aucune | p 100 % | 0,0 | 1,00 | moyenne, C |
| T55 | 25 ans | Permis C/CE + FIMO (3 mois, financés) | p estimé 85 % | 0,0 | 1,12 | moyenne, C |

## 5. Frontière de Pareto

| Rang barrière | ID | Triplet | Indice barrière | Palier | Gain en montant d'un cran |
|---|---|---|---|---|---|
| 1 | T75 | Employé commerce ou accueil (référence) × salarié × France | 1,00 | C |  |
| 2 | T66 | Sous-officier × militaire × France | 1,26 | C | +0,45 point de score pour +0,26 de barrière |
| 3 | T47 | Électricien × salarié × France | 1,26 | B | +0,60 point de score pour +0,01 de barrière |
| 4 | T62 | Contrôleur des finances publiques × fonctionnaire × France | 1,47 | B | +0,06 point de score pour +0,21 de barrière |
| 5 | T35 | Développeur × salarié × France | 1,51 | B* | +0,20 point de score pour +0,04 de barrière |
| 6 | T36 | Développeur × indépendant (freelance) × France | 2,03 | B* | +0,05 point de score pour +0,52 de barrière |
| 7 | T41 | Ingénieur × salarié × France | 2,04 | A* | +0,12 point de score pour +0,01 de barrière |
| 8 | T56 | Professeur des écoles × fonctionnaire × France | 2,37 | A | +0,07 point de score pour +0,33 de barrière |
| 9 | T77 | Ergothérapeute × fonctionnaire FPH × France | 2,60 | A | +0,16 point de score pour +0,23 de barrière |
| 10 | T76 | Pédicure-podologue × libéral × France | 2,66 | A | +0,01 point de score pour +0,06 de barrière |
| 11 | T09 | Sage-femme × libéral × France | 3,02 | S* | +0,34 point de score pour +0,36 de barrière |
| 12 | T15 | Orthophoniste × libéral × France | 3,27 | S | +0,11 point de score pour +0,25 de barrière |
| 13 | T05 | Chirurgien-dentiste × libéral × France | 3,56 | S | +0,00 point de score pour +0,29 de barrière |

### À moins de 0,1 d'une frontière de palier

T09 (S), T30 (A), T10 (A), T03 (A), T64 (A), T41 (A), T43 (A), T32 (A), T20 (A), T40 (A), T46 (A), T16 (A), T37 (A), T42 (B), T22 (B), T29 (B), T36 (B), T57 (B), T71 (B), T35 (B), T18 (B), T25 (B), T54 (B), T72 (B), T67 (B), T48 (B), T51 (B), T12 (B), T28 (C), T07 (C), T53 (C), T44 (C), T65 (C), T79 (C), T06 (C)

### Égalités (écart de score interne inférieur à 0,005)

T05 = T15, T64 = T41, T43 = T32, T46 = T16, T46 = T37, T16 = T37, T29 = T36, T29 = T57, T36 = T57, T35 = T18, T14 = T38, T14 = T68, T38 = T68, T68 = T78, T39 = T50, T31 = T08, T17 = T47, T45 = T49, T24 = T52, T48 = T51

### Sensibilité des paliers aux poids (opinion, pas consensus)

| Variante | Palier S | Nombre S/A/B/C |
|---|---|---|
| Base (22/20/15/15/13/15) | T05, T09, T15 | 3/20/40/16 |
| Poids égaux | T05, T09, T15, T30 | 4/19/43/13 |
| Revenu 30 (17/15/13/13/12/30) | T05, T30 | 2/14/41/22 |

### Marge des triplets S au-dessus de 4,2

- T05 : marge 0,18 ; une note de moins sur contrôle, charge le fait passer en A.
- T15 : marge 0,18 ; une note de moins sur contrôle, charge le fait passer en A.
- T09 : marge 0,07 ; une note de moins sur contrôle, charge, relations, sécurité, sens le fait passer en A.

## 6. Conclusion : palier S

| Triplet | En une phrase |
|---|---|
| T05 Chirurgien-dentiste × libéral × France | Meilleur score interne du pool grâce au contrôle maximal et au revenu le plus élevé de France à 40 ans (92 k€ médian), payé par moins de 5 % de chances d'accès estimées et 5,7 années de revenu perdues. |
| T15 Orthophoniste × libéral × France | À égalité avec le dentiste (écart inférieur à 0,005), porté par une charge légère, une pénurie qui garantit l'emploi et un sens maximal, malgré un revenu modeste (31 k€) et 3,29 % d'admis en 2025. |
| T09 Sage-femme × libéral × France | S de justesse (marge 0,07, moins de 0,1 de la frontière) mais barrière la plus basse des trois (entrée à 31 ans, p estimé 16 %), avec 40 k€ médians à 40 ans. |

Lecture : les trois S sont des professions de santé libérales françaises, parce que les poids (contrôle 22, charge 20) récompensent l'autonomie bien plus que le revenu. Aucun triplet hors de France n'atteint S avec ces poids ; le médecin généraliste indépendant en Suisse (T30) passe en S avec des poids égaux, et seuls T05 et T30 restent S si le revenu pèse 30. Une seule note de moins en contrôle ou en charge fait tomber T05 et T15 en A ; n'importe quelle note de moins fait tomber T09.

## 7. Ce qui est vérifiable et ce qui est mon opinion

| Élément | Statut |
|---|---|
| Revenus moyens ou médians cités (codes S), grilles de rémunération, indices de prix Eurostat, taux d'admission, règles d'âge et de tentatives | Vérifiable, mais lu ici à travers des résumés de moteur de recherche : à contrôler dans les tableaux primaires avant toute décision. |
| Conversion du brut au net, surcoûts régionaux des frontaliers, ratios P80, trajectoires de revenu, frais de scolarité | Hypothèses déclarées (mon choix), modifiables dans `modele.py`. |
| Notes de contrôle, charge, relations, sécurité, sens | Estimations normatives (mon jugement), guidées par DARES, DREES, INSEE, DEPP. |
| Poids des critères | Opinion fondée sur des tailles d'effet publiées ; aucun consensus chiffré. |
| Probabilités de réussite p | Estimations personnelles ancrées sur des taux d'admission publiés ; ne tiennent pas compte d'une préparation intensive ni d'aptitudes réelles différentes de la moyenne. |
| Scénarios IA | Bornes de scénario, poids de preuve faible ; ne sont pas des prévisions. |
| Seuils de paliers et frontières | Arbitraires (fixés par la consigne) ; 35 triplets sur 79 sont à moins de 0,1 d'une frontière. |

Règle de révision : un palier ne changera que sur une donnée nouvelle (par exemple un tableau primaire qui contredit une cellule) ou une incohérence démontrée dans les entrées ci-dessus, jamais sur une simple contestation.

## 8. Cellules revenu manquantes ou estimées

- Sans source directe, estimées sur grille, structure ou proxy : T06 pharmacien adjoint, T16 orthoptiste, T20 psychologue, T22 ostéopathe, T32 médecin de famille au Québec, T46 actuaire, T48 et T51 artisans du bâtiment, T59 sapeur-pompier, T66 sous-officier, T71 magistrat, T73 agent immobilier, T74 pilote, T78 diététicien.
- Sourcées mais ajustées (ancienneté du sujet, passage au net, proxy de branche) : toutes les autres cellules marquées « est. » dans le tableau final.
- Tous les P80 sont estimés par ratio, sauf T23, T24 (haut de fourchette HUG), T28 (troisième quartile québécois), T36 (TJM au-delà de 15 ans) et T67 (dispersion des avocats).
- Revenus non récupérés qui amélioreraient le plus la fiabilité : tableau INSEE des non-salariés 2024 par activité (médecine générale, dentaires, BTP, vétérinaires), jeu DREES 2026 des libéraux non médecins (orthophonistes, orthoptistes, podologues), tableau OFS T17 de l'ESS 2024 par profession, grille FHL par ancienneté, données RAMQ des médecins de famille.

## 9. Sources

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
| S36 | Eurostat, niveaux de prix 2024 (relais) : https://mail.actmedia.eu/daily/eurostat-household-consumption-price-levels-in-2024/114449 ; https://monstat.org/uploads/files/cijene/Komparativne/2/Comparative%20price%20levels%20in%202024.pdf |
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
