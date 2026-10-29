#!/bin/bash
#
# Exercice 4 : Rechercher les erreurs dans tous les logs
#
# Usage : sudo ./find_errors.sh [motif]
#         défaut : error|fail|critical|fatal|panic|denied (majuscules ignorées)
#
# Les logs sont "tournés" (logrotate) : syslog devient syslog.1, puis
# syslog.2.gz (compressé)... Pour tout fouiller, il faut lire aussi les .gz.
#   1. find liste tous les fichiers de /var/log (archives comprises), sauf les
#      binaires (journal, wtmp, btmp, lastlog).
#   2. xargs les passe tous à zgrep (= grep qui sait lire les .gz).
#      -I : ignore les fichiers binaires   -i : majuscules/minuscules   -H : nom du fichier
#   3. Résumé : nombre d'erreurs par fichier, puis les dernières erreurs.
#   4. En plus : les erreurs du journal systemd (journalctl -p err).

set -u

PATTERN="${1:-error|fail|critical|fatal|panic|denied}"

if [[ $EUID -ne 0 ]]; then
    echo "Lancer en root (sudo $0)." >&2
    exit 1
fi

RESULT=$(mktemp)
trap 'rm -f "$RESULT"' EXIT

# 1 et 2. -print0 / -0 : noms de fichiers séparés par un caractère nul,
# pour ne pas casser sur les noms avec espaces
find /var/log -type f \
    ! -path "/var/log/journal/*" ! -name "wtmp*" ! -name "btmp*" ! -name "lastlog" ! -name "faillog" \
    -print0 2>/dev/null \
    | xargs -0 zgrep -IiHE "$PATTERN" 2>/dev/null > "$RESULT"

total=$(wc -l < "$RESULT")
files=$(find /var/log -type f ! -path "/var/log/journal/*" | wc -l)
archives=$(find /var/log -type f -name "*.gz" | wc -l)
echo "Recherche de : $PATTERN"
echo "Fichiers fouillés : $files (dont $archives archives .gz)"
echo "Lignes trouvées   : $total"
echo

# 3. Résumé par fichier (tout ce qui est avant le premier ":")
echo "--- Erreurs par fichier"
cut -d: -f1 "$RESULT" | sort | uniq -c | sort -rn | head -n 15
echo
echo "--- 15 dernières erreurs trouvées"
tail -n 15 "$RESULT" | cut -c1-180
echo

# 4. Journal systemd : niveau "err" et plus grave, depuis le dernier démarrage
echo "--- Journal systemd : erreurs depuis le démarrage (journalctl -p err -b)"
journalctl -p err -b --no-pager 2>/dev/null | tail -n 10
