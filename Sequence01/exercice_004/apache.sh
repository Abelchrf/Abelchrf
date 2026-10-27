#!/bin/bash
#
# Exercice 004 : Installation et configuration d'Apache
#
# Usage : sudo ./apache.sh
#
#   1. Installe Apache (apt install apache2).
#   2. Crée un site simple dans /var/www/monsite avec une page index.html.
#   3. Crée un virtual host "monsite.local" qui sert ce dossier.
#   4. Active le site, démarre Apache (systemctl) et teste avec curl.

set -u

SITE="monsite.local"
ROOT="/var/www/monsite"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# 1. Installation (curl sert seulement au test final)
apt-get update -qq
apt-get install -y -qq apache2 curl >/dev/null

# 2. Le contenu du site
mkdir -p "$ROOT"
cat > "$ROOT/index.html" <<HTML
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>$SITE</title></head>
<body><h1>Bienvenue sur $SITE</h1><p>Servi par Apache sur $(hostname).</p></body>
</html>
HTML
chown -R www-data:www-data "$ROOT"     # www-data = l'utilisateur d'Apache

# 3. Le virtual host : "quand on demande $SITE sur le port 80, sers $ROOT"
cat > "/etc/apache2/sites-available/$SITE.conf" <<CONF
<VirtualHost *:80>
    ServerName $SITE
    DocumentRoot $ROOT
    ErrorLog \${APACHE_LOG_DIR}/$SITE-error.log
    CustomLog \${APACHE_LOG_DIR}/$SITE-access.log combined
</VirtualHost>
CONF

# Le nom monsite.local doit pointer vers cette machine
grep -q " $SITE\$" /etc/hosts || echo "127.0.0.1 $SITE" >> /etc/hosts

# 4. Activation du site, vérification de la config, démarrage
a2ensite -q "$SITE"
apache2ctl configtest || exit 1
systemctl enable --now apache2
systemctl reload apache2

echo
echo "Test : curl http://$SITE"
curl -s "http://$SITE" | grep "<h1>"
