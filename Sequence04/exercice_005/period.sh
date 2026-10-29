#!/bin/bash
#
# Exercice 5 : Extraire les événements d'une période
#
# Usage : sudo ./period.sh <début> <fin> [fichier ...]
#   exemples :
#     sudo ./period.sh "2026-10-29 08:00" "2026-10-29 09:30"
#     sudo ./period.sh "1 hour ago" "now" /var/log/auth.log
#     sudo ./period.sh "yesterday 22:00" "today 06:00"
#   (début et fin : tout ce que comprend la commande date -d)
#   fichiers : défaut = /var/log/syslog et /var/log/auth.log (+ leurs archives)
#
#   1. date -d transforme les bornes en "AAAA-MM-JJ HH:MM:SS".
#   2. awk lit la date au début de chaque ligne (2 formats possibles :
#      "2026-10-29T09:40:26.41+00:00" ou "Oct 29 09:40:26") et garde les
#      lignes dans la période.
#   3. sed rend les dates plus lisibles : 2026-10-29T09:40:26.413964+00:00
#      -> 2026-10-29 09:40:26
#   4. Sans fichiers texte (Debian 12 sans rsyslog) : journalctl --since --until.

set -u

if [[ $# -lt 2 ]]; then
    sed -n '3,12p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
fi
if [[ $EUID -ne 0 ]]; then
    echo "Lancer en root (sudo $0)." >&2
    exit 1
fi

# 1. Bornes
FROM=$(date -d "$1" '+%Y-%m-%d %H:%M:%S') || { echo "Date de début invalide : $1" >&2; exit 1; }
TO=$(date -d "$2" '+%Y-%m-%d %H:%M:%S') || { echo "Date de fin invalide : $2" >&2; exit 1; }
shift 2
if [[ "$FROM" > "$TO" ]]; then
    echo "Le début ($FROM) est après la fin ($TO)." >&2
    exit 1
fi
echo "Période : du $FROM au $TO"

if [[ $# -gt 0 ]]; then
    files=("$@")
else
    files=()
    for name in syslog auth.log; do
        for f in $(ls -1tr /var/log/"$name"* 2>/dev/null); do files+=("$f"); done
    done
fi

# 4. Pas de fichiers : journal systemd
if [[ ${#files[@]} -eq 0 ]]; then
    echo "(source : journal systemd)"
    journalctl --since "$FROM" --until "$TO" --no-pager -o short-iso
    exit 0
fi
echo "(source : ${files[*]})"
echo

# 2. Filtre awk + 3. dates lisibles avec sed
RESULT=$(mktemp)
trap 'rm -f "$RESULT"' EXIT
for f in "${files[@]}"; do
    zcat -f "$f" 2>/dev/null
done | awk -v from="$FROM" -v to="$TO" -v year="$(date +%Y)" '
    BEGIN {
        split("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec", m, " ")
        for (i = 1; i <= 12; i++) mon[m[i]] = sprintf("%02d", i)
    }
    {
        if ($1 ~ /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T/)
            ts = substr($1, 1, 10) " " substr($1, 12, 8)
        else if ($1 in mon)
            ts = year "-" mon[$1] "-" sprintf("%02d", $2) " " $3
        else
            next
        if (ts >= from && ts <= to) print
    }' \
    | sed -E 's/^([0-9-]{10})T([0-9:]{8})[.0-9]*([+-][0-9:]+|Z)?/\1 \2/' > "$RESULT"

echo "--- $(wc -l < "$RESULT") événements"
cat "$RESULT"
