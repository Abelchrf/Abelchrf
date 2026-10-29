# -*- coding: utf-8 -*-
"""Version 7.1 (29 octobre 2026) : liste neutre, un seul triplet par code CITP-08 a 4 chiffres, sans regle de langue.

Consigne du 29 octobre (correction de la v7), regles appliquees :
1. Chaque code CITP-08 a 4 chiffres porte un seul poste, au meme niveau de detail pour tous les domaines.
   Les postes plus fins sont fusionnes dans leur code avec une cellule revenu de niveau code :
   13 specialites medicales -> 2212 (DREES 2021, ensemble des specialistes liberaux ; OFS 2019, ensemble des
   medecins independants en Suisse) ; 4 postes de cybersecurite -> 2529 (APEC, famille securite informatique ;
   ESS, specialistes TIC) ; RSSI -> 1330 (APEC, famille direction informatique ; directeur informatique en
   Suisse) ; IDE et IADE -> 2221 ; inspecteur et controleur des finances publiques -> 3352 (recodage de
   l'inspecteur, classe 2411 en v6 ; 3352 = agents des services fiscaux).
2. Chaque code a plusieurs variantes statut x pays ; seul le meilleur score de base est garde (un triplet par
   code). Bornes de l'echelle de revenu : toutes les variantes du classement.
3. Regle de langue supprimee : ES = relations dans tous les pays.
4. Classement monde : les 10 pays du tri, puis Etats-Unis, Canada, Australie, Singapour et Emirats pour les
   10 premiers codes ; un revenu non trouve laisse la cellule vide et la variante n'est pas classee.
Couverture : les codes qui ont deja des donnees ; elle vient de l'historique de l'analyse (limite signalee).
"""
import copy
import json
import math
import os

import classement2_v7 as C2
import fiscalite_v7 as F
import modele as M6
import modele_v7 as M7
import postes_v7 as P
from revenus import LAMAL, MED_MOY_LIB, NET_BNC, P80_LIB, REV, p80_ln

ICI = os.path.dirname(os.path.abspath(__file__))
NOMS_CITP = {
    "0210": "Sous-officiers des forces armées", "1330": "Directeurs des services des TIC",
    "2120": "Mathématiciens, actuaires et statisticiens", "2141": "Ingénieurs industriels et de production",
    "2211": "Médecins généralistes", "2212": "Médecins spécialistes", "2221": "Infirmiers",
    "2222": "Sages-femmes", "2230": "Médecines traditionnelle et complémentaire", "2250": "Vétérinaires",
    "2261": "Dentistes", "2262": "Pharmaciens", "2264": "Physiothérapeutes", "2265": "Diététiciens",
    "2266": "Audiologistes et orthophonistes", "2267": "Optométristes et orthoptistes",
    "2269": "Professions de la santé non classées ailleurs", "2330": "Professeurs du secondaire",
    "2341": "Instituteurs du primaire", "2411": "Comptables", "2422": "Spécialistes des politiques d'administration",
    "2512": "Concepteurs de logiciels", "2521": "Concepteurs et administrateurs de bases de données",
    "2522": "Administrateurs de systèmes", "2529": "Spécialistes des bases de données et des réseaux n.c.a. (cybersécurité)",
    "2611": "Avocats", "2612": "Magistrats", "2619": "Juristes non classés ailleurs", "2634": "Psychologues",
    "3115": "Techniciens en génie mécanique", "3153": "Pilotes d'avions", "3154": "Contrôleurs de la circulation aérienne",
    "3211": "Techniciens d'imagerie médicale", "3254": "Opticiens", "3313": "Professions intermédiaires de la comptabilité",
    "3322": "Représentants commerciaux", "3334": "Agents immobiliers", "3352": "Agents des services fiscaux",
    "3513": "Techniciens des réseaux et systèmes", "5223": "Vendeurs en magasin", "5321": "Aides-soignants",
    "5411": "Pompiers", "5412": "Agents de police", "7126": "Plombiers et tuyauteurs",
    "7127": "Mécaniciens en froid et climatisation", "7411": "Électriciens du bâtiment", "8311": "Conducteurs de locomotives",
    "8332": "Conducteurs de poids lourds",
}
RECODE = {"T61": "3352"}
LIEUX_PROPRES = {"C20", "C21"}  # Nations unies a Geneve : poste propre au lieu, non transpose


def code_de(t):
    return RECODE.get(t["id"], t["citp"])


def cellule_v6(src, **kw):
    r = REV[src]
    d = dict(med=r["med"], p80=r["p80"], src_med=r["src_med"], src_p80=r["src_p80"], fiab=r["fiab"], h=r["h"],
             q=r["q"], etp=r["etp"], etp_ok=r["etp_ok"])
    d.update(kw)
    return d


