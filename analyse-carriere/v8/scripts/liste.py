import csv, sys, collections
src, out = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(src, encoding="utf-8-sig"), delimiter=";"))
dom = collections.OrderedDict()
for r in rows:
    dom.setdefault((r["Code FAP 22"], r["Intitulé FAP 22"]), []).append(r)
EXCLUS = {"X"}
lines = ["# Liste neutre des métiers : FAP-2021 de la DARES, niveau le plus fin (341 métiers)", "",
         "Source : DARES, nomenclature des familles professionnelles 2021 (export open data, 341 lignes) : "
         "https://data.dares.travail-emploi.gouv.fr/explore/dataset/dares_nomenclature_fap2021/", "",
         "Règle : tous les métiers de la nomenclature, dans l'ordre et avec l'intitulé officiel ; seul le domaine X "
         "(politique, religion : mandat électif et ministère religieux) est proposé à l'exclusion.", "",
         "| Domaine | Métiers (341) | Familles détaillées (228) |", "|---|---|---|"]
tot = [0, 0]
for (c, l), rs in dom.items():
    n341 = len({r["Code FAP 341"] for r in rs}); n228 = len({r["Code FAP 228"] for r in rs})
    tag = " (exclusion proposée)" if c in EXCLUS else ""
    lines.append(f"| {c} {l}{tag} | {n341} | {n228} |")
    if c not in EXCLUS: tot[0] += n341; tot[1] += n228
lines += [f"| **Total retenu** | **{tot[0]}** | **{tot[1]}** |", ""]
for (c, l), rs in dom.items():
    lines += [f"## {c} — {l}" + (" (exclusion proposée)" if c in EXCLUS else ""), "",
              "| Code FAP 341 | Métier (intitulé officiel) | Famille détaillée (FAP 228) |", "|---|---|---|"]
    for r in sorted(rs, key=lambda r: r["Code FAP 341"]):
        lines.append(f"| {r['Code FAP 341']} | {r['Intitulé FAP 341']} | {r['Code FAP 228']} {r['Intitulé FAP 228']} |")
    lines.append("")
open(out, "w", encoding="utf-8").write("\n".join(lines))
print(tot)
