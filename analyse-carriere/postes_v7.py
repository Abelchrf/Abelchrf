# -*- coding: utf-8 -*-
"""Version 7 (29 octobre 2026) : catalogue de postes precis et triplets du classement 1 (France et Suisse).

Regles declarees en section 1.15 du rapport :
- chaque triplet porte le nom exact du poste et son code CITP-08 a 4 chiffres (OIT) ;
- les triplets francais et suisses de la v6 sont repris avec leurs notes, facteurs, ancrages et cellules
  revenu (code v6 dans le champ src), sauf les changements declares ici ;
- les categories larges de la v6 sont remplacees par des postes : « medecin specialiste (rang median) »
  (T03) par chaque specialite dont un revenu publie a ete trouve ; « ingenieur cybersecurite (hors SOC) »
  (T83, T89) par pentesteur, ingenieur securite cloud, consultant GRC et RSSI ;
- Suisse « frontalier inclus » : chaque poste salarie suisse existe en resident et en frontalier ; les
  independants (medecins, dentistes) restent residents.

Les notes des postes nouveaux suivent la grille normative 1.3 et sont estimees (statut E) sauf ancrage ;
chaque ecart a la note du poste d'origine est justifie dans le champ just.
"""
import math

import eurofound as EU
import modele as M6
from revenus import LAMAL, NET_BNC, MED_MOY_LIB, P80_LIB, REV, p80_ln

V6 = {t["id"]: t for t in M6.T}

# Codes CITP-08 corriges ou precises (v6 : code du metier ; v7 : code du poste).
CITP_POSTE = {"T35": "2512", "T36": "2512", "T80": "2522", "T81": "2522", "T82": "2522", "T86": "2522",
              "T84": "2529", "T85": "2521"}

