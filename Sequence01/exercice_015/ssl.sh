#!/bin/bash
#
# Exercice 015 : HTTPS (SSL) avec un certificat auto-signé
#
# Usage : sudo ./ssl.sh     (après l'exercice 004)
#
# HTTPS = HTTP chiffré. Il faut une paire de clés :
#   - la clé privée  (secrète, reste sur le serveur)
#   - le certificat  (public, envoyé au navigateur, contient la clé publique)
# "Auto-signé" = c'est nous qui signons le certificat, pas une autorité
# reconnue : le navigateur affichera un avertissement, c'est normal.
#
#   1. Génère la clé et le certificat avec openssl (valable 365 jours).
#   2. Active le module SSL d'Apache (a2enmod ssl).
#   3. Crée un virtual host sur le port 443 qui utilise ce certificat.
#   4. Recharge Apache (systemctl reload apache2) et teste en HTTPS.

set -u

SITE="monsite.local"
DOMAIN="je-le-trouve-beau-mon-domain-donc-il-est-beau.com"
ROOT="/var/www/monsite"
KEY="/etc/ssl/private/$SITE.key"
CERT="/etc/ssl/certs/$SITE.crt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -d "$ROOT" ]] || { echo "Lancer d'abord l'exercice 004." >&2; exit 1; }

# 1. Clé + certificat
#   req -x509      : fabrique directement un certificat (auto-signé)
#   -nodes         : clé privée sans mot de passe (sinon Apache le demanderait)
#   -newkey rsa:2048 : nouvelle clé RSA de 2048 bits
#   -subj          : identité du certificat (CN = nom du site)
#   subjectAltName : les noms pour lesquels le certificat est valable
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$KEY" -out "$CERT" \
    -subj "/C=FR/O=ETNA/CN=$SITE" \
    -addext "subjectAltName=DNS:$SITE,DNS:www.$DOMAIN,DNS:$DOMAIN" 2>/dev/null
chmod 600 "$KEY"                         # la clé privée : root uniquement
echo "Certificat : $CERT"
openssl x509 -in "$CERT" -noout -subject -enddate

# 2. Module SSL
a2enmod -q ssl

# 3. Virtual host HTTPS (port 443)
cat > "/etc/apache2/sites-available/$SITE-ssl.conf" <<CONF
<VirtualHost *:443>
    ServerName $SITE
    ServerAlias www.$DOMAIN $DOMAIN
    DocumentRoot $ROOT

    SSLEngine on
    SSLCertificateFile    $CERT
    SSLCertificateKeyFile $KEY

    ErrorLog \${APACHE_LOG_DIR}/$SITE-ssl-error.log
    CustomLog \${APACHE_LOG_DIR}/$SITE-ssl-access.log combined
</VirtualHost>
CONF
a2ensite -q "$SITE-ssl"

# 4. Vérification, rechargement, test (-k : accepter le certificat auto-signé)
apache2ctl configtest || exit 1
systemctl reload apache2
sleep 1
echo "--- curl -k https://$SITE"
curl -sk --noproxy "*" "https://$SITE" | grep "<h1>"
