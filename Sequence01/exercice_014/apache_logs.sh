#!/bin/bash
#
# Exercice 014 : Surveillance des logs Apache
#
# Usage : sudo ./apache_logs.sh         -> résumé des logs
#         sudo ./apache_logs.sh -f      -> suivi en direct (Ctrl+C pour quitter)
#
# Apache écrit deux fichiers :
#   - access.log : une ligne par page demandée
#       IP - - [date] "GET /page HTTP/1.1" CODE taille ...
#     CODE : 200 = OK, 301/302 = redirection, 404 = introuvable,
#            403 = interdit, 500 = erreur du serveur
#   - error.log  : les problèmes rencontrés par Apache

set -u

LOG_DIR="/var/log/apache2"
ACCESS="$LOG_DIR/access.log"
ERROR="$LOG_DIR/error.log"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# Mode suivi en direct : tail -F suit les nouvelles lignes de tous les logs,
# grep --line-buffered n'affiche que les erreurs (codes 4xx/5xx ou [error])
if [[ "${1:-}" == "-f" ]]; then
    echo "Surveillance des erreurs Apache (Ctrl+C pour arrêter)..."
    tail -F -n 0 "$LOG_DIR"/*.log | grep --line-buffered -E '" [45][0-9]{2} |\[[a-z_]*:?(error|crit|alert|emerg)\]'
    exit 0
fi

# Tous les access.log (celui par défaut + ceux des sites : monsite.local-access.log...)
access_logs=$(ls "$LOG_DIR"/*access.log 2>/dev/null)
[[ -z "$access_logs" ]] && { echo "Aucun log d'accès dans $LOG_DIR" >&2; exit 1; }

echo "=== Nombre de requêtes par code HTTP"
# Le code HTTP est le 9e champ de chaque ligne
cat $access_logs | awk '{print $9}' | sort | uniq -c | sort -rn

echo
echo "=== Les 5 adresses IP qui visitent le plus"
cat $access_logs | awk '{print $1}' | sort | uniq -c | sort -rn | head -n 5

echo
echo "=== Les 5 pages les plus demandées"
cat $access_logs | awk '{print $7}' | sort | uniq -c | sort -rn | head -n 5

echo
echo "=== Dernières requêtes en erreur (4xx / 5xx)"
cat $access_logs | grep -E '" [45][0-9]{2} ' | tail -n 5

echo
echo "=== Dernières lignes de error.log"
tail -n 5 "$ERROR"

echo
echo "Suivi en direct : $0 -f"
