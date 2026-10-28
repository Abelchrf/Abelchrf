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
