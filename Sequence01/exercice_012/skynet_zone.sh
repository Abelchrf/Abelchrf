#!/bin/bash
#
# Exercice 012 : Générer une zone DNS à partir d'une liste de machines
#
# Usage : sudo ./skynet_zone.sh [skynetHostIPs.csv]
#         (par défaut : skynetHostIPs.csv placé à côté du script)
#
# Chaque ligne du CSV contient un nom de machine et une IP (dans n'importe
# quel ordre, séparés par , ou ; ou tabulation ou espace). Les lignes sans
# IP (en-tête) et les IP invalides (10.0.0.800) sont ignorées.
#   1. awk transforme chaque ligne en enregistrement DNS : "nom IN A ip"
#   2. le résultat va dans /etc/bind/db.<domaine>.skynet, inclus dans la zone
#      principale par $INCLUDE (on ne touche pas aux exercices 009 à 011)
#   3. serial + 1, named-checkzone, rechargement, systemctl status bind9
#   4. test de quelques noms avec dig

set -u

CSV="${1:-$(dirname "$0")/skynetHostIPs.csv}"
DOMAIN="je-le-trouve-beau-mon-domain-donc-il-est-beau.com"
ZONE_FILE="/etc/bind/db.$DOMAIN"
HOSTS_FILE="/etc/bind/db.$DOMAIN.skynet"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -r "$CSV" ]] || { echo "Fichier introuvable : $CSV" >&2; exit 1; }
[[ -f "$ZONE_FILE" ]] || { echo "Lancer d'abord l'exercice 009." >&2; exit 1; }

# 1. Génération des enregistrements
#    tr -d '\r"'  : enlève les fins de ligne Windows et les guillemets
#    awk : sur chaque ligne, le champ qui ressemble à une IP valide (4 nombres
#          de 0 à 255) est l'adresse, le premier autre champ est le nom.
tr -d '\r"' < "$CSV" | awk -F'[,;\t]' '
function valid_ip(s,   p, n, i) {
    if (s !~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) return 0
    n = split(s, p, ".")
    for (i = 1; i <= n; i++) if (p[i] > 255) return 0
    return 1
}
{
    if (NF == 1) NF = split($0, f, " ")         # fichier séparé par des espaces
    else         split($0, f, /[,;\t]/)
    ip = ""; name = ""; bad = ""
    for (i = 1; i <= NF; i++) {
        v = f[i]; gsub(/^ +| +$/, "", v)          # espaces autour
        if (valid_ip(v)) ip = v
        else if (v ~ /^[0-9.]+$/ && v ~ /\./) bad = v
        else if (name == "" && v != "" && v !~ /^[0-9]+$/) name = v
    }
    if (bad != "" && ip == "") { print "IP invalide ignorée : " $0 > "/dev/stderr"; next }
    if (ip == "" || name == "") next          # en-tête ou ligne vide
    name = tolower(name)
    gsub(/[^a-z0-9.-]/, "-", name)            # "Skynet Core" -> skynet-core
    sub(/\.$/, "", name)
    printf "%-30s IN  A  %s\n", name, ip
}' > "$HOSTS_FILE.new"

count=$(wc -l < "$HOSTS_FILE.new")
if [[ $count -eq 0 ]]; then
    echo "Aucune ligne 'nom + IP' trouvée dans $CSV" >&2
    rm -f "$HOSTS_FILE.new"
    exit 1
fi
mv "$HOSTS_FILE.new" "$HOSTS_FILE"
echo "$count machines -> $HOSTS_FILE"
head -n 5 "$HOSTS_FILE"; echo "..."

# 2. La zone principale inclut ce fichier (une seule fois)
grep -q "^\$INCLUDE $HOSTS_FILE" "$ZONE_FILE" || echo "\$INCLUDE $HOSTS_FILE" >> "$ZONE_FILE"

# 3. serial + 1, vérification, rechargement
old=$(grep -oE '[0-9]+ *; serial' "$ZONE_FILE" | grep -oE '^[0-9]+')
sed -i "s/$old *; serial/$((old + 1)) ; serial/" "$ZONE_FILE"

named-checkzone "$DOMAIN" "$ZONE_FILE" || exit 1
rndc reload "$DOMAIN"
systemctl status bind9 --no-pager | head -n 5

# 4. Test des 3 premières machines
sleep 1
for name in $(awk '{print $1}' "$HOSTS_FILE" | head -n 3); do
    echo "--- $name.$DOMAIN -> $(dig +short "$name.$DOMAIN" @127.0.0.1)"
done