# --- Reprise des triplets v6 de France et de Suisse : nom exact du poste et statut ----------------------
REPRISE = {
    "T01": ("Médecin généraliste", "libéral"),
    "T02": ("Médecin généraliste", "salarié (centre de santé)"),
    "T04": ("Praticien hospitalier (spécialiste, grille commune à toutes les spécialités)", "statut PH (public)"),
    "T05": ("Chirurgien-dentiste omnipraticien", "libéral"),
    "T06": ("Pharmacien adjoint d'officine", "salarié"),
    "T07": ("Pharmacien titulaire d'officine", "indépendant"),
    "T08": ("Sage-femme hospitalière", "fonctionnaire FPH"),
    "T09": ("Sage-femme", "libéral"),
    "T10": ("Masseur-kinésithérapeute", "libéral"),
    "T11": ("Masseur-kinésithérapeute hospitalier", "fonctionnaire FPH"),
    "T12": ("Infirmier en soins généraux (IDE) hospitalier", "fonctionnaire FPH"),
    "T13": ("Infirmier en soins généraux (IDE)", "libéral"),
    "T14": ("Infirmier anesthésiste (IADE)", "fonctionnaire FPH"),
    "T15": ("Orthophoniste", "libéral"),
    "T16": ("Orthoptiste", "salarié"),
    "T17": ("Manipulateur en électroradiologie médicale (MERM)", "fonctionnaire FPH"),
    "T18": ("Audioprothésiste", "salarié"),
    "T19": ("Vétérinaire praticien", "libéral"),
    "T20": ("Psychologue hospitalier", "contractuel FPH"),
    "T21": ("Aide-soignant hospitalier", "fonctionnaire FPH"),
    "T22": ("Ostéopathe", "libéral"),
    "T76": ("Pédicure-podologue", "libéral"),
    "T77": ("Ergothérapeute hospitalier", "fonctionnaire FPH"),
    "T78": ("Diététicien", "libéral"),
    "T79": ("Opticien-lunetier", "salarié"),
    "T35": ("Développeur logiciel (études et développement)", "salarié"),
    "T36": ("Développeur logiciel", "indépendant (freelance)"),
    "T80": ("Ingénieur cloud DevOps", "salarié"),
    "T81": ("Ingénieur cloud DevOps", "indépendant (freelance)"),
    "T84": ("Analyste SOC (niveaux 1 et 2)", "salarié"),
    "T85": ("Data engineer (ingénieur des données)", "salarié"),
    "T41": ("Ingénieur méthodes et industrialisation", "salarié"),
    "T44": ("Technicien de maintenance industrielle", "salarié"),
    "T45": ("Technicien systèmes et réseaux", "salarié"),
    "T46": ("Actuaire", "salarié"),
    "T47": ("Électricien du bâtiment", "salarié"),
    "T48": ("Électricien du bâtiment", "artisan"),
    "T51": ("Plombier-chauffagiste", "artisan"),
    "T52": ("Frigoriste (froid et climatisation)", "salarié"),
    "T53": ("Conducteur de train", "salarié (SNCF)"),
    "T55": ("Conducteur routier poids lourd", "salarié"),
    "T56": ("Professeur des écoles", "fonctionnaire"),
    "T57": ("Professeur certifié (collège et lycée)", "fonctionnaire"),
    "T58": ("Gardien de la paix", "fonctionnaire"),
    "T59": ("Sapeur-pompier professionnel", "fonctionnaire territorial"),
    "T60": ("Attaché d'administration de l'État", "fonctionnaire"),
    "T61": ("Inspecteur des finances publiques", "fonctionnaire"),
    "T62": ("Contrôleur des finances publiques", "fonctionnaire"),
    "T63": ("Contrôleur aérien (ICNA)", "fonctionnaire"),
    "T66": ("Sous-officier de l'armée de Terre", "militaire"),
    "T67": ("Avocat", "libéral"),
    "T68": ("Expert-comptable", "libéral"),
    "T69": ("Comptable", "salarié"),
    "T71": ("Magistrat de l'ordre judiciaire", "fonctionnaire"),
    "T72": ("Attaché commercial B2B", "salarié"),
    "T73": ("Agent immobilier", "indépendant (mandataire)"),
    "T74": ("Pilote de ligne", "salarié"),
    "T75": ("Vendeur en magasin (référence)", "salarié"),
    # Suisse
    "T23": ("Infirmier en soins généraux hospitalier", "salarié"),
    "T24": ("Infirmier en soins généraux hospitalier", "salarié"),
    "T29": ("Médecin hospitalier (chef de clinique à médecin adjoint)", "salarié (hôpital)"),
    "T30": ("Médecin de famille (médecine interne générale)", "indépendant"),
    "T33": ("Assistant en soins et santé communautaire (ASSC)", "salarié"),
    "T34": ("Physiothérapeute", "salarié"),
    "T37": ("Développeur logiciel", "salarié"),
    "T42": ("Ingénieur méthodes et industrialisation", "salarié"),
    "T49": ("Électricien de montage (CFC)", "salarié"),
    "T54": ("Mécanicien de locomotive (CFF)", "salarié"),
    "T82": ("Ingénieur cloud DevOps", "salarié"),
    "T86": ("Ingénieur cloud DevOps", "salarié"),
    "T91": ("Médecin-dentiste", "indépendant"),
}
# Copies suisses (resident ou frontalier du meme poste salarie) : nouvel identifiant -> (v6 d'origine, residence).
COPIES_CH = {"T29": "FR-GE", "T33": "CH", "T34": "CH", "T37": "CH", "T42": "CH", "T49": "CH"}

LIBERAUX = {"libéral", "indépendant", "artisan", "indépendant (freelance)", "indépendant (mandataire)"}


def _pays_resid(t6):
    if t6["pays"] == "France":
        return "FR", "FR"
    return "CH", t6["resid"]


def _fiscal(pays, statut):
    lib = statut in LIBERAUX
    if pays == "FR":
        return "liberal_fr" if lib else "salarie_fr"
    return "independant_ch" if lib else "salarie_ch"


def _cellule(src):
    r = REV[src]
    return dict(med=r["med"], p80=r["p80"], src_med=r["src_med"], src_p80=r["src_p80"], fiab=r["fiab"],
                h=r["h"], q=r["q"], etp=r["etp"], etp_ok=r["etp_ok"])


R1 = []


def ajouter(**kw):
    kw.setdefault("anc_extra", [])
    kw.setdefault("anc_exclus", [])
    kw.setdefault("anc_partiel", [])
    kw.setdefault("langue", 0)
    kw.setdefault("just", "")
    kw.setdefault("exonere", False)
    kw["fx"] = set(kw["fx"].split()) if isinstance(kw["fx"], str) else set(kw["fx"])
    R1.append(kw)