_spe = 153300 * NET_BNC * MED_MOY_LIB
_ch_spe = 162000
FUSIONS = {
    # (code, type de statut, pays, residence) : (triplet modele des notes, cellule, poste represente)
    ("2212", "indépendant", "FR", "FR"): ("F12", dict(
        med=round(_spe, -2), p80=round(_spe * P80_LIB, -2),
        src_med="DREES 2021 (S02) : médecins spécialistes libéraux hors généralistes, revenu d'activité moyen 153 300 € ; × 0,96 × 0,85",
        src_p80="estimé : log-normale des libéraux (× 1,62)", fiab="relayée", h="non trouvé", q=1.0,
        etp="temps de travail non trouvé", etp_ok=False), "spécialistes libéraux, toutes spécialités"),
    ("2211", "indépendant", "FR", "FR"): ("F01", cellule_v6("T01"), "médecin généraliste"),
    ("2529", "salarié", "FR", "FR"): ("F15", cellule_v6("T83"), "sécurité informatique, famille APEC"),
    ("1330", "salarié", "FR", "FR"): ("F18", dict(
        med=round(77000 * 0.78, -2), p80=round(77000 * 0.78 * 60800 / 48400, -2),
        src_med="APEC 2025 (S192) : famille « direction informatique », médiane 77 k€ brut, fixe et variable (proxy du code) ; × 0,78",
        src_p80="estimé : rapport P80 / médiane de la famille sécurité informatique (× 1,26)", fiab="relayée, proxy",
        h="non trouvé", q=1.0, etp="source en équivalent temps plein (cadres à temps plein)", etp_ok=True),
        "directeur des services informatiques"),
    ("2221", "fonctionnaire", "FR", "FR"): ("T12", cellule_v6("T12"), "infirmier hospitalier, IADE compris"),
    ("3352", "fonctionnaire", "FR", "FR"): ("T62", dict(
        med=round((40500 + 32600) / 2, -2), p80=round((48600 + 39200) / 2, -2),
        src_med="Insee et DGAFP 2023 (S67) : catégories A (3 373 €) et B (2 720 €), net moyen par mois (proxy) ; moyenne simple des deux grades (estimé)",
        src_p80="estimé : amplitude de grille (× 1,2)", fiab="officielle, proxy, moyenne estimée", h="non trouvé", q=1.0,
        etp="source en équivalent temps plein (EQTP)", etp_ok=True), "inspecteur et contrôleur des finances publiques"),
    ("2529", "salarié", "CH", "CH"): ("C12", cellule_v6("T89"), "spécialistes TIC, ESS"),
    ("2529", "salarié", "CH", "FR-GE"): ("C13", cellule_v6("T89"), "spécialistes TIC, ESS"),
    ("1330", "salarié", "CH", "CH"): ("C18", dict(
        med=round(180000 * 0.80, -2), p80=round(180000 * 0.80 * 112000 / 96000, -2),
        src_med="Michael Page, fiche de salaires informatiques non datée (S193) : directeur des systèmes d'information, 180 000 CHF de salaire de base moyen ; × 0,80",
        src_p80="estimé : rapport P80 / médiane des spécialistes TIC suisses (× 1,17)", fiab="non officielle, non datée",
        h="non trouvé", q=1.0, etp="source à temps plein", etp_ok=True), "directeur des systèmes d'information"),
    ("1330", "salarié", "CH", "FR-GE"): ("C19", None, "directeur des systèmes d'information"),
    ("2212", "indépendant", "CH", "CH"): ("C03", dict(
        med=round(_ch_spe - LAMAL, -2), p80=round(p80_ln(_ch_spe, 204985 / 162000) - LAMAL, -2),
        src_med="OFS 2019 (S176, S24) : ensemble des médecins indépendants, médiane 162 000 CHF nets d'AVS et de 2e pilier (généralistes compris, proxy) ; moins la prime LAMal",
        src_p80="estimé : log-normale (moyenne OFS 204 985 CHF)", fiab="relayée, proxy", h="non trouvé", q=1.0,
        etp="temps de travail non trouvé", etp_ok=False), "spécialistes indépendants, toutes spécialités"),
}
FUSIONS[("1330", "salarié", "CH", "FR-GE")] = ("C19", FUSIONS[("1330", "salarié", "CH", "CH")][1], "directeur des systèmes d'information")

R1_PAR_ID = {t["id"]: t for t in M7.R1}


