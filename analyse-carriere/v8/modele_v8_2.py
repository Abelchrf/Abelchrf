# -*- coding: utf-8 -*-
"""Version 8.2 : postes precis des familles de tete de la v8.1, sans refaire la v8.1.

Regles declarees avant calcul (consigne du 30 octobre 2026) :
- familles decoupees : les 10 premieres du classement France et les 10 premieres du classement Suisse de
  la v8.1, soit 13 familles (les deux listes se recoupent), decoupees dans les deux classements ;
- postes : tous les postes reels de chaque famille, au meme niveau (le poste ou la specialite) ; medecins :
  les diplomes d'etudes specialisees, biologie medicale exceptee (famille V2X93b) ; le nombre de postes
  varie donc selon la famille (choix valide) ;
- revenu du poste, de la source la plus precise a la moins precise : source qui nomme le poste (officielle
  ou non), puis groupe de postes qui le contient (Apec, OFS), sinon revenu de la famille v8 (signale) ;
  chaque revenu est marque officiel ou non officiel ; conversions v6 et v7 (Apec et sites : brut x 0,78 en
  France, x 0,80 en Suisse ; CARMF : moyenne x 0,96 x 0,85 ; OFS 2019 : mediane moins la prime LAMal) ;
- medecins : variante liberale francaise seulement si la CARMF publie la specialite ;
- notes hors revenu : celles de la famille, sauf ecart justifie poste par poste (regle v7, section 1.15) :
  EP 3 pour une exposition reguliere aux rayonnements, aux produits chimiques ou aux risques biologiques,
  IT 2 pour l'urgence, la vigilance de securite ou des exigences emotionnelles fortes, F3 pour les gardes,
  astreintes de bloc ou de maternite ; un ecart est une note estimee ;
- postes indiscernables (meme revenu et memes notes dans le classement) : une seule ligne, sinon des
  postes identiques compteraient comme plusieurs tickets dans les tirages ;
- classements : ceux de la v8.1 (France seule, Suisse seule en resident, revenu apres impot, echelle et
  tirages propres a chaque classement), les familles decoupees etant remplacees par leurs postes.
Usage : python modele_v8_2.py (ecrit resultats_v8_2.json a cote du script).
"""
import copy
import json
import math
import os
import re
import sys
from statistics import NormalDist

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.dirname(ICI))
import modele_v8 as M  # noqa: E402
import modele_v8_1 as M1  # noqa: E402
from revenus import LAMAL, P80_LIB  # noqa: E402

Z = NormalDist()
D = os.path.join(ICI, "donnees_v8_2")
APEC = json.load(open(os.path.join(D, "apec_111_familles_2025.json"), encoding="utf-8"))
V7 = {t["id"]: t for t in json.load(open(os.path.join(os.path.dirname(ICI), "resultats_v7.json"),
                                          encoding="utf-8"))["classement1"]}
NET_FR, NET_CH = 0.78, 0.80

# --- Sources ----------------------------------------------------------------------------------------
# CARMF, communique du 7 novembre 2023 : BNC 2022 moyen par specialite, secteurs 1 et 2 (donnees_v8_2).
CARMF = {
    "Médecine générale": 76512, "Allergologie": 66272, "Anatomie cytologie pathologiques": 139957,
    "Anesthésie réanimation": 164662, "Cancérologie": 258531, "Chirurgie": 140824, "Dermato vénérologie": 82809,
    "Endocrinologie et métabolisme": 60867, "Gastro entérologie hépatologie": 126094, "Gériatrie": 66388,
    "Gynécologie médicale": 57050, "Gynécologie obstétrique": 98390, "Hématologie": 93125,
    "Médecin biologiste": 96119, "Médecine d'urgence": 41692, "Médecine interne": 69007,
    "Médecine légale et expertises médicales": 70594, "Médecine nucléaire": 140147,
    "Médecine physique et de réadaptation": 74961, "Médecine vasculaire": 112005, "Néphrologie": 143789,
    "Neurologie": 101172, "Ophtalmologie": 145283, "Oto-rhino laryngologie": 109980,
    "Pathologie cardio vasculaire": 129400, "Pédiatrie": 74884, "Pneumologie": 101122, "Psychiatrie": 73014,
    "Radiologie imagerie médicale": 118368, "Rhumatologie": 75612, "Stomatologie": 130784,
}
# OFS, Revenus des medecins independants en 2019 (2021), T7 : mediane et 3e quartile par domaine (CHF, nets
# d'AVS et de 2e pilier) ; T14 : specialites de chaque domaine.
OFS_DOM = {"premier recours": (171788, 251116), "psychiatrie": (108164, 157143),
           "gynécologie et obstétrique": (219366, 349988), "spécialisée sans activité chirurgicale": (222112, 345480),
           "spécialisée avec activité chirurgicale": (265779, 404325), "autre domaine de spécialisation": (135096, 250121)}


