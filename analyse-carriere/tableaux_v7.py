# -*- coding: utf-8 -*-
"""Genere tableaux_v7.md (tableaux du rapport, version 7) a partir de pays_v7, modele_v7 et classement2_v7."""
import json
import os
import re
from collections import Counter, defaultdict

import classement2_v7 as C2
import fiscalite_v7 as F
import modele_v7 as M7
import pays_v7 as PV

ICI = os.path.dirname(os.path.abspath(__file__))
R1, CL1 = M7.R1, M7.CLASSEMENT1
R2, CL2 = C2.R2, C2.CLASSEMENT2
NOM_PAYS = dict(PV.NOMS)
DIMS6 = M7.DIMS6
L = []


def k(x):
    return f"{x / 1000:.0f}"


def lieu(t):
    p = NOM_PAYS[t["pays"]]
    if t["pays"] in ("CH", "LU"):
        return p + (" (frontalier)" if t["resid"] in ("FR-GE", "FR-LO") else " (résident)")
    return p


def triplet(t):
    return f"{t['poste']} × {t['statut']} × {lieu(t)}"


def rang(t, cle="rang", groupe="groupe_eg"):
    return f"{t[cle]}{'=' if t.get(groupe, 1) > 1 else ''}"


def palier(t):
    return t["palier"] + ("*" if t["proche"] else "")


IA_NOM = {"faible": "faible", "moyenne": "moyenne", "elevee": "élevée"}


def pct(x):
    return f"{100 * x:.0f} %"


def pct1(x):
    return f"{100 * x:.1f} %"


def statut_note(t, d):
    s, codes, tensions = t["prov"][d]
    lettre = {"sourcée": "S", "mixte": "M", "estimée": "E"}[s]
    return lettre + (f" ({', '.join(codes)})" if codes else "") + (f", tension {', '.join(tensions)}" if tensions else "")


def section(titre):
    L.append(f"### {titre}\n")


def table(entetes, lignes):
    L.append("| " + " | ".join(entetes) + " |")
    L.append("|" + "---|" * len(entetes))
    for l in lignes:
        L.append("| " + " | ".join(str(c) for c in l) + " |")
    L.append("")


# ---------------------------------------------------------------------------
# A. Tri des pays
# ---------------------------------------------------------------------------
section("Tri des pays : 40 pays, trois piliers, 10 retenus")
lignes = []
for i, c in enumerate(PV.RANG, 1):
    b = PV.BASE[c]
    net, h = PV.NET[c], PV.HEURES[c]
    st = PV.STRAIN.get(c)
    lignes.append([i, NOM_PAYS[c], f"{net[0]:,} ({net[1]})".replace(",", " "), f"{h[0]:,} ({h[1]})".replace(",", " "),
                   f"{st[0]} % ({st[1]})" if st else "sans donnée comparable (médiane)",
                   pct(PV.P_TOP10[c]), "oui" if c in PV.RETENUS else "non"])
table(["Rang", "Pays", "Net au salaire moyen, USD PPA 2025 (provenance)", "Heures par an (provenance)",
       "Tension au travail 2021 (provenance)", "P(10 premiers), 10 000 tirages", "Retenu"], lignes)
L.append("Lecture : l'ordre suit la moyenne des trois piliers ramenés à [0, 1] (règle 1.15) ; l'indice lui-même n'est pas affiché "
         "(pas de score décimal). « lu » : lu dans une source pendant l'analyse ; « imputé » : calculé ou borné à partir de chiffres lus ; "
         "« connu » : chiffre OCDE connu avant l'analyse, non revérifié. Sources : S167 (revenu), S168 à S172 (heures), S173 (tension).\n")
hors = [c for c in PV.PAYS if c not in PV.EUROPE]
L.append("Pays hors Europe sans donnée comparable de tension au travail (enquête européenne EWCTS 2021) : "
         + ", ".join(NOM_PAYS[c] for c in hors) + ". En Europe, l'Islande, le Royaume-Uni et la Türkiye n'ont pas non plus de valeur "
         "publiée. Aucun pays hors Europe n'entre dans les 10 premiers : le meilleur, le Canada, est 15e (5 % des tirages dans les 10 premiers).\n")

