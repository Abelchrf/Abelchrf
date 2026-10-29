#!/bin/bash
#
# Exercice 1 : Installation de Postfix (SMTP)
#
# Usage : sudo ./postfix.sh
#
# Postfix est le "facteur" : il reçoit les mails (protocole SMTP, port 25)
# et les dépose dans la boîte du destinataire, ici /var/spool/mail/<user>.
#   1. Installe Postfix sans questions (réponses données à l'avance avec
#      debconf) + mailutils pour la commande "mail".
#   2. Configure le domaine local etna.nx avec postconf.
#   3. Redémarre Postfix et envoie un mail de test à root@etna.nx.

set -u

DOMAIN="etna.nx"
HOST="mail.$DOMAIN"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# 1. Installation : on répond d'avance aux questions de l'installateur
echo "postfix postfix/main_mailer_type select Internet Site" | debconf-set-selections
echo "postfix postfix/mailname string $DOMAIN" | debconf-set-selections
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq postfix mailutils >/dev/null

# 2. Configuration (postconf -e modifie /etc/postfix/main.cf)
echo "$DOMAIN" > /etc/mailname
postconf -e "myhostname = $HOST"                 # nom du serveur
postconf -e "mydomain = $DOMAIN"                 # domaine géré
postconf -e "myorigin = \$mydomain"              # expéditeur : user@etna.nx
# Domaines pour lesquels CE serveur garde les mails (livraison locale)
postconf -e "mydestination = \$myhostname, \$mydomain, localhost.\$mydomain, localhost"
postconf -e "inet_interfaces = all"              # écoute sur toutes les cartes réseau
postconf -e "inet_protocols = ipv4"
postconf -e "mynetworks = 127.0.0.0/8"           # seule la machine peut envoyer sans compte
postconf -e "home_mailbox ="                     # boîtes dans /var/spool/mail/<user>
# Journal lisible facilement (Debian 12 n'a pas toujours rsyslog)
postconf -e "maillog_file = /var/log/postfix.log"

newaliases                                       # (re)génère /etc/aliases.db
postfix check || exit 1

# 3. Démarrage et test
systemctl enable postfix
systemctl restart postfix
sleep 2

echo "Test Email" | mail -s "Test Subject" "root@$DOMAIN"
sleep 3
echo "--- tail /var/spool/mail/root"
tail -n 15 /var/spool/mail/root
echo
echo "Suivre les mails qui arrivent : tail -f /var/spool/mail/root"
echo "Journal de Postfix            : tail -f /var/log/postfix.log"
