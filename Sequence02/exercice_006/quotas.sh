#!/bin/bash
#
# Exercice 6 : Quotas de boîtes mail (Dovecot)
#
# Usage : sudo ./quotas.sh [taille]      (par défaut : 10M par utilisateur)
#
# Un quota = une taille maximale de boîte mail. Comme c'est Dovecot qui
# livre les mails (exercice 5), c'est lui qui refuse quand c'est plein.
#   1. Active le plugin quota de Dovecot (fichier 99-quota.conf).
#   2. Redémarre Dovecot et affiche le quota d'un utilisateur (doveadm quota).
#   3. Test de dépassement : quota baissé à 1M le temps du test, mail de
#      2 Mo -> refusé "Mailbox is full", puis le quota normal est remis.

set -u

QUOTA="${1:-10M}"
DOMAIN="etna.nx"
PASS_FILE="/root/mail_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f /etc/dovecot/conf.d/99-etna.conf ]] || { echo "Lancer d'abord l'exercice 5." >&2; exit 1; }

# 1. Configuration
#   quota = count  : Dovecot compte lui-même la taille des messages
#   quota_rule     : la limite (*: = pour tout le monde)
#   quota_exceeded_message : réponse renvoyée à l'expéditeur
cat > /etc/dovecot/conf.d/99-quota.conf <<CONF
# Exercice 6 : quotas
mail_plugins = \$mail_plugins quota
protocol imap {
  mail_plugins = \$mail_plugins imap_quota
}
plugin {
  quota = count:Quota utilisateur
  quota_vsizes = yes
  quota_rule = *:storage=$QUOTA
  quota_grace = 0
  quota_exceeded_message = 552 5.2.2 Boite mail pleine (Mailbox is full)
}
CONF

doveconf -n >/dev/null || exit 1
systemctl restart dovecot
sleep 1

# 2. Quota d'un utilisateur
user=$(head -n 1 "$PASS_FILE" 2>/dev/null | cut -d';' -f2)
[[ -z "$user" ]] && { echo "Lancer l'exercice 3 pour tester."; exit 0; }
echo "--- doveadm quota get -u $user"
doveadm quota get -u "$user"

# 3. Test : on baisse le quota à 1M, on envoie un mail de 2 Mo, puis on remet
sed -i "s/storage=$QUOTA/storage=1M/" /etc/dovecot/conf.d/99-quota.conf
systemctl restart dovecot
sleep 1
echo "--- Quota de test (1M)"
doveadm quota get -u "$user"

head -c 2000000 /dev/urandom | base64 | mail -s "Gros mail de 2 Mo" "$user@$DOMAIN"
sleep 4
echo "--- Réponse de Dovecot pour le mail de 2 Mo (journal de Postfix)"
grep "to=<$user@$DOMAIN>" /var/log/postfix.log | tail -n 1 | grep -oE "status=.*"

sed -i "s/storage=1M/storage=$QUOTA/" /etc/dovecot/conf.d/99-quota.conf
systemctl restart dovecot
echo
echo "Quota de chacun : doveadm quota get -A"