# ---------------------------------------------------------------------------
# B. Classement 1
# ---------------------------------------------------------------------------
section(f"Classement 1, catalogue des postes ({len(R1)} triplets)")
lignes = []
for t in sorted(R1, key=lambda t: (t["pays"], t["poste"], t["resid"])):
    lignes.append([t["id"], t["poste"], t["citp"], t["statut"], lieu(t), t["src"] or "nouveau", t["just"] or ""])
table(["ID", "Poste exact", "CITP-08", "Statut", "Pays", "Origine v6", "Écart à la note d'origine, justification"], lignes)


def table_classement(cl, avec_p=True):
    lignes = []
    for t in cl:
        mc = t["mc"]["A"]
        lignes.append([rang(t), t["id"], triplet(t), t["EP"], t["IT"], t["QT"], t["ES"], f"{t['CA']:.1f}", t["PS"],
                       f"{t['RE']:.1f}", palier(t), t["nb_top"], pct(mc["p_top"])])
    table(["Rang", "ID", "Triplet", "EP", "IT", "QT", "ES", "CA", "PS", "RE", "Palier", "Top 10 (sur 8 pondérations)",
           "P(10 premiers), variante A"], lignes)


section("Classement 1, partie A : notes des 7 dimensions, palier et probabilité d'être dans les 10 premiers")
table_classement(CL1)
c1 = Counter(t["palier"] for t in R1)
L.append(f"Paliers : S {c1['S']}, A {c1['A']}, B {c1['B']}, C {c1['C']}. « 2= » : rang partagé (écart inférieur à 0,03). "
         "* : à moins de 0,1 d'une frontière.\n")


def table_revenu(cl):
    lignes = []
    for t in cl:
        cur = t["cur"]
        lignes.append([t["id"], triplet(t), f"{k(t['med'])} / {k(t['p80'])} k{cur}", pct(t["taux_impot"]),
                       f"{k(t['med_ai_nom'])} / {k(t['med_ai_ppa'])}", f"{k(t['p80_ai_nom'])} / {k(t['p80_ai_ppa'])}",
                       t["fiab"], t["src_med"]])
    table(["ID", "Triplet", "Cellule avant impôt, médiane / P80", "Impôt (médiane)", "Médiane après impôt, k€ change / PPA",
           "P80 après impôt, k€ change / PPA", "Fiabilité", "Source de la médiane"], lignes)


section("Classement 1, partie B : revenu net après impôt, en équivalent temps plein")
table_revenu(CL1)
L.append("Lecture : « X / Y » = milliers d'euros au change 2025 sans ajustement, puis en parité de pouvoir d'achat au niveau des prix "
         "français ; le score utilise Y. Impôt = part de la cellule (nette de cotisations) prélevée par l'impôt sur le revenu. "
         f"Bornes de l'échelle logarithmique du classement 1 : médiane {k(M7.B1['med_ai_ppa'][0])} à {k(M7.B1['med_ai_ppa'][1])} k€, "
         f"P80 {k(M7.B1['p80_ai_ppa'][0])} à {k(M7.B1['p80_ai_ppa'][1])} k€ PPA.\n")


def table_prov(cl):
    lignes = []
    for t in cl:
        lignes.append([t["id"], triplet(t)] + [statut_note(t, d) for d in DIMS6])
    table(["ID", "Triplet"] + list(DIMS6), lignes)


section("Classement 1, partie C : provenance des notes hors revenu")
cnt = Counter(t["prov"][d][0] for t in R1 for d in DIMS6)
L.append(f"Sur {6 * len(R1)} notes : {cnt['sourcée']} sourcées (S), {cnt['mixte']} mixtes (M, dont les {len(R1)} notes CA), "
         f"{cnt['estimée']} estimées (E). Codes d'ancrage : section 1.13 et 1.14.\n")
table_prov(CL1)


def table_poids(cl, n=30):
    noms = list(M7.VARIANTES_POIDS)
    lignes = []
    for t in cl[:n]:
        lignes.append([t["id"], triplet(t)] + [t["rangs_var"][v] for v in noms] + [f"{t['rang_min']} à {t['rang_max']}"])
    table(["ID", "Triplet"] + [v.replace(" doublé", " ×2") for v in noms] + ["Étendue"], lignes)


