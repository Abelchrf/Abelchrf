# -*- coding: utf-8 -*-
"""Version 6 (29 octobre 2026) : robustesse du classement aux notes estimees (section 1.14 du rapport).

Tirages aleatoires a poids egaux, regles declarees avant calcul :
- A (consigne) : chaque note de statut E (estimee) recoit un ecart tire dans {-1, 0, +1} avec la meme
  probabilite, independamment, puis est bornee a [1, 5]. Notes S et M, CA et revenu inchanges.
- B (correlee) : comme A, mais l'ecart de EP et de IT est commun a tout un groupe de metiers, puisque ces
  deux notes viennent d'une grille par groupe ; les autres notes E restent independantes.
- C (elargie) : notes E et M tirees comme en A ; CA (moitie estimee : la latitude) tiree dans
  {-0,5 ; 0 ; +0,5} ; seules les notes S et le revenu restent fixes.
Rang dans un tirage : 1 + nombre de triplets au score strictement plus eleve (sans la regle d'egalite de
0,03 : les tirages mesurent eux-memes l'incertitude). P(1er) : en cas d'egalite exacte en tete, la
premiere place est partagee a parts egales.
"""
import numpy as np

import eurofound as EU

N_TIRAGES = 10_000
GRAINE = 20261029
DIMS6 = ("EP", "IT", "QT", "ES", "CA", "PS")
VARIANTES = {"A": "notes estimées, tirages indépendants (consigne)",
             "B": "notes estimées, EP et IT communs au groupe de métiers",
             "C": "notes estimées et mixtes, CA à ± 0,5"}


def tirages(T, variante, n=N_TIRAGES, graine=GRAINE, top=10):
    rng = np.random.default_rng(graine)
    k = len(T)
    base = np.array([[t[d] for d in DIMS6] for t in T], dtype=float)
    re_ = np.array([t["RE"] for t in T], dtype=float)
    statut = np.array([[t["prov"][d][0] for d in DIMS6] for t in T])
    variable = (statut == "estimée") if variante in ("A", "B") else (statut != "sourcée")
    if variante in ("A", "B"):
        variable[:, DIMS6.index("CA")] = False
    pas = np.ones((k, len(DIMS6)))
    if variante == "C":
        pas[:, DIMS6.index("CA")] = 0.5
    ecarts = rng.integers(-1, 2, size=(n, k, len(DIMS6))).astype(float)
    if variante == "B":
        groupes = sorted(EU.GROUPES)
        idx = np.array([groupes.index(EU.groupe_de(t["id"])[0]) for t in T])
        commun = rng.integers(-1, 2, size=(n, len(groupes), 2)).astype(float)
        ecarts[:, :, 0] = commun[:, idx, 0]
        ecarts[:, :, 1] = commun[:, idx, 1]
    notes = np.clip(base[None, :, :] + ecarts * pas[None, :, :] * variable[None, :, :], 1, 5)
    scores = (notes.sum(axis=2) + re_[None, :]) / 7
    p_top = np.zeros(k)
    p_1 = np.zeros(k)
    rangs = np.zeros((n, k), dtype=np.int32)
    for i in range(0, n, 1000):
        s = scores[i:i + 1000]
        r = (s[:, None, :] > s[:, :, None]).sum(axis=2) + 1
        rangs[i:i + 1000] = r
        p_top += (r <= top).sum(axis=0)
        en_tete = np.isclose(s, s.max(axis=1, keepdims=True), rtol=0, atol=1e-12)
        p_1 += (en_tete / en_tete.sum(axis=1, keepdims=True)).sum(axis=0)
    out = {}
    for j, t in enumerate(T):
        out[t["id"]] = {"p_top": p_top[j] / n, "p_1": p_1[j] / n,
                        "r_med": int(np.median(rangs[:, j])),
                        "r_p5": int(np.percentile(rangs[:, j], 5)), "r_p95": int(np.percentile(rangs[:, j], 95)),
                        "n_var": int(variable[j].sum())}
    return out


def tout(T):
    return {v: tirages(T, v) for v in VARIANTES}