def reprise(src, resid=None, ident=None, **changements):
    t6 = V6[src]
    poste, statut = REPRISE[src]
    pays, res = _pays_resid(t6)
    if resid is not None:
        res = resid
    groupe, ep, it = EU.groupe_de(src)
    fx = set(EU.FACTEURS[src].split())
    if pays == "CH":  # F5 (trajet) : informatif, suit la residence
        fx.discard("F5")
        if res == "FR-GE":
            fx.add("F5")
    d = dict(id=ident or src, src=src, poste=poste, citp=CITP_POSTE.get(src, EU.CITP[src][0]),
             niveau=EU.CITP[src][1], statut=statut, pays=pays, resid=res, cur=t6["cur"],
             C=t6["C"], R=t6["R"], Se=t6["Se"], fx=fx, EP=ep, IT=it, groupe=groupe, ia=t6["ia"], L=t6["L"],
             fiscal=_fiscal(pays, statut), **_cellule(src))
    d.update(changements)
    ajouter(**d)


for _src in REPRISE:
    if _src == "T01":
        continue  # repris plus bas avec la source commune des specialites
    reprise(_src)
for _src, _res in COPIES_CH.items():
    reprise(_src, resid=_res, ident=_src + ("f" if _res == "FR-GE" else "r"))

# ---------------------------------------------------------------------------
# Medecins liberaux francais : une seule source pour toutes les specialites (CARMF 2023)
# ---------------------------------------------------------------------------
# Revenu net d'activite independante moyen 2023 (nouvelle methode de la CARMF), x 0,96 (CSG et CRDS non
# deductibles) x 0,85 (mediane = moyenne x 0,85, regle 1.4) ; P80 = mediane x 1,62 (log-normale 1.4).
H_NT = "temps de travail non trouvé"
SPECIALITES = [
    # (id, poste, montant, annee et relais, fiabilite, EP, IT, facteurs, ia, just, exclus, extra)
    ("F01", "Médecin généraliste", 89238, "2023, Quotidien du Médecin citant la CARMF (S174)", "relayée",
     4, 3, "F1 F2", "faible", "", [], []),
    ("F02", "Radiologue", 192625, "2023, Docteur Imago citant la CARMF (S174)", "relayée",
     3, 3, "F1 F2", "moyenne", "EP 3 : rayonnements ionisants réguliers (grille 1.3) ; IA : imagerie, exposition la plus citée", [], []),
    ("F03", "Ophtalmologue", 201000, "2023, Quotidien du Médecin citant la CARMF (S174)", "relayée",
     4, 3, "F1 F2", "faible", "", [], []),
    ("F04", "Anesthésiste-réanimateur", 209906, "2023, Quotidien du Médecin et What's up Doc citant la CARMF (S174)", "relayée",
     3, 2, "F1 F2 F3", "faible", "exercice en clinique : EP 3 (gaz anesthésiques, risques biologiques), IT 2 (vigilance de sécurité), "
     "F3 (astreintes de continuité des soins chirurgicaux et obstétricaux) ; ancrages des médecins de ville (Q2, Q18) "
     "retirés, ancrage des médecins hospitaliers (Q3) étendu en mixte", ["Q2", "Q18"], ["Q3"]),
    ("F05", "Anatomopathologiste", 190600, "2023, Quotidien du Médecin citant la CARMF (S174)", "relayée",
     3, 3, "F1 F2", "moyenne", "EP 3 : fixateurs et solvants (formol, xylène) ; IA : lecture de lames numérisées", [], []),
    ("F06", "Cancérologue (oncologie médicale et radiothérapie)", 366200, "2023, Quotidien du Médecin citant la CARMF, environ 700 médecins (S174)", "relayée",
     4, 2, "F1 F2", "faible", "IT 2 : exigences émotionnelles fortes et fréquentes (annonce, fin de vie)", [], []),
    ("F07", "Médecin nucléaire", 231400, "2023, Quotidien du Médecin citant la CARMF (S174)", "relayée",
     3, 3, "F1 F2", "moyenne", "EP 3 : sources radioactives non scellées", [], []),
    ("F08", "Gastro-entérologue", 157239, "2023, site spécialisé citant la CARMF (S175)", "relayée (site secondaire)",
     3, 3, "F1 F2", "faible", "EP 3 : endoscopies (risques biologiques, postures)", [], []),
    ("F09", "Cardiologue", 170766, "2024, cabinet d'expertise comptable citant la CARMF (S175)", "relayée (2024, site secondaire)",
     4, 3, "F1 F2", "faible", "", [], []),
    ("F10", "Dermatologue", 107139, "2024, site spécialisé citant la CARMF (S175)", "relayée (2024, site secondaire)",
     4, 3, "F1 F2", "moyenne", "IA : classement d'images de lésions", [], []),
    ("F11", "Gynécologue-obstétricien", 98390, "tableau de la CARMF relayé, année incertaine (2022 ou 2023, S175)", "relayée (année incertaine)",
     3, 2, "F1 F2 F3", "faible", "EP 3 et IT 2 : urgences obstétricales ; F3 : astreintes de maternité ; ancrages Q2 et Q18 retirés, "
     "Q3 étendu en mixte", ["Q2", "Q18"], ["Q3"]),
    ("F12", "Rhumatologue", 95200, "2023, Quotidien du Médecin citant la CARMF (S174)", "relayée",
     4, 3, "F1 F2", "faible", "", [], []),
    ("F13", "Psychiatre", 92500, "2023, Quotidien du Médecin citant la CARMF (S174)", "relayée",
     5, 3, "F1 F2", "faible", "EP 5 : cabinet sans contrainte physique", [], []),
    ("F14", "Pédiatre", 86200, "Quotidien du Médecin citant la CARMF, année non confirmée (S174)", "relayée (année non confirmée)",
     4, 3, "F1 F2", "faible", "", [], []),
]
for (_id, _poste, _x, _rel, _fiab, _ep, _it, _fx, _ia, _just, _excl, _extra) in SPECIALITES:
    _med = _x * NET_BNC * MED_MOY_LIB
    ajouter(id=_id, src="T01" if _id == "F01" else "T03", poste=_poste,
            citp="2211" if _id == "F01" else "2212", niveau=4, statut="libéral", pays="FR", resid="FR", cur="EUR",
            C=4, R=4, Se=5, fx=_fx, EP=_ep, IT=_it,
            groupe="medecin_hopital" if "F3" in _fx else "medecin_cabinet", ia=_ia, L=2, fiscal="liberal_fr",
            med=round(_med, -2), p80=round(_med * P80_LIB, -2),
            src_med=f"CARMF, revenu net d'activité indépendante moyen {_x:,} € ({_rel}) ; × 0,96 × 0,85".replace(",", " "),
            src_p80="estimé : log-normale des libéraux (× 1,62)", fiab=_fiab, h=H_NT, q=1.0, etp=H_NT,
            etp_ok=_id == "F01", anc_exclus=_excl, anc_extra=_extra, anc_partiel=list(_extra), just=_just)
