"""Lecteur xlsx minimal (bibliotheque standard) : feuilles -> listes de lignes."""
import re, sys, zipfile
import xml.etree.ElementTree as ET
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
def col(ref):
    c = 0
    for ch in re.sub(r"\d", "", ref):
        c = c * 26 + ord(ch) - 64
    return c - 1
def lire(path):
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    out = {}
    for s in wb.find("m:sheets", NS):
        t = rels[s.get("{%s}id" % NS["r"])]
        t = t[1:] if t.startswith("/") else "xl/" + t
        rows = []
        for r in ET.fromstring(z.read(t)).iter("{%s}row" % NS["m"]):
            row = {}
            for c in r.findall("m:c", NS):
                v = c.find("m:v", NS)
                val = v.text if v is not None else ""
                if c.get("t") == "s":
                    val = ss[int(val)]
                elif c.get("t") == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                row[col(c.get("r"))] = val
            rows.append([row.get(i, "") for i in range(max(row) + 1)] if row else [])
        out[s.get("name")] = rows
    return out
if __name__ == "__main__":
    for nom, rows in lire(sys.argv[1]).items():
        print("=== feuille", nom, len(rows))
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
        for r in rows[:n]:
            print(" | ".join(str(x)[:40] for x in r))
