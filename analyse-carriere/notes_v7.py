# -*- coding: utf-8 -*-
"""Version 7 : notes Eurofound et ancrages appliques a un triplet decrit par ses propres champs.

Meme methode que la v6 (sections 1.12 a 1.14, eurofound.py), generalisee aux postes v7 :
- notes de depart : EP et IT du poste, QT = 5 - F1 - F3 - H (H = 1 si controle <= 3, plancher 1),
  ES = relations - langue, CA = (controle + K(niveau CITP)) / 2, PS = securite ;
- ancrages : ceux du triplet v6 d'origine (champ src), moins anc_exclus, plus anc_extra ; un ancrage
  etendu a un poste qu'il ne couvre qu'en partie (anc_partiel) est au mieux mixte ;
- statut S seulement si le chiffre porte sur le metier, est quantitatif, officiel, du pays du triplet,
  hors QT et CA ; une contradiction S remplace la note, une contradiction M est une tension.
"""
import eurofound as EU

DIMS6 = ("EP", "IT", "QT", "ES", "CA", "PS")


def ancrages_de(t):
    out = []
    for a in EU.ANCRAGES:
        if a["code"] in t["anc_exclus"]:
            continue
        if t["src"] in a["ids"] or a["code"] in t["anc_extra"]:
            out.append(a)
    return out


def _cle(a, t):
    return t["src"]


def statut(a, t):
    s = (a["metier"] and a["quant"] and a["officiel"] and a["pays"] == t["pays"] and a["dim"] not in ("QT", "CA")
         and _cle(a, t) not in a["partiel"] and a["code"] not in t["anc_partiel"])
    return "S" if s else "M"


def compatibles(a, t):
    ok = a["ok"]
    if isinstance(ok, dict):
        return ok.get(_cle(a, t), set().union(*ok.values()))
    return ok


def accord(a, t, d):
    if a["dim"] == "QT":
        f = t["fx"]
        return all(ex is None or (fx in f) == ex for fx, ex in (("F1", a["f1"]), ("F3", a["f3"])))
    n = d[a["dim"]] + (t["langue"] if a["dim"] == "ES" else 0)
    return n in compatibles(a, t)


def qt(fx, c):
    return max(1, 5 - ("F1" in fx) - ("F3" in fx) - (1 if c <= 3 else 0))


def dims(t):
    return {"EP": t["EP"], "IT": t["IT"], "QT": qt(t["fx"], t["C"]), "ES": t["R"] - t["langue"],
            "CA": (t["C"] + EU.K_NIVEAU[t["niveau"]]) / 2, "PS": t["Se"]}


def ancrer(t):
    d = dims(t)
    liste = ancrages_de(t)
    modifs = []
    for a in liste:
        if statut(a, t) == "S" and not accord(a, t, d):
            lang = t["langue"] if a["dim"] == "ES" else 0
            n = d[a["dim"]] + lang
            nouveau = min(compatibles(a, t), key=lambda v: (abs(v - n), v)) - lang
            modifs.append((a["dim"], d[a["dim"]], nouveau, a["code"]))
            d[a["dim"]] = nouveau
    prov = {}
    for dim in DIMS6:
        aa = [a for a in liste if a["dim"] == dim]
        st = [statut(a, t) for a in aa]
        tensions = [a["code"] for a in aa if not accord(a, t, d)]
        if dim == "CA":
            prov[dim] = ("mixte", [], [])
        elif "S" in st:
            prov[dim] = ("sourcée", [a["code"] for a in aa], tensions)
        elif aa:
            prov[dim] = ("mixte", [a["code"] for a in aa], tensions)
        else:
            prov[dim] = ("estimée", [], [])
    return d, prov, modifs


def variante_tensions(t, d):
    """Informatif : notes en tension avec un ancrage mixte ramenees a la valeur compatible la plus proche."""
    d = dict(d)
    f = set(t["fx"])
    for a in ancrages_de(t):
        if accord(a, dict(t, fx=f), d):
            continue
        if a["dim"] == "QT":
            for fx, exige in (("F1", a["f1"]), ("F3", a["f3"])):
                if exige is not None:
                    (f.add if exige else f.discard)(fx)
            d["QT"] = qt(f, t["C"])
        else:
            lang = t["langue"] if a["dim"] == "ES" else 0
            n = d[a["dim"]] + lang
            d[a["dim"]] = min(compatibles(a, t), key=lambda v: (abs(v - n), v)) - lang
    return d