# Le generaliste garde ses heures v6 (46 h, S07).
next(t for t in R1 if t["id"] == "F01").update(h=REV["T01"]["h"], etp=REV["T01"]["etp"], etp_ok=True)

# Medecins independants suisses par groupe de specialites (OFS 2019, mediane nette d'AVS et de 2e pilier,
# moins la prime LAMal ; P80 log-normale avec le rapport moyenne / mediane du premier recours, 199 975 / 172 000).
SPE_CH = [
    ("C01", "Psychiatre", 108000, "groupe psychiatrie", 5, "F1 F2 F3", ["Q10", "P8"], [],
     "F1 transposé du spécialiste français (heures non trouvées) ; F3 : gardes obligatoires des indépendants (Q15, 1.14) ; "
     "Q10 et P8 propres au premier recours, retirés"),
    ("C02", "Pédiatre", 172000, "groupe premier recours (médecine interne générale et pédiatrie)", 4, "F2 F3", [], ["Q10", "P8"],
     "premier recours : Q10 (43 h) et P8 (pénurie) gardés en mixte ; F3 : gardes obligatoires (Q15)"),
    ("C03", "Ophtalmologue", 266000, "groupe à activité chirurgicale (ophtalmologie, ORL, chirurgie)", 4, "F1 F2 F3", ["Q10", "P8"], [],
     "F1 transposé du spécialiste français ; F3 : gardes obligatoires (Q15) ; Q10 et P8 retirés"),
]
for (_id, _poste, _x, _groupe_ofs, _ep, _fx, _excl, _part, _just) in SPE_CH:
    ajouter(id=_id, src="T30", poste=_poste, citp="2212", niveau=4, statut="indépendant", pays="CH", resid="CH",
            cur="CHF", C=4, R=4, Se=5, fx=_fx, EP=_ep, IT=3, groupe="medecin_cabinet", ia="faible", L=2,
            fiscal="independant_ch", med=round(_x - LAMAL, -2), p80=round(p80_ln(_x, 199975 / 172000) - LAMAL, -2),
            src_med=f"OFS 2019 (S176) : {_groupe_ofs}, médiane {_x:,} CHF nets d'AVS et de 2e pilier ; moins la prime LAMal".replace(",", " "),
            src_p80="estimé : log-normale (rapport moyenne / médiane du premier recours, OFS)", fiab="relayée, groupe",
            h=H_NT, q=1.0, etp=H_NT, etp_ok=False, anc_exclus=_excl, anc_partiel=_part, just=_just)