section("Classement 1, partie D : rang dans chacune des 8 pondérations (30 premiers)")
table_poids(CL1)


def table_mc(T, n=30):
    tri = sorted(T, key=lambda t: (-t["mc"]["A"]["p_top"], t["id"]))[:n]
    lignes = []
    for t in tri:
        mc = t["mc"]
        lignes.append([t["id"], triplet(t)] + [pct(mc[v]["p_top"]) for v in "ABCDE"]
                      + [pct1(mc[v]["p_1"]) for v in "ABDE"]
                      + [f"{mc['A']['r_med']} [{mc['A']['r_p5']} à {mc['A']['r_p95']}]", mc["A"]["n_var"]])
    table(["ID", "Triplet", "P(10 premiers) A", "B", "C", "D", "E", "P(1er) A", "B", "D", "E",
           "Rang médian A [5e à 95e centile]", "Notes tirées (A)"], lignes)


section("Classement 1, partie E : robustesse aux notes et au revenu, 10 000 tirages")
L.append("Variantes : " + " ; ".join(f"{v} {d}" for v, d in M7.VARIANTES_MC.items()) + ". La variante E a été ajoutée après le "
         "premier calcul du classement 2, à titre informatif : un même poste transposé dans plusieurs pays porte la même note estimée, "
         "son écart doit donc être commun. La règle de désignation d'un 1er reste celle de la variante A (1.15).\n")
table_mc(R1)
best = {v: max(R1, key=lambda t: t["mc"][v]["p_1"]) for v in "ABCDE"}
L.append("Plus forte probabilité d'être 1er : " + " ; ".join(f"{v} {b['id']} ({pct1(b['mc'][v]['p_1'])})" for v, b in best.items())
         + ". Aucune ne dépasse 50 % : pas de 1er désigné.\n")


def egalites(cl):
    groupes = defaultdict(list)
    for t in cl:
        if t["groupe_eg"] > 1:
            groupes[t["rang"]].append(t["id"])
    return groupes


section("Classement 1, partie F : égalités, frontières de palier, scénario IA fort, sensibilité aux tensions")
g = egalites(CL1)
L.append("Égalités déclarées (écart inférieur à 0,03 avec le premier du groupe) : "
         + " ; ".join(f"rang {r} : {', '.join(ids)}" for r, ids in sorted(g.items())[:12]) + ".\n")
proches = [t for t in CL1 if t["proche"]]
L.append(f"À moins de 0,1 d'une frontière : {len(proches)} triplets ; dans les 30 premiers : "
         + ", ".join(f"{t['id']} ({t['palier']})" for t in CL1[:30] if t["proche"]) + ".\n")
lignes = []
for t in CL1[:30]:
    lignes.append([t["id"], triplet(t), IA_NOM[t["ia"]], palier(t), t["palier_ia"], rang(t), t["rang_tension"]])
table(["ID", "Triplet", "Exposition IA", "Palier", "Palier, IA fort (informatif)", "Rang", "Rang, tensions résolues (informatif)"],
      lignes)


section("Classement 1, partie G : modifications par rapport à la version 6 (triplets repris)")
v6 = json.load(open(os.path.join(ICI, "rangs_v6.json"), encoding="utf-8"))
lignes = []
for t in sorted((t for t in R1 if t["src"] in v6 and t["id"] in v6), key=lambda t: t["rang"]):
    o = v6[t["id"]]
    notes_id = all(abs(o[d] - t[d]) < 1e-9 for d in DIMS6)
    lignes.append([t["id"], t["poste"], f"{o['rang']}", rang(t), f"{o['RE']:.1f}", f"{t['RE']:.1f}", o["palier"], t["palier"],
                   "identiques" if notes_id else "modifiées"])
table(["ID", "Poste", "Rang v6 (93 triplets, 7 pays)", "Rang v7 (classement 1)", "RE v6 (avant impôt)", "RE v7 (après impôt)",
       "Palier v6", "Palier v7", "Notes hors revenu"], lignes)
L.append("Causes déclarées : (1) revenu après impôt sur le revenu (1.15) ; (2) nouveau pool (postes précis, pays limités à la France "
         "et à la Suisse), donc nouvelles bornes de l'échelle de revenu ; (3) T01 devient F01 (source CARMF 2023 commune aux "
         "spécialités). Les notes hors revenu des triplets repris sont identiques à la v6 (contrôle automatique : 0 écart).\n")

