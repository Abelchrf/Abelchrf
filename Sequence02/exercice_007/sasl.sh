#!/bin/bash
#
# Exercice 7 : Authentification SASL pour Postfix
#
# Usage : sudo ./sasl.sh       (après les exercices 4 et 5)
#
# Sans authentification, n'importe qui pourrait utiliser notre serveur pour
# envoyer des mails partout (un "open relay" = paradis des spammeurs).
# Avec SASL, pour ENVOYER vers l'extérieur il faut se connecter avec son
# login / mot de passe. Postfix ne vérifie pas lui-même : il demande à
# Dovecot (qui connaît déjà les mots de passe).
#   1. Dovecot ouvre un "guichet d'authentification" pour Postfix.
#   2. Postfix l'utilise (smtpd_sasl_type = dovecot).
#   3. Règles : authentifié ou machine locale = OK, sinon on ne relaie pas.
#   4. Port 587 (submission) : le port des logiciels mail, TLS + login obligatoires.
#   5. Tests : envoi avec et sans mot de passe.

set -u

DOMAIN="etna.nx"
PASS_FILE="/root/mail_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f /etc/dovecot/conf.d/99-etna.conf ]] || { echo "Lancer d'abord l'exercice 5." >&2; exit 1; }

# 1. Dovecot : socket d'authentification dans le dossier de Postfix
cat > /etc/dovecot/conf.d/99-sasl.conf <<'CONF'
# Exercice 7 : Postfix demande à Dovecot de vérifier les mots de passe
service auth {
  unix_listener /var/spool/postfix/private/auth {
    mode = 0660
    user = postfix
    group = postfix
  }
}
CONF
doveconf -n >/dev/null || exit 1
systemctl restart dovecot

# 2. et 3. Postfix
postconf -e "smtpd_sasl_type = dovecot"
postconf -e "smtpd_sasl_path = private/auth"
postconf -e "smtpd_sasl_auth_enable = yes"
postconf -e "smtpd_tls_auth_only = yes"          # mot de passe seulement en chiffré
postconf -e "smtpd_relay_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination"

# 4. Port 587 : TLS obligatoire et connexion obligatoire
postconf -M "submission/inet=submission inet n - y - - smtpd"
postconf -P "submission/inet/syslog_name=postfix/submission"
postconf -P "submission/inet/smtpd_tls_security_level=encrypt"
postconf -P "submission/inet/smtpd_sasl_auth_enable=yes"
postconf -P "submission/inet/smtpd_client_restrictions=permit_sasl_authenticated,reject"

postfix check || exit 1
systemctl restart postfix
sleep 2

# 5. Tests
user=$(head -n 1 "$PASS_FILE" 2>/dev/null | cut -d';' -f2)
pass=$(head -n 1 "$PASS_FILE" 2>/dev/null | cut -d';' -f3)
[[ -z "$user" ]] && { echo "Lancer l'exercice 3 pour tester."; exit 0; }

echo "--- Le port 587 propose AUTH (après STARTTLS)"
{ sleep 1; echo "EHLO test"; sleep 1; echo QUIT; } | openssl s_client -starttls smtp -connect localhost:587 -quiet 2>/dev/null | grep AUTH

printf 'Subject: Test SASL\n\nEnvoye avec login et mot de passe.\n' > /tmp/sasl_test.eml
echo "--- Envoi AVEC mot de passe ($user)"
curl -sk --noproxy '*' --ssl-reqd "smtp://localhost:587" -u "$user:$pass" \
    --mail-from "$user@$DOMAIN" --mail-rcpt "root@$DOMAIN" -T /tmp/sasl_test.eml \
    && echo "OK : mail accepté"
echo "--- Envoi SANS mot de passe"
curl -sk --noproxy '*' --ssl-reqd "smtp://localhost:587" \
    --mail-from "pirate@example.com" --mail-rcpt "root@$DOMAIN" -T /tmp/sasl_test.eml \
    || echo "Refusé, comme prévu"
rm -f /tmp/sasl_test.eml
