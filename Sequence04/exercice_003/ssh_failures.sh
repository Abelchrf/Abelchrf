#!/bin/bash
#
# Exercice 3 : Compter les connexions SSH échouées et alerter
#
# Usage : sudo ./ssh_failures.sh [seuil]     (défaut : 5 échecs par adresse IP)
#
# Un robot qui essaie des mots de passe au hasard (attaque "brute force")
# laisse des lignes comme :
#   sshd[123]: Failed password for root from 203.0.113.5 port 4242 ssh2
#   sshd[123]: Invalid user admin from 203.0.113.5 port 4243
#
# Une tentative écrit plusieurs lignes (pam "authentication failure",
# "Invalid user", "Failed password") : on ne compte que "Failed ... for",
# qui apparaît une fois par tentative.
#
#   1. Récupère les lignes d'échec (auth.log + archives, sinon journalctl).
#   2. Compte : total, par adresse IP, par utilisateur visé (sort | uniq -c).
#   3. ALERTE pour chaque IP au-dessus du seuil : message à l'écran + ligne
#      dans le journal système (logger). Code de sortie 1 s'il y a une alerte
#      (utile pour un autre script ou une tâche cron).

set -u

THRESHOLD="${1:-5}"

if [[ $EUID -ne 0 ]]; then
    echo "Lancer en root (sudo $0)." >&2
    exit 1
fi

FAILS=$(mktemp)
trap 'rm -f "$FAILS"' EXIT

# 1. Lignes d'échec
PATTERN="Failed (password|publickey) for"
if [[ -f /var/log/auth.log ]]; then
    SOURCE="/var/log/auth.log (+ archives)"
    for f in $(ls -1tr /var/log/auth.log* 2>/dev/null); do zcat -f "$f"; done | grep "sshd" | grep -E "$PATTERN" > "$FAILS"
else
    SOURCE="journal systemd (ssh)"
    journalctl -u ssh -u sshd --no-pager -o short-iso 2>/dev/null | grep -E "$PATTERN" > "$FAILS"
fi

# 2. Comptages
total=$(wc -l < "$FAILS")
echo "Source : $SOURCE"
echo "Tentatives SSH échouées : $total"
echo
echo "--- Par adresse IP (les plus actives d'abord)"
grep -oE "from [0-9a-fA-F.:]+" "$FAILS" | awk '{print $2}' | sort | uniq -c | sort -rn | head -n 10
echo
echo "--- Par utilisateur visé"
grep -oE "for (invalid user )?[^ ]+ from" "$FAILS" | awk '{print $(NF-1)}' | sort | uniq -c | sort -rn | head -n 10
echo "(dont tentatives sur des comptes qui n'existent pas : $(grep -c "invalid user" "$FAILS"))"
echo

# 3. Alertes
alert=0
while read -r count ip; do
    if [[ $count -ge $THRESHOLD ]]; then
        echo "ALERTE : $count échecs SSH depuis $ip (seuil : $THRESHOLD)"
        logger -p auth.warning -t ssh_failures "ALERTE : $count échecs SSH depuis $ip"
        alert=1
    fi
done < <(grep -oE "from [0-9a-fA-F.:]+" "$FAILS" | awk '{print $2}' | sort | uniq -c)

if [[ $alert -eq 0 ]]; then
    echo "Aucune adresse ne dépasse le seuil de $THRESHOLD échecs."
else
    echo
    echo "Pour bloquer automatiquement ces adresses : apt install fail2ban"
fi
exit $alert