# ---------------------------------------------------------------------------
# C. Classement 2
# ---------------------------------------------------------------------------
section("Classement 2, postes retenus et transposition")
lignes = []
for cp in C2.CLES2:
    base = C2.meilleur(cp)
    pays = [p for p in C2.PAYS2 if any(t["cle_mc"] == "|".join(cp) and t["pays"] == p for t in R2)]
    lignes.append([cp[0], cp[1], base["id"], "contrôle" if cp in C2.AJOUTES2 else "30 premiers", ", ".join(pays)])
table(["Poste", "Statut", "Notes de base (classement 1)", "Entrée", "Pays"], lignes)
L.append(f"{len(C2.CLES2)} postes, dont {len(C2.AJOUTES2)} ajoutés par le contrôle (score maximal possible supérieur ou égal au "
         f"10e score du classement 2) ; {len(R2)} triplets. Spécialistes hospitaliers (grille commune) en "
         + ", ".join(NOM_PAYS[p] for p in C2.PAYS_HOSP) + " ; administrateur de l'UE à Luxembourg.\n")

section("Classement 2, revenus : données lues et règle de structure")
lignes = []
for t in sorted((t for t in R2 if t["pays"] != "CH" and not t["fiab"].startswith("estimé")), key=lambda t: (t["pays"], t["poste"])):
    lignes.append([t["id"], triplet(t), f"{t['med']:,.0f} {t['cur']}".replace(",", " "), t["fiab"], t["src_med"]])
table(["ID", "Triplet", "Brut médian", "Fiabilité", "Source"], lignes)
lignes = []
vus = set()
for t in R2:
    if t["fiab"] == "estimé (structure)" and t["poste"] not in vus:
        vus.add(t["poste"])
        lignes.append([t["poste"], t["statut"], f"{t['rapport']:.2f}", t["src_med"].split(" × salaire moyen")[0]])
table(["Poste", "Statut", "Rapport au salaire moyen appliqué", "Base"], lignes)
lignes = [[NOM_PAYS[p], f"{C2.AW[p][0]:,} {C2.CUR[p]}".replace(",", " "), C2.AW[p][1], f"{C2.PLI[p]}".replace(".", ","), C2.PLI_PROV[p],
           f"{C2.ppa(p, p):.3f}"] for p in ["FR"] + C2.PAYS2 if p in C2.AW and p in C2.PLI]
table(["Pays", "Salaire moyen OCDE 2025", "Provenance", "Niveau des prix 2024 (UE = 100)", "Provenance", "€ PPA France par unité locale"],
      lignes)
n_struct = sum(1 for t in R2 if t["fiab"] == "estimé (structure)")
L.append(f"{n_struct} cellules sur {len(R2)} viennent de la règle de structure (estimées), toutes hors Suisse ; "
         f"les {sum(1 for t in R2 if t['pays'] == 'CH')} triplets suisses reprennent les cellules du classement 1.\n")

section("Classement 2, partie A : notes, palier et probabilité d'être dans les 10 premiers (60 premiers)")
table_classement(CL2[:60])
c2 = Counter(t["palier"] for t in R2)
L.append(f"Paliers sur les {len(R2)} triplets : S {c2['S']}, A {c2['A']}, B {c2['B']}, C {c2['C']}. Tableau complet dans "
         "`resultats_v7.json`.\n")

section("Classement 2, partie B : meilleur triplet de chaque pays et part des 10 premières places")
som = defaultdict(float)
meill = {}
for t in CL2:
    som[t["pays"]] += t["mc"]["A"]["p_top"]
    meill.setdefault(t["pays"], t)
lignes = []
for p in sorted(som, key=lambda p: -som[p]):
    t = meill[p]
    lignes.append([NOM_PAYS[p], f"{som[p]:.1f}".replace(".", ","), rang(t), t["id"], triplet(t), palier(t), pct(t["mc"]["A"]["p_top"]),
                   "non couvert par l'EWCTS 2021" if p in C2.EWCTS_ABSENT else "couvert"])