def nouvelle_variante(modele, code, cellule, poste_rep, ident):
    t = copy.deepcopy({k: v for k, v in modele.items() if k not in ("mc", "rangs_var", "prov", "modifs")})
    if cellule is not None:
        t.update(cellule)
    t["citp"] = code
    t["code"] = code
    t["poste_rep"] = poste_rep
    t["poste"] = f"{code} {NOMS_CITP[code]}"
    t["id"] = ident
    t["langue"] = 0
    t["cle_mc"] = code
    return t


def variantes_r1():
    groupes = {}
    for t in M7.R1:
        k = (code_de(t), P.type_statut(t), t["pays"], t["resid"])
        groupes.setdefault(k, []).append(t)
    V = []
    for k, membres in sorted(groupes.items()):
        code, st, pays, res = k
        ident = f"{code}-{pays}{'f' if res in ('FR-GE', 'FR-LO') else ''}-{st[:3]}"
        if k in FUSIONS:
            mod, cel, rep = FUSIONS[k]
            V.append(nouvelle_variante(R1_PAR_ID[mod], code, cel, rep, ident))
        elif len(membres) == 1:
            m = membres[0]
            V.append(nouvelle_variante(m, code, None, m["poste"], ident))
        else:
            raise ValueError(f"fusion non déclarée : {k} {[m['id'] for m in membres]}")
        V[-1]["src_v7"] = ",".join(m["id"] for m in membres)
    return V


def calculer(V):
    M7.preparer(V)
    B = M7.bornes(V)
    M7.classer(V, B)
    meilleurs = {}
    for t in sorted(V, key=lambda t: (-t["W"], t["id"])):
        meilleurs.setdefault(t["code"], t)
    sel = [copy.deepcopy(t) for t in meilleurs.values()]
    for t in sel:
        for cle in ("rangs_var", "mc"):
            t.pop(cle, None)
    cl = M7.classer(sel, B)
    mc = {v: M7.tirages(sel, B, v) for v in "ABCD"}
    for t in sel:
        t["mc"] = {v: mc[v][t["id"]] for v in mc}
    return sel, cl, B


# ---------------------------------------------------------------------------
# Classement 1 : France et Suisse
# ---------------------------------------------------------------------------
V1 = variantes_r1()
SEL1, CL1, B1 = calculer(V1)

# ---------------------------------------------------------------------------
# Classement 2 : 10 pays retenus, puis 5 pays ajoutes pour les 10 premiers codes
# ---------------------------------------------------------------------------
LUS2 = {  # donnees lues de la v7, au niveau du code
    ("2211", "indépendant", "DE"): ("Médecin généraliste (médecin de famille)", "indépendant", "DE"),
    ("2211", "indépendant", "GB"): ("Médecin généraliste (médecin de famille)", "indépendant", "GB"),
    ("2212", "salarié", "NO"): (C2.HOSP, "salarié", "NO"),
    ("2212", "salarié", "DK"): (C2.HOSP, "salarié", "DK"),
    ("2212", "salarié", "GB"): (C2.HOSP, "salarié", "GB"),
    ("2512", "salarié", "NO"): ("Développeur logiciel", "salarié", "NO"),
    ("2512", "salarié", "GB"): ("Développeur logiciel", "salarié", "GB"),
    ("2512", "salarié", "NL"): ("Développeur logiciel", "salarié", "NL"),
    ("2512", "salarié", "DE"): ("Développeur logiciel", "salarié", "DE"),
}


def rapport_structure(V, code, st):
    fr, ch, q = [], [], []
    for t in V:
        if t["code"] != code or P.type_statut(t) != st or t["id"] in LIEUX_PROPRES:
            continue
        if t["pays"] == "FR":
            fr.append(t["med"] / 0.78 / C2.AW["FR"][0])
        else:
            ch.append(t["med"] / 0.80 / C2.AW["CH"][0])
        q.append(t["p80"] / t["med"])
    vals = [sum(x) / len(x) for x in (fr, ch) if x]
    if not vals:
        return None
    r = math.exp(sum(math.log(v) for v in vals) / len(vals))
    return r, math.exp(sum(math.log(v) for v in q) / len(q)), "+".join(p for p, x in (("FR", fr), ("CH", ch)) if x)


def cellule_pays(V, code, st, pays):
    if (code, st, pays) in LUS2:
        return C2.cellule_lue((LUS2[(code, st, pays)][0], st), pays)
    rs = rapport_structure(V, code, st)
    if rs is None:
        return None
    r, q, src = rs
    if code == "2212" and st == "indépendant":
        r = min(r, 5.0)
    brut = r * C2.AW[pays][0]
    return dict(med=round(brut, -2), p80=round(brut * q, -2), fiscal="brut_" + pays, net_de_brut=F.NET_PAYS[pays],
                src_med=f"estimé (structure) : rapport au salaire moyen {r:.2f} ({src}) × salaire moyen OCDE 2025 du pays",
                src_p80=f"estimé : rapport P80 / médiane du code ({q:.2f})", fiab="estimé (structure)", h="non trouvé",
                q=1.0, etp="règle de structure (temps plein)", etp_ok=False, rapport=r)


