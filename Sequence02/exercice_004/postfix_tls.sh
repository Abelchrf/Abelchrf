#!/bin/bash
#
# Exercice 4 : Chiffrer SMTP avec TLS
#
# Usage : sudo ./postfix_tls.sh
#
# Sans TLS, les mails (et les mots de passe) passent en clair sur le réseau.
# Avec STARTTLS, le client dit "passons en chiffré" juste après EHLO.
#   1. Génère un certificat auto-signé pour mail.etna.nx (openssl).
#   2. Indique à Postfix où sont le certificat et la clé (postconf).
#   3. Recharge Postfix et vérifie qu'il propose STARTTLS et que la
#      connexion chiffrée fonctionne (openssl s_client -starttls smtp).

set -u

HOST="mail.etna.nx"
CERT="/etc/ssl/certs/$HOST.pem"
KEY="/etc/ssl/private/$HOST.key"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# 1. Certificat auto-signé (10 ans), clé privée lisible par root seul
if [[ ! -f "$CERT" ]]; then
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
        -keyout "$KEY" -out "$CERT" \
        -subj "/C=FR/O=ETNA/CN=$HOST" -addext "subjectAltName=DNS:$HOST" 2>/dev/null
    chmod 600 "$KEY"
fi
openssl x509 -in "$CERT" -noout -subject -enddate

# 2. Configuration de Postfix
#   smtpd_ = quand Postfix RECOIT (serveur)   smtp_ = quand il ENVOIE (client)
#   security_level = may : TLS proposé, mais pas obligatoire (sinon les
#   serveurs qui ne savent pas faire de TLS ne pourraient plus nous écrire)
postconf -e "smtpd_tls_cert_file = $CERT"
postconf -e "smtpd_tls_key_file = $KEY"
postconf -e "smtpd_tls_security_level = may"
postconf -e "smtpd_tls_loglevel = 1"
postconf -e "smtpd_tls_protocols = !SSLv2, !SSLv3, !TLSv1, !TLSv1.1"
postconf -e "smtp_tls_security_level = may"
postconf -e "smtp_tls_loglevel = 1"

postfix check || exit 1
systemctl reload postfix
sleep 1

# 3. Tests
echo "--- Postfix annonce-t-il STARTTLS ?"
{ sleep 1; echo "EHLO test"; sleep 1; echo "QUIT"; } | telnet localhost 25 2>/dev/null | grep -i starttls
echo "--- Connexion chiffrée"
echo QUIT | openssl s_client -starttls smtp -connect localhost:25 -servername "$HOST" 2>/dev/null \
    | grep -E "^subject=|^New,|Protocol *:" | head -n 3