table(["Pays", "Places attendues dans les 10 premiers (somme des probabilités, A)", "Rang du meilleur", "ID", "Meilleur triplet",
       "Palier", "P(10 premiers)", "Enquête européenne 2021"], lignes)

section("Classement 2, partie C : revenu net après impôt (60 premiers)")
table_revenu(CL2[:60])
L.append(f"Bornes de l'échelle du classement 2 : médiane {k(C2.B2['med_ai_ppa'][0])} à {k(C2.B2['med_ai_ppa'][1])} k€, "
         f"P80 {k(C2.B2['p80_ai_ppa'][0])} à {k(C2.B2['p80_ai_ppa'][1])} k€ PPA.\n")

section("Classement 2, partie D : provenance des notes (60 premiers)")
cnt2 = Counter(t["prov"][d][0] for t in R2 for d in DIMS6)
L.append(f"Sur {6 * len(R2)} notes : {cnt2['sourcée']} sourcées, {cnt2['mixte']} mixtes, {cnt2['estimée']} estimées. Hors Suisse, "
         "aucune note n'est sourcée : les ancrages viennent de France, de Suisse ou de l'UE, donc au mieux mixtes (1.13).\n")
table_prov(CL2[:60])

section("Classement 2, partie E : rang dans les 8 pondérations (30 premiers)")
table_poids(CL2)

section("Classement 2, partie F : robustesse aux notes et au revenu, 10 000 tirages")
table_mc(R2)
best2 = {v: max(R2, key=lambda t: t["mc"][v]["p_1"]) for v in "ABCDE"}
L.append("Plus forte probabilité d'être 1er : " + " ; ".join(f"{v} {b['id']} ({pct1(b['mc'][v]['p_1'])})" for v, b in best2.items())
         + ". Aucune ne dépasse 50 % : pas de 1er désigné.\n")

section("Classement 2, partie G : sensibilité sans la règle de langue (informatif)")
tri = sorted(R2, key=lambda t: (C2.RANG_SANS_LANGUE[t["id"]][0], t["id"]))[:20]
lignes = [[C2.RANG_SANS_LANGUE[t["id"]][0], t["id"], triplet(t), rang(t)] for t in tri]
table(["Rang sans la règle", "ID", "Triplet", "Rang avec la règle"], lignes)

section("Classement 2, partie H : égalités et frontières")
g = egalites(CL2)
L.append("Égalités dans les 40 premiers : " + " ; ".join(f"rang {r} : {', '.join(ids)}" for r, ids in sorted(g.items()) if r <= 40) + ".\n")
L.append("À moins de 0,1 d'une frontière dans les 40 premiers : " + ", ".join(f"{t['id']} ({t['palier']})" for t in CL2[:40] if t["proche"]) + ".\n")

# ---------------------------------------------------------------------------
# D. Verification fiscale et cellules signalees
# ---------------------------------------------------------------------------
section("Vérification des barèmes au salaire moyen")
lignes = []
for c, (aw, taux, cible, prov) in F.verification().items():
    lignes.append([NOM_PAYS[c], f"{aw:,}".replace(",", " "), pct1(taux), pct1(cible), f"{100 * (taux - cible):+.1f}".replace("+", "plus ").replace("-", "moins "), prov])
table(["Pays", "Salaire moyen 2025 (monnaie locale)", "Impôt et cotisations salariales calculés", "Cible OCDE", "Écart (points)", "Provenance de la cible"], lignes)
L.append("Cibles : taux moyen publié (S167) ou déduit du coin fiscal publié (S183) avec une part patronale estimée. Genève : points lus "
         "16,5 % à 100 000 CHF, 22,5 % à 200 000, 25 % à 300 000 (S179). France : contrôle à 100 000 € de bénéfice libéral, impôt de 26,7 %.\n")

section("Cellules revenu signalées (classement 1)")
lignes = []
for t in CL1:
    if M7.incertaine(t) or not t["etp_ok"]:
        lignes.append([t["id"], triplet(t), t["fiab"], "oui" if t["etp_ok"] else "non : " + t["etp"]])
table(["ID", "Triplet", "Fiabilité", "Temps de travail réel connu"], lignes)


# ---------------------------------------------------------------------------
# E. Groupes de tete et scenarios IA (conclusions)
# ---------------------------------------------------------------------------
import modele as M6


