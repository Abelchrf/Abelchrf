#!/bin/bash
#
# Exercice 5 : Dovecot (IMAP)
#
# Usage : sudo ./dovecot.sh      (après les exercices 1, 3 et 4)
#
# Postfix = le facteur (il livre).  Dovecot = la boîte aux lettres (on vient
# y relever son courrier avec un logiciel mail, en IMAP, port 143 / 993).
#   1. Installe Dovecot (IMAP + LMTP).
#   2. Configuration dans /etc/dovecot/conf.d/99-etna.conf (lu en dernier) :
#        - les boîtes restent /var/spool/mail/<user> (format mbox)
#        - IMAP chiffré avec le certificat de l'exercice 4
#        - un "guichet" LMTP par lequel Postfix confie les mails à Dovecot
#   3. Postfix livre désormais via Dovecot (mailbox_transport = lmtp),
#      sauf pour root que Dovecot refuse (UID 0).
#   4. Test : envoie un mail à un utilisateur et le relit en IMAP.

set -u

DOMAIN="etna.nx"
HOST="mail.$DOMAIN"
CERT="/etc/ssl/certs/$HOST.pem"
KEY="/etc/ssl/private/$HOST.key"
PASS_FILE="/root/mail_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f "$CERT" ]] || { echo "Lancer d'abord l'exercice 4 (certificat)." >&2; exit 1; }

# 1. Installation (curl sert au test IMAP)
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq dovecot-imapd dovecot-lmtpd curl >/dev/null

# 2. Configuration
cat > /etc/dovecot/conf.d/99-etna.conf <<CONF
# Exercice 5 : Dovecot avec Postfix
protocols = imap lmtp
listen = *

# Où sont les mails : boîte principale /var/mail/<user>, dossiers dans ~/mail
mail_location = mbox:~/mail:INBOX=/var/mail/%u
mail_privileged_group = mail
# Connexion : login + mot de passe Linux, en IMAP chiffré (TLS)
auth_mechanisms = plain login
ssl = yes
ssl_cert = <$CERT
ssl_key = <$KEY

# Guichet LMTP placé dans le dossier de Postfix
service lmtp {
  unix_listener /var/spool/postfix/private/dovecot-lmtp {
    mode = 0600
    user = postfix
    group = postfix
  }
}
# Postfix donne "user@etna.nx", Dovecot ne garde que "user"
protocol lmtp {
  auth_username_format = %Ln
}
CONF

doveconf -n >/dev/null || exit 1          # vérifie la configuration
systemctl enable dovecot
systemctl restart dovecot
sleep 1

# 3. Postfix confie les mails locaux à Dovecot
postconf -e "mailbox_transport = lmtp:unix:private/dovecot-lmtp"

# Exception : Dovecot refuse de livrer à root (UID 0, par sécurité).
# Les mails de root passent par "rootmbox", une copie du livreur local de
# Postfix -> ils arrivent toujours dans /var/spool/mail/root (exercice 1).
postconf -M "rootmbox/unix=rootmbox unix - n n - - local"
postconf -P "rootmbox/unix/mailbox_transport=" "rootmbox/unix/mailbox_transport_maps="
echo "root rootmbox:" > /etc/postfix/mailbox_transport
postmap /etc/postfix/mailbox_transport
postconf -e "mailbox_transport_maps = hash:/etc/postfix/mailbox_transport"
postfix check || exit 1
systemctl reload postfix
sleep 1

# 4. Test avec le premier utilisateur de l'exercice 3
user=$(head -n 1 "$PASS_FILE" 2>/dev/null | cut -d';' -f2)
pass=$(head -n 1 "$PASS_FILE" 2>/dev/null | cut -d';' -f3)
if [[ -z "$user" ]]; then
    echo "Pas d'utilisateur dans $PASS_FILE : lancer l'exercice 3 pour tester."
    exit 0
fi
echo "Mail relevé en IMAP" | mail -s "Test Dovecot" "$user@$DOMAIN"
sleep 3
echo "--- Boîte de $user vue en IMAPS (port 993) : nombre de messages"
curl -sk --noproxy '*' "imaps://localhost/INBOX" -u "$user:$pass" -X "STATUS INBOX (MESSAGES)"
echo "--- Sujet du dernier message"
curl -sk --noproxy '*' "imaps://localhost/INBOX;UID=*;SECTION=HEADER.FIELDS%20(SUBJECT)" -u "$user:$pass"
echo
echo "Depuis un logiciel mail : serveur $HOST, IMAP port 993 (SSL), login $user"