# ---------------------------------------------------------------------------
# Cybersecurite : postes precis (remplacent T83 et T89)
# ---------------------------------------------------------------------------
ETP_PRIVE = "source en équivalent temps plein (salaires annuels à temps plein)"
CYBER_FR = [
    # (id, poste, citp, med brut, p80 brut, source, fiab, C, R, Se, fx, EP, IT, ia, L, just)
    ("F15", "Pentesteur (auditeur en tests d'intrusion)", "2529", 55000, 65000,
     "baromètre Silkhom 2026 relayé (S177) : 50 à 60 k€ brut fixe de 3 à 7 ans, 60 à 70 k€ au-delà ; milieu de fourchette × 0,78",
     "non officielle", 4, 4, 4, "F2", 5, 3, "moyenne", 4, ""),
    ("F16", "Ingénieur sécurité cloud", "2529", 80000, 90000,
     "site de formation (S177) : 70 à 90 k€ brut pour un profil confirmé ; milieu × 0,78 ; APEC, famille sécurité informatique : 64 k€ (recoupement)",
     "non officielle", 4, 4, 4, "F2", 5, 3, "moyenne", 4, ""),
    ("F17", "Consultant GRC (gouvernance, risques et conformité)", "2529", 64000, 64000 * 60800 / 48400,
     "APEC 2025 (S17, S103) : famille « sécurité informatique », médiane 60 k€ + 4 k€ de variable, brut (proxy) ; × 0,78",
     "relayée, proxy", 4, 4, 4, "F2", 5, 3, "elevee", 4, "IA élevée : rédaction documentaire et contrôles de conformité automatisables"),
    ("F18", "Responsable de la sécurité des systèmes d'information (RSSI)", "1330", 90000, 110000,
     "Robert Half 2026 relayé (S177) : médiane 90 k€ brut, 25e centile 80 k€, 75e centile 110 k€ ; × 0,78",
     "non officielle", 4, 4, 4, "F2 F3", 5, 2, "moyenne", 3,
     "IT 2 : gestion de crise, responsabilité ; F3 : astreintes de crise (Q19, mixte)"),
]
for (_id, _poste, _citp, _m, _p, _src, _fiab, _c, _r, _se, _fx, _ep, _it, _ia, _l, _just) in CYBER_FR:
    ajouter(id=_id, src="T83", poste=_poste, citp=_citp, niveau=4, statut="salarié", pays="FR", resid="FR", cur="EUR",
            C=_c, R=_r, Se=_se, fx=_fx, EP=_ep, IT=_it, groupe="informatique", ia=_ia, L=_l, fiscal="salarie_fr",
            med=round(_m * 0.78, -2), p80=round(_p * 0.78, -2), src_med=_src,
            src_p80="même source, haut de fourchette ou 75e à 80e centile (estimé)", fiab=_fiab, h="non trouvé",
            q=1.0, etp=ETP_PRIVE, etp_ok=True, just=_just)