def groupe_tete(T, titre, seuil=0.20):
    section(titre)
    tete = sorted([t for t in T if t["mc"]["A"]["p_top"] >= seuil], key=lambda t: (-t["mc"]["A"]["p_top"], t["id"]))
    lignes = []
    for t in tete:
        c = Counter(t["prov"][d][0][0] for d in DIMS6)
        mc = t["mc"]
        lignes.append([t["id"], triplet(t), pct(mc["A"]["p_top"]), f"{pct(min(mc[v]['p_top'] for v in 'ABCDE'))} à {pct(max(mc[v]['p_top'] for v in 'ABCDE'))}",
                       pct1(mc["A"]["p_1"]), rang(t), palier(t), t["palier_ia"],
                       f"{k(t['med_ai_nom'])} / {k(t['med_ai_ppa'])}", t["fiab"], f"S {c['s']}, M {c['m']}, E {c['e']}"])
    table(["ID", "Triplet", "P(10 premiers), A", "Étendue sur A à E", "P(1er), A", "Rang", "Palier", "Palier, IA fort",
           "Médiane après impôt, k€ change / PPA", "Fiabilité du revenu", "Notes hors revenu"], lignes)
    meilleur = max(T, key=lambda t: t["mc"]["A"]["p_1"])
    L.append(f"Seuil de présentation : 20 % de chances d'être dans les 10 premiers (variante A), choix d'affichage aussi arbitraire "
             f"qu'une frontière de palier ; {len(tete)} triplets. Plus forte probabilité d'être 1er : {meilleur['id']}, "
             f"{pct1(meilleur['mc']['A']['p_1'])} : sous 50 %, aucun 1er n'est désigné (règle 1.15).\n")


def scenarios_ia(T, titre):
    section(titre)
    r_ia = M6.rangs_partages(T, cle="W_ia")
    base = sorted(T, key=lambda t: (-t["W"], t["id"]))[:10]
    fort = sorted(T, key=lambda t: (-t["W_ia"], t["id"]))[:10]
    lignes = []
    for i in range(10):
        a, b = base[i], fort[i]
        lignes.append([i + 1, f"{a['id']} {triplet(a)} ({IA_NOM[a['ia']]})", f"{b['id']} {triplet(b)} ({IA_NOM[b['ia']]}, rang de base {rang(b)})",
                       f"{r_ia[b['id']][0]}"])
    table(["Place", "Scénario 1 : IA sans effet sur l'emploi (classement de base)",
           "Scénario 2 : IA fort (PS moins 1 ou 2, revenu brut × 0,9 ou × 0,8 selon l'exposition)", "Rang partagé, scénario 2"], lignes)
    L.append("Scénarios bornés déclarés en v2 et inchangés ; exposition notée faible, moyenne ou élevée par poste (estimation, "
             "poids de preuve faible) ; fonctionnaires : choc réduit d'un cran.\n")


groupe_tete(R1, "Classement 1, groupe de tête")
scenarios_ia(R1, "Classement 1, deux scénarios IA")
groupe_tete(R2, "Classement 2, groupe de tête")
scenarios_ia(R2, "Classement 2, deux scénarios IA")

texte = "\n".join(L)
texte = re.sub(r"(?<=\d)\.(?=\d)", ",", texte)
texte = re.sub(r"(section|grille|règle|règles) 1,(\d+)", r"\1 1.\2", texte)
texte = re.sub(r"\((1),(1[0-5])\)", r"(\1.\2)", texte)
with open(os.path.join(ICI, "tableaux_v7.md"), "w", encoding="utf-8") as f:
    f.write(texte + "\n")


def export(T):
    out = []
    for t in T:
        out.append({k: (sorted(v) if isinstance(v, set) else v) for k, v in t.items()
                    if k not in ("net_de_brut",) and not callable(v)})
    return out


with open(os.path.join(ICI, "resultats_v7.json"), "w", encoding="utf-8") as f:
    json.dump({"classement1": export(CL1), "classement2": export(CL2),
               "pays": {c: dict(PV.BASE[c], p_top10=PV.P_TOP10[c]) for c in PV.PAYS}}, f, ensure_ascii=False, indent=1, default=float)
print("tableaux_v7.md :", len(texte), "caractères")
