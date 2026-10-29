#!/bin/bash
#
# Exercice 2 : Événements d'un utilisateur sur une plage horaire
#
# Usage : sudo ./user_events.sh [utilisateur] [début] [fin]
#   défaut : root, depuis aujourd'hui 00:00 jusqu'à maintenant
#   exemple : sudo ./user_events.sh root "2026-10-29 08:00" "2026-10-29 12:00"
#             sudo ./user_events.sh tbutchers "yesterday" "today"
#   (début et fin : tout ce que comprend la commande date -d)
#
#   1. date convertit les bornes au format "AAAA-MM-JJ HH:MM:SS".
#   2. On lit auth.log et syslog (y compris les anciens fichiers .1 et .gz),
#      on garde les lignes où le nom de l'utilisateur apparaît (grep -w).
#   3. awk garde celles dont l'heure est dans la plage (comparaison de textes :
#      "2026-10-29 09:00" < "2026-10-29 10:00", comme dans un dictionnaire).
#   4. Si /var/log n'a pas ces fichiers (Debian 12 sans rsyslog), on
#      interroge le journal systemd.
#   5. Résumé : nombre d'événements par programme (sudo, sshd, cron...).

set -u

USER_NAME="${1:-root}"
FROM=$(date -d "${2:-today 00:00}" '+%Y-%m-%d %H:%M:%S') || exit 1
TO=$(date -d "${3:-now}" '+%Y-%m-%d %H:%M:%S') || exit 1

if [[ $EUID -ne 0 ]]; then
    echo "Lancer en root (sudo $0)." >&2
    exit 1
fi
id "$USER_NAME" >/dev/null 2>&1 || echo "Attention : $USER_NAME n'existe pas (on cherche quand même)." >&2

echo "Événements de '$USER_NAME' du $FROM au $TO"
echo

# read_logs NOM : contenu de /var/log/NOM et de ses archives, du plus ancien
# au plus récent (zcat -f lit aussi bien les .gz que les fichiers normaux)
read_logs() {
    local f
    for f in $(ls -1tr /var/log/"$1"* 2>/dev/null); do zcat -f "$f"; done
}

# in_range : garde les lignes dont la date est entre FROM et TO.
# Deux formats de date existent dans les logs :
#   2026-10-29T09:40:26.413964+00:00 ...   (Debian 12)
#   Oct 29 09:40:26 ...                    (format classique, sans année)
in_range() {
    awk -v from="$FROM" -v to="$TO" -v year="$(date +%Y)" '
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
    }'
}

RESULT=$(mktemp)
trap 'rm -f "$RESULT"' EXIT

if [[ -f /var/log/auth.log || -f /var/log/syslog ]]; then
    echo "(source : /var/log/auth.log et /var/log/syslog)"
    { read_logs auth.log; read_logs syslog; } | grep -w -- "$USER_NAME" | in_range | sort -u > "$RESULT"
else
    echo "(source : journal systemd)"
    uid=$(id -u "$USER_NAME" 2>/dev/null)
    {
        journalctl --since "$FROM" --until "$TO" -o short-iso --no-pager | grep -w -- "$USER_NAME"
        [[ -n "$uid" ]] && journalctl _UID="$uid" --since "$FROM" --until "$TO" -o short-iso --no-pager
    } | grep -v '^-- ' | sort -u > "$RESULT"
fi

echo "--- Événements trouvés : $(wc -l < "$RESULT")"
tail -n 30 "$RESULT"
echo
echo "--- Par programme"
# 3e champ (format Debian 12 : date machine programme[pid]:), sans le [pid]
awk '{ p = ($1 ~ /^[A-Z][a-z][a-z]$/) ? $5 : $3; sub(/\[.*/, "", p); sub(/:$/, "", p); print p }' "$RESULT" \
    | sort | uniq -c | sort -rn
echo
echo "--- Commandes lancées avec sudo"
grep "COMMAND=" "$RESULT" | awk -F'COMMAND=' '{print $2}' | cut -c1-80 | tail -n 10