def variantes_r2(V1):
    V = []
    for t in V1:  # Suisse : toutes ses variantes du classement 1
        if t["pays"] == "CH":
            c = {k: v for k, v in t.items() if k not in ("mc", "rangs_var", "prov", "modifs")}
            c = copy.deepcopy(c)
            c["langue"] = 0
            V.append(c)
    bases = {}
    for t in sorted(V1, key=lambda t: (-t["W"], t["id"])):
        if t["id"] in LIEUX_PROPRES:
            continue
        bases.setdefault((t["code"], P.type_statut(t)), t)
    n = 0
    for (code, st), base in sorted(bases.items()):
        for pays in C2.PAYS2:
            if pays == "CH":
                continue
            if code == "2212" and st == "indépendant" and pays not in C2.PAYS_LIBERAL_SPE:
                continue
            if code == "2212" and st in ("salarié", "fonctionnaire") and (st == "fonctionnaire" or pays not in C2.PAYS_HOSP):
                continue
            if code == "2619" and pays not in C2.NOTAIRE_PAYS:
                continue
            for resid in [pays] + (["FR-LO"] if pays == "LU" and st == "salarié" else []):
                if code == "2212" and st == "salarié":
                    cel = C2.cellule_lue((C2.HOSP, "salarié"), pays) if (C2.HOSP, "salarié", pays) in C2.REVENUS_LUS else None
                    if cel is None:
                        r = math.exp((math.log(83100 / 0.78 / C2.AW["FR"][0]) + math.log(163600 / 0.80 / C2.AW["CH"][0])) / 2)
                        cel = dict(med=round(r * C2.AW[pays][0], -2), p80=round(r * C2.AW[pays][0] * 1.2, -2), fiscal="brut_" + pays,
                                   net_de_brut=F.NET_PAYS[pays], src_med=f"estimé (structure) : rapport {r:.2f} (praticien hospitalier, médecin hospitalier suisse)",
                                   src_p80="estimé : amplitude de grille (× 1,2)", fiab="estimé (structure)", h="non trouvé", q=1.0,
                                   etp="règle de structure (temps plein)", etp_ok=False, rapport=r)
                else:
                    cel = cellule_pays(V1, code, st, pays)
                if cel is None:
                    continue
                n += 1
                t = C2.triplet(base, pays, resid, poste=base["poste"], statut=None, cellule=cel, ident=f"{code}-{pays}{'f' if resid == 'FR-LO' else ''}-{st[:3]}")
                t["statut"] = C2.type_statut(base) if not t["statut"] else t["statut"]
                t.update(code=code, poste_rep=base["poste_rep"], langue=0, cle_mc=code)
                V.append(t)
    # Administrateur de l'UE a Luxembourg (v7, impot de l'UE estime a 18 %).
    ad = next(t for t in C2.R2 if t["poste"].startswith("Administrateur (AD)"))
    ad = copy.deepcopy({k: v for k, v in ad.items() if k not in ("mc", "rangs_var", "prov", "modifs")})
    ad.update(code="2422", citp="2422", poste="2422 " + NOMS_CITP["2422"], poste_rep="administrateur (AD) de l'UE",
              id="2422-LU-ue", langue=0, cle_mc="2422")
    V.append(ad)
    return V


V2 = variantes_r2(V1)
SEL2, CL2, B2 = calculer(V2)

if __name__ == "__main__":
    for nom, cl, V in (("Classement 1", CL1, V1), ("Classement 2 (10 pays)", CL2, V2)):
        print(nom, ":", len(V), "variantes,", len(cl), "codes")
        for i, t in enumerate(cl[:20], 1):
            mc = t["mc"]
            print(f"{i:3d} {t['rang']:3d}{'=' if t['groupe_eg'] > 1 else ' '} {t['id']:16s} {t['poste'][:44]:44s} ({t['poste_rep'][:30]}) {t['statut'][:12]:12s} "
                  f"{t['pays']}/{t['resid']:5s} {t['palier']}{'*' if t['proche'] else ' '} W {t['W']:.3f} RE {t['RE']:.2f} "
                  f"{t['med_ai_ppa'] / 1000:.0f}k P10 A {mc['A']['p_top']:.2f} B {mc['B']['p_top']:.2f} C {mc['C']['p_top']:.2f} D {mc['D']['p_top']:.2f} P1 {mc['A']['p_1']:.3f} [{t['fiab'][:24]}]")