CYBER_CH = [
    # (code, poste, citp, src v6, med brut, p80 brut, source, C, R, Se, fx, EP, IT, groupe, ia, L, extra)
    ("SOC", "Analyste SOC (niveaux 1 et 2)", "2529", "T84", 97000, 126000,
     "sites de salaires (S178) : environ 97 000 CHF brut en 2025 ; Glassdoor, SOC Analyst I : médiane 90 000, quartiles 71 804 et 109 229 CHF ; "
     "Optima 2026, SOC senior : 88 000 à 118 000 CHF ; × 0,80", 2, 3, 4, "F2 F3", 5, 2, "soc", "elevee", 2, ["P12", "Q19"]),
    ("PEN", "Pentesteur (auditeur en tests d'intrusion)", "2529", "T89", 112000, 130000,
     "ERI SalaryExpert, décembre 2025 (S178) : moyenne 114 262 CHF, 80 331 en début, 141 304 après 8 ans ; × 0,80",
     4, 4, 4, "F2", 5, 3, "informatique", "moyenne", 4, []),
    ("CLO", "Ingénieur sécurité cloud", "2529", "T89", 124000, 140000,
     "Paymetric Labs 2026 (S178) : médiane 124 000 CHF, quartiles 120 000 et 131 000, senior 162 000 ; Optima, senior : 125 000 à 168 000 ; × 0,80",
     4, 4, 4, "F2", 5, 3, "informatique", "moyenne", 4, []),
    ("GRC", "Consultant GRC (gouvernance, risques et conformité)", "2529", "T89", 114716, 114716 * 112000 / 96000,
     "ERI SalaryExpert (S178) : consultant en cybersécurité, médiane 114 716 CHF (proxy) ; × 0,80",
     4, 4, 4, "F2", 5, 3, "informatique", "elevee", 4, []),
    ("RSI", "Responsable de la sécurité des systèmes d'information (RSSI)", "1330", "T89", 200000, 250000,
     "cabinets de recrutement (S178) : CISO 185 000 à 320 000 CHF (Optima 2026), responsable de la sécurité de l'information 190 000 à 250 000 CHF ; "
     "estimé 200 000 ; × 0,80", 4, 4, 4, "F2 F3", 5, 2, "informatique", "moyenne", 3, []),
]
for _i, (_code, _poste, _citp, _src6, _m, _p, _srcm, _c, _r, _se, _fx, _ep, _it, _gr, _ia, _l, _extra) in enumerate(CYBER_CH):
    for _res in ("CH", "FR-GE"):
        _fxr = set(_fx.split()) | ({"F5"} if _res == "FR-GE" else set())
        ajouter(id=f"C{10 + 2 * _i + (_res == 'FR-GE')}", src=_src6, poste=_poste, citp=_citp, niveau=4, statut="salarié",
                pays="CH", resid=_res, cur="CHF", C=_c, R=_r, Se=_se, fx=_fxr, EP=_ep, IT=_it, groupe=_gr, ia=_ia, L=_l,
                fiscal="salarie_ch", med=round(_m * 0.80, -2), p80=round(_p * 0.80, -2), src_med=_srcm,
                src_p80="même source, haut de fourchette ou senior (estimé)", fiab="non officielle", h="non trouvé",
                q=1.0, etp=ETP_PRIVE, etp_ok=True, anc_extra=_extra,
                just="poste précis issu de T89 ; notes de T89" + (" et de T84 (SOC)" if _code == "SOC" else "")
                + ("" if _code not in ("RSI",) else " ; IT 2 et F3 comme le RSSI français"))

# ---------------------------------------------------------------------------
# Autres postes ajoutes (equivalents suisses de postes publics du pool, profession juridique liberale)
# ---------------------------------------------------------------------------
# Administrateur des Nations unies (P-3) a Geneve : bareme net CFPI 2026, echelon 1 a 15 de 71 335 a
# 92 127 USD, plus ajustement de poste de Geneve (84 %, sources divergentes de 84 a 87 %), exonere d'impot.
_ech6 = 71335 + 5 * (92127 - 71335) / 14
_net_usd = _ech6 * 1.84 - 0.079 * 108000 - 4000
_p80_usd = 92127 * 1.84 - 0.079 * 125000 - 4500
_usd_chf = M6.XR2025["CHF"] / M6.XR2025["USD"]
for _res in ("CH", "FR-GE"):
    ajouter(id="C20" if _res == "CH" else "C21", src="T64", poste="Administrateur de programme (P-3), Nations unies, Genève",
            citp="2422", niveau=4, statut="fonctionnaire international", pays="CH", resid=_res, cur="CHF",
            C=3, R=3, Se=3, fx="F2" + (" F5" if _res == "FR-GE" else ""), EP=5, IT=3, groupe="bureau_cadre", ia="moyenne",
            L=4, fiscal="exonere", exonere=True, med=round(_net_usd * _usd_chf, -2), p80=round(_p80_usd * _usd_chf, -2),
            src_med="barème CFPI relayé (S181) : P-3 échelon 6 estimé à 78 760 USD net de contribution du personnel, × 1,84 "
                    "(ajustement de poste de 84 %), moins pension 7,9 % et assurance maladie (estimées) ; converti au change 2025",
            src_p80="P-3 dernier échelon, 92 127 USD × 1,84, mêmes retenues (estimé)", fiab="relayée, estimée",
            h="40 h (non mesurée)", q=1.0, etp="barème à temps plein", etp_ok=True,
            just="notes de l'administrateur de l'UE (T64) ; PS 3 au lieu de 5 : contrats à durée déterminée renouvelables et "
                 "suppressions de postes annoncées en 2025 et 2026 à Genève (grille 1.3 : marché moyen, cyclique)")