def carmf(ligne):
    moy = CARMF[ligne]
    med = moy * 0.96 * 0.85
    return dict(med=med, p80=med * P80_LIB, cur="EUR", type="officiel", fiab="officielle (CARMF)",
                src=f"CARMF, communiqué du 7 novembre 2023 : BNC 2022 moyen « {ligne} » {moy:,} € × 0,96 × 0,85".replace(",", " "),
                src_p80="estimé : log-normale des libéraux (× 1,62)")


def ofs(dom):
    med, q3 = OFS_DOM[dom]
    p80 = med * math.exp(Z.inv_cdf(0.8) * math.log(q3 / med) / Z.inv_cdf(0.75))
    return dict(med=med - LAMAL, p80=p80 - LAMAL, cur="CHF", type="officiel", fiab="officielle (OFS, groupe de spécialités)",
                src=f"OFS 2021, revenus des médecins indépendants en 2019, T7 : domaine « {dom} », médiane {med:,} CHF ; moins la prime LAMal".replace(",", " "),
                src_p80=f"log-normale ajustée sur le 3e quartile OFS ({q3:,} CHF)".replace(",", " "))


def apec(cle):
    f = [x for x in APEC if cle.upper() in x["nom"].upper()]
    assert len(f) == 1, (cle, [x["nom"] for x in f])
    f = dict(f[0])
    f["nom"] = re.sub(r"\s+(\d+ ?%|2025)$", "", re.split(r"\s{2,}", f["nom"])[0])
    med = f["med"] * 1000 * NET_FR
    p80 = med * math.exp(Z.inv_cdf(0.8) * math.log(f["d9"] / f["med"]) / Z.inv_cdf(0.9))
    return dict(med=med, p80=p80, cur="EUR", type="non officiel", fiab="non officielle (enquête Apec, groupe de postes)",
                src=f"Apec 2025, 111 familles de métiers : « {f['nom'].capitalize()} », médiane {f['med']} k€ brut (fixe et variable) ; × 0,78",
                src_p80=f"log-normale ajustée sur le 9e décile Apec ({f['d9']} k€)")


def v7(ident):
    t = V7[ident]
    return dict(med=t["med"], p80=t["p80"], cur=t["cur"], src=t["src_med"] + f" (cellule v7 {ident})",
                src_p80=t["src_p80"], fiab=t["fiab"], type="officiel" if t["fiab"].startswith("officielle") else "non officiel")


def chf(brut, src):
    """Salaire suisse brut annuel d'un site ou d'un cabinet ; P80 : rapport de la famille (fixe plus bas)."""
    return dict(med=brut * NET_CH, p80=None, cur="CHF", type="non officiel", fiab="non officielle", src=src + " ; × 0,80",
                src_p80="estimé : rapport P80 / médiane de la famille en Suisse")


def fr_liberal(moy, src):
    med = moy * 0.96 * 0.85
    return dict(med=med, p80=med * P80_LIB, cur="EUR", type="non officiel", fiab="non officielle", src=src + " ; × 0,96 × 0,85",
                src_p80="estimé : log-normale des libéraux (× 1,62)")


DSI_CH = dict(med=144000, p80=168000, cur="CHF", type="non officiel", fiab="non officielle, non datée",
              src="Michael Page, fiche de salaires informatiques non datée (S193) : directeur des systèmes d'information, "
                  "180 000 CHF de salaire de base moyen ; × 0,80 (cellule v7.1)",
              src_p80="estimé : rapport P80 / médiane des spécialistes TIC suisses (× 1,17)")

