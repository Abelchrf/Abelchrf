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