ajouter(id="C22", src="T57", poste="Enseignant du secondaire I (cycle d'orientation), Genève", citp="2330", niveau=4,
        statut="fonctionnaire cantonal", pays="CH", resid="CH", cur="CHF", C=4, R=3, Se=5, fx="F2", EP=4, IT=3,
        groupe="enseignant", ia="moyenne", L=3, fiscal="salarie_ch", med=round(108500 * 0.80, -2), p80=round(121500 * 0.80, -2),
        src_med="agrégateur de salaires (S180) : 102 000 à 115 000 CHF brut en milieu de carrière, 90 000 à 100 000 au début ; "
                "milieu × 0,80 ; grille officielle du canton non lue",
        src_p80="fin de carrière, 115 000 à 128 000 CHF (S180) ; milieu × 0,80", fiab="non officielle",
        h="non trouvé", q=1.0, etp="grille à temps plein", etp_ok=True,
        just="notes du professeur certifié français (T57), ancrages français ramenés au statut mixte (autre pays) ; "
             "frontalier non retenu (condition de résidence non vérifiée)")
ajouter(id="F19", src=None, poste="Notaire", citp="2619", niveau=4, statut="libéral", pays="FR", resid="FR", cur="EUR",
        C=4, R=3, Se=4, fx="F1 F2", EP=5, IT=3, groupe="bureau_cadre", ia="moyenne", L=2, fiscal="liberal_fr",
        med=round(224976 * NET_BNC * MED_MOY_LIB, -2), p80=round(224976 * NET_BNC * MED_MOY_LIB * P80_LIB, -2),
        src_med="UNASA 2024 relayée (S182) : revenu moyen estimé 224 976 € ; × 0,96 × 0,85 ; médiane relayée de 197 500 € « brut » "
                "(définition non précisée) ; activité en baisse de 10 % en 2023 et de 4 % en 2024",
        src_p80="estimé : log-normale des libéraux (× 1,62)", fiab="relayée (site secondaire)", h=H_NT, q=1.0, etp=H_NT,
        etp_ok=False, just="notes estimées : C 4 (office propre), R 3 (clients en transaction), Se 4 (profession réglementée, "
                           "activité immobilière cyclique), F1 et F2 (charge d'actes et responsabilité)")

# Nom canonique d'un poste (meme poste sous deux noms en France et en Suisse) et type de statut.
CANON = {"Médecin de famille (médecine interne générale)": "Médecin généraliste (médecin de famille)",
         "Médecin généraliste": "Médecin généraliste (médecin de famille)",
         "Développeur logiciel (études et développement)": "Développeur logiciel",
         "Infirmier en soins généraux (IDE) hospitalier": "Infirmier en soins généraux hospitalier",
         "Médecin-dentiste": "Chirurgien-dentiste omnipraticien",
         "Physiothérapeute": "Masseur-kinésithérapeute"}
STATUT_TYPE = {"libéral": "indépendant", "indépendant": "indépendant", "artisan": "indépendant",
               "indépendant (freelance)": "indépendant (freelance)", "indépendant (mandataire)": "indépendant (mandataire)"}


def canon(t):
    return CANON.get(t["poste"], t["poste"])


def type_statut(t):
    s = t["statut"]
    if s in STATUT_TYPE:
        return STATUT_TYPE[s]
    if "fonctionnaire" in s or "statut" in s or s == "militaire":
        return "fonctionnaire"
    return "salarié"


def cle(t):
    return canon(t), type_statut(t)


for _t in R1:
    _t["cle_mc"] = "|".join(cle(_t))

IDS = [t["id"] for t in R1]
assert len(IDS) == len(set(IDS)), "identifiants en double"

if __name__ == "__main__":
    from collections import Counter
    print(len(R1), "triplets ;", Counter(t["pays"] + "/" + t["resid"] for t in R1))
    for t in R1:
        print(t["id"], t["src"], t["poste"], "|", t["statut"], "|", t["pays"], t["resid"], t["med"], t["p80"], sorted(t["fx"]))