# --- Postes -----------------------------------------------------------------------------------------
# Medecins : (code, poste, ligne CARMF ou None, domaine OFS, EP, IT, F3).
MEDECINS = [
    ("MG", "Médecin généraliste", "Médecine générale", "premier recours", 4, 3, 0),
    ("ALL", "Allergologue", "Allergologie", "spécialisée sans activité chirurgicale", 4, 3, 0),
    ("ACP", "Anatomopathologiste", "Anatomie cytologie pathologiques", "autre domaine de spécialisation", 3, 3, 0),
    ("ANE", "Anesthésiste-réanimateur", "Anesthésie réanimation", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("CMF", "Chirurgien maxillo-facial", "Stomatologie", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("CORA", "Chirurgien oral (médecin)", "Stomatologie", "spécialisée avec activité chirurgicale", 3, 3, 0),
    ("CORT", "Chirurgien orthopédiste", "Chirurgie", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("CPED", "Chirurgien pédiatrique", "Chirurgie", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("CPLA", "Chirurgien plasticien", "Chirurgie", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("CTCV", "Chirurgien thoracique et cardiovasculaire", "Chirurgie", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("CVAS", "Chirurgien vasculaire", "Chirurgie", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("CVIS", "Chirurgien viscéral et digestif", "Chirurgie", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("NCH", "Neurochirurgien", "Chirurgie", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("URO", "Urologue", "Chirurgie", "spécialisée avec activité chirurgicale", 3, 2, 1),
    ("CAR", "Cardiologue", "Pathologie cardio vasculaire", "spécialisée sans activité chirurgicale", 4, 3, 0),
    ("DER", "Dermatologue", "Dermato vénérologie", "autre domaine de spécialisation", 4, 3, 0),
    ("END", "Endocrinologue", "Endocrinologie et métabolisme", "spécialisée sans activité chirurgicale", 4, 3, 0),
    ("GEN", "Généticien", None, "autre domaine de spécialisation", 4, 3, 0),
    ("GER", "Gériatre", "Gériatrie", "autre domaine de spécialisation", 4, 3, 0),
    ("GYM", "Gynécologue médical", "Gynécologie médicale", "gynécologie et obstétrique", 4, 3, 0),
    ("GYO", "Gynécologue-obstétricien", "Gynécologie obstétrique", "gynécologie et obstétrique", 3, 2, 1),
    ("HEM", "Hématologue", "Hématologie", "spécialisée sans activité chirurgicale", 4, 2, 0),
    ("HGE", "Hépato-gastro-entérologue", "Gastro entérologie hépatologie", "spécialisée sans activité chirurgicale", 3, 3, 0),
    ("INF", "Infectiologue", None, "spécialisée sans activité chirurgicale", 3, 3, 0),
    ("INT", "Médecin interniste", "Médecine interne", "premier recours", 4, 3, 0),
    ("MIR", "Médecin intensiviste-réanimateur", None, "autre domaine de spécialisation", 3, 2, 1),
    ("MLE", "Médecin légiste", "Médecine légale et expertises médicales", "autre domaine de spécialisation", 3, 3, 0),
    ("MNU", "Médecin nucléaire", "Médecine nucléaire", "autre domaine de spécialisation", 3, 3, 0),
    ("MPR", "Médecin de médecine physique et de réadaptation", "Médecine physique et de réadaptation",
     "spécialisée sans activité chirurgicale", 4, 3, 0),
    ("MTR", "Médecin du travail", None, "autre domaine de spécialisation", 4, 3, 0),
    ("MVA", "Médecin vasculaire (angiologue)", "Médecine vasculaire", "spécialisée sans activité chirurgicale", 4, 3, 0),
    ("NEP", "Néphrologue", "Néphrologie", "spécialisée sans activité chirurgicale", 4, 3, 0),
    ("NEU", "Neurologue", "Neurologie", "spécialisée sans activité chirurgicale", 4, 3, 0),
    ("ONC", "Oncologue (oncologie médicale et radiothérapie)", "Cancérologie", "spécialisée sans activité chirurgicale", 4, 2, 0),
    ("OPH", "Ophtalmologue", "Ophtalmologie", "spécialisée avec activité chirurgicale", 4, 3, 0),
    ("ORL", "ORL et chirurgien cervico-facial", "Oto-rhino laryngologie", "spécialisée avec activité chirurgicale", 4, 3, 0),
    ("PED", "Pédiatre", "Pédiatrie", "premier recours", 4, 3, 0),
    ("PNE", "Pneumologue", "Pneumologie", "spécialisée sans activité chirurgicale", 4, 3, 0),
    ("PSY", "Psychiatre", "Psychiatrie", "psychiatrie", 5, 3, 0),
    ("RAD", "Radiologue", "Radiologie imagerie médicale", "autre domaine de spécialisation", 3, 3, 0),
    ("RHU", "Rhumatologue", "Rhumatologie", "spécialisée sans activité chirurgicale", 4, 3, 0),
    ("SPU", "Médecin de santé publique", None, "autre domaine de spécialisation", 5, 3, 0),
    ("URG", "Médecin urgentiste", "Médecine d'urgence", "autre domaine de spécialisation", 3, 2, 1),
]

POSTES = {"V2X90": []}
for code, nom, ligne, dom, ep, it, f3 in MEDECINS:
    p = dict(id=code, nom=nom, EP=ep, IT=it, F3=f3, **{"CH-ind": ofs(dom)})
    if ligne:
        p["FR-ind"] = carmf(ligne)
    else:
        p["sans"] = {"FR-ind"}
    POSTES["V2X90"].append(p)

POSTES.update({
    "V2X91": [dict(id=i, nom=n) for i, n in (("OMNI", "Chirurgien-dentiste omnipraticien"),
                                            ("ODF", "Orthodontiste (spécialiste ODF)"),
                                            ("CO", "Chirurgien oral (dentiste)"),
                                            ("MBD", "Spécialiste en médecine bucco-dentaire"))],
    "V2X93b": [dict(id="BIO", nom="Biologiste médical", **{"FR-ind": carmf("Médecin biologiste"),
                                                           "FR-sal": apec("PHARMACIE ET DE LA BIOLOGIE")})],
    "V3X80d": [dict(id="ORTHOPHO", nom="Orthophoniste", **{"FR-sal": apec("SOINS INFIRMIERS ET PARAM")}),
               dict(id="ORTHOPT", nom="Orthoptiste", **{"FR-ind": fr_liberal(
                   48000, "Advizexperts, cabinet comptable (2025) : revenu moyen annuel d'un orthoptiste libéral 48 000 €, méthode non publiée")})],
    "V3X80a": [dict(id="DIET", nom="Diététicien", **{"FR-sal": apec("SOINS INFIRMIERS ET PARAM")})],
    "V3X90": [dict(id="CLIN", nom="Psychologue clinicien", **{"FR-sal": apec("PSYCHOLOGIE ET DE L'ACCOMPAGNEMENT")}),
              dict(id="NEURO", nom="Neuropsychologue", **{"FR-sal": apec("PSYCHOLOGIE ET DE L'ACCOMPAGNEMENT")}),
              dict(id="TRAV", nom="Psychologue du travail", **{"FR-sal": apec("RELATIONS SOCIALES")}),
              dict(id="PSYEN", nom="Psychologue de l'Éducation nationale", sans={"FR-ind"}, **{"FR-sal": v7("T57")}),
              dict(id="PSYTH", nom="Psychothérapeute")],
    "P2X90h": [dict(id=i, nom=n) for i, n in (("CONSP", "Conservateur du patrimoine"),
                                             ("CONSB", "Conservateur des bibliothèques"),
                                             ("ACP", "Attaché de conservation du patrimoine"),
                                             ("BIB", "Bibliothécaire"))],
    "M2X91": [dict(id="DSI", nom="Directeur des systèmes d'information (DSI)",
                   **{"FR-sal": apec("DIRECTION INFORMATIQUE"), "CH-sal": DSI_CH}),
              dict(id="CDP", nom="Chef de projet informatique", **{"FR-sal": apec("GESTION DE PROJETS INFORMATIQUES")}),
              dict(id="PO", nom="Product owner (chef de projet agile)", **{"FR-sal": apec("GESTION DE PROJETS INFORMATIQUES")}),
              dict(id="MOA", nom="Chef de projet maîtrise d'ouvrage", **{"FR-sal": apec("MAÎTRISE D'OUVRAGE")}),
              dict(id="RSSI", nom="Responsable de la sécurité des systèmes d'information (RSSI)", IT=2, F3=1,
                   **{"FR-sal": v7("F18"), "CH-sal": v7("C18")})],
    "M2X93": [dict(id="ARCH", nom="Architecte SI et cloud", **{"FR-sal": apec("INFRASTRUCTURES ET SYSTÈMES")}),
              dict(id="GRC", nom="Consultant cybersécurité GRC (gouvernance, risques et conformité)",
                   **{"FR-sal": apec("SÉCURITÉ INFORMATIQUE"), "CH-sal": v7("C16")}),
              dict(id="PENT", nom="Pentesteur (auditeur en tests d'intrusion)", **{"FR-sal": v7("F15"), "CH-sal": v7("C12")}),
              dict(id="SECC", nom="Ingénieur sécurité cloud", **{"FR-sal": v7("F16"), "CH-sal": v7("C14")}),
              dict(id="ERP", nom="Consultant ERP et progiciels", **{"FR-sal": apec("INTÉGRATION PROGICIELLE")}),
              dict(id="BI", nom="Consultant BI et décisionnel", **{"FR-sal": apec("BUSINESS INTELLIGENCE")}),
              dict(id="RES", nom="Expert réseaux et télécoms", **{"FR-sal": apec("RÉSEAUX INFORMATIQUES")}),
              dict(id="DBA", nom="Expert bases de données", **{"FR-sal": apec("BASES DE DONNÉES")})],
    "M2X90": [dict(id="DEV", nom="Développeur (ingénieur études et développement)", **{"FR-sal": apec("DÉVELOPPEMENT INFORMATIQUE")}),
              dict(id="DEVOPS", nom="Ingénieur cloud DevOps", F3=1, **{"FR-sal": apec("INFRASTRUCTURES ET SYSTÈMES")}),
              dict(id="DE", nom="Data engineer", **{"FR-sal": apec("BIG DATA")}),
              dict(id="DS", nom="Data scientist", **{"FR-sal": apec("BIG DATA"), "CH-sal": chf(
                  110000, "Lohncheck (site de salaires, 2026, d'après Robert Half et ITBoard) : data scientist, médiane environ 110 000 CHF")}),
              dict(id="ML", nom="Ingénieur machine learning", **{"FR-sal": apec("BIG DATA")}),
              dict(id="EMB", nom="Ingénieur systèmes embarqués", **{"FR-sal": apec("INFORMATIQUE INDUSTRIELLE")}),
              dict(id="TEL", nom="Ingénieur réseaux et télécoms", **{"FR-sal": apec("RÉSEAUX INFORMATIQUES")}),
              dict(id="TEST", nom="Ingénieur test et validation", **{"FR-sal": apec("TESTS ET RECETTES")})],
    "QAX03": [dict(id="ACT", nom="Actuaire", **{"FR-sal": apec("ACTUARIAT"), "CH-sal": chf(
                  114847, "Payscale (déclarations, Zurich, 2026) : actuaire, médiane 114 847 CHF")}),
              dict(id="SOUS", nom="Souscripteur", **{"FR-sal": apec("SOUSCRIPTION ET GESTION")}),
              dict(id="EXP", nom="Expert d'assurances (sinistres)", **{"FR-sal": apec("SOUSCRIPTION ET GESTION")}),
              dict(id="RISK", nom="Risk manager", **{"FR-sal": apec("RISQUES ET DU CONTRÔLE INTERNE")})],
    "N1X90": [dict(id="RD", nom="Ingénieur R&D (généraliste)", **{"FR-sal": apec("INGÉNIERIE R&D")}),
              dict(id="ELEC", nom="Ingénieur électronique et électrique", **{"FR-sal": apec("ÉLECTRIQUE ET ÉLECTRONIQUE")}),
              dict(id="MECA", nom="Ingénieur mécanique", **{"FR-sal": apec("INGÉNIERIE MÉCANIQUE")}),
              dict(id="MAT", nom="Ingénieur matériaux", EP=3, **{"FR-sal": apec("INGÉNIERIE EN MATÉRIAUX")}),
              dict(id="CHIM", nom="Ingénieur chimiste ou biologiste R&D", EP=3, **{"FR-sal": apec("CHIMIQUE, BIOLOGIQUE")}),
              dict(id="CALC", nom="Ingénieur calcul et simulation", **{"FR-sal": apec("CALCUL ET DE LA SIMULATION")}),
              dict(id="ESSAI", nom="Ingénieur essais et instrumentation", EP=4, **{"FR-sal": apec("INSTRUMENTATION ET DES ESSAIS")}),
              dict(id="CPRD", nom="Chef de projet R&D", **{"FR-sal": apec("GESTION DE PROJETS R&D")})],
    "W1X80b": [dict(id="FORM", nom="Formateur d'adultes", **{"FR-sal": apec("ENSEIGNEMENT ET DE LA FORMATION")}),
               dict(id="INGF", nom="Responsable et ingénieur de formation", **{"FR-sal": apec("INGÉNIERIE DE LA FORMATION")})],
})
FAMILLES = sorted(POSTES)


def variantes_poste(fam, p):
    out = []
    for v in M.V:
        if v["metier"] != fam or v["kind"] in p.get("sans", set()):
            continue
        w = copy.deepcopy(v)
        w.update(famille=fam, nom_famille=v["nom"], metier=f"{fam}:{p['id']}", nom=p["nom"], postes=[p["nom"]])
        spec = p.get(v["kind"])
        if spec:
            r = dict(spec)
            if r["p80"] is None:
                r["p80"] = r["med"] * v["rev"]["p80"] / v["rev"]["med"]
            w["rev"].update({k: r[k] for k in ("med", "p80", "cur", "src", "src_p80", "fiab")})
            w["rev_type"] = f"poste, {r['type']}"
        else:
            w["rev_type"] = "famille, " + ("officiel" if v["rev"]["fiab"].startswith("officielle") else "non officiel")
        n, prov = w["notes"], w["prov"]
        for d in ("EP", "IT"):
            if d in p and p[d] != n[d]:
                n[d], prov[d] = p[d], "estimée"
        if p.get("F3") and not n["F3"]:
            n["F3"] = 1
            n["QT"] = max(1, 5 - n["F1"] - 1 - n["H"])
            prov["QT"] = "estimée"
        out.append(w)
    return out


def signature(variantes):
    return tuple(sorted((w["kind"], w["resid"], round(w["rev"]["med"], 2), round(w["rev"]["p80"], 2), w["rev"]["cur"],
                         tuple(w["notes"][d] for d in M.DIMS6)) for w in variantes))


def classement(pays_resid):
    V = [M1.preparer(v) for v in M.V if v["resid"] == pays_resid and v["metier"] not in POSTES]
    fusions = []
    for fam in FAMILLES:
        groupes = {}
        for p in POSTES[fam]:
            ws = [w for w in variantes_poste(fam, p) if w["resid"] == pays_resid]
            if ws:
                groupes.setdefault(signature(ws), []).append(ws)
        for g in groupes.values():
            ws = g[0]
            noms = [x[0]["nom"] for x in g]
            for w in ws:
                w["postes"] = noms
                w["nom"] = " / ".join(noms)
            V += [M1.preparer(w) for w in ws]
            if len(g) > 1:
                fusions.append(noms)
    return V, fusions


out = {}
for nom, resid in (("France", "FR"), ("Suisse", "CH")):
    V, fusions = classement(resid)
    out[nom] = M1.classer_et_tirer(nom, V)
    out[nom]["postes_regroupes"] = fusions
    R = out[nom]["classement"]
    n_postes = sum(1 for v in R if "famille" in v)
    print(f"   {n_postes} lignes de postes (dont {len(fusions)} regroupements), {len(R) - n_postes} familles non découpées")
    for i, v in enumerate(sorted(R, key=lambda v: (-v["p_top"], -v["W"]))[:22], 1):
        r, n = v["rev"], v["notes"]
        print(f"{i:2} {v['nom'][:70]:70} {v.get('famille', '(famille)'):7} {v['kind']:6} W={v['W']:.3f} "
              f"P10={v['p_top']:.3f} P1={v['p_1']:.3f} | EP{n['EP']} IT{n['IT']} QT{n['QT']} ES{n['ES']} PS{n['PS']} "
              f"RE{v['RE']:.2f} | {r['med_ai']:,.0f} {r['cur']} | {v.get('rev_type', 'famille non découpée')}"
              f"{' CITP2' if v['citp2'] else ''}".replace(",", " "))

json.dump(out, open(os.path.join(ICI, "resultats_v8_2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1,
          default=lambda x: sorted(x) if isinstance(x, set) else float(x))
