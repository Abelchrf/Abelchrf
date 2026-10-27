#!/bin/bash
#
# Exercice 005 : une page web personnelle pour chaque utilisateur
#
# Usage : sudo ./userdir.sh
#
# Chaque utilisateur met ses pages dans ~/www et elles sont visibles à
# l'adresse http://<serveur>/~<login>/  (ex : http://localhost/~tbutchers/)
#
#   1. Installe Apache et active le module userdir (a2enmod userdir).
#   2. Configure userdir pour utiliser ~/www (au lieu de ~/public_html).
#   3. Pour chaque utilisateur : crée ~/www + un index.html, règle les droits.
#   4. Recharge Apache et teste chaque page avec curl.

set -u

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# 1. Installation + module userdir
apt-get update -qq
apt-get install -y -qq apache2 curl >/dev/null
a2enmod -q userdir

# 2. Configuration du module : dossier "www" dans le home de chaque utilisateur
cat > /etc/apache2/mods-available/userdir.conf <<'CONF'
<IfModule mod_userdir.c>
    UserDir www
    UserDir disabled root

    <Directory /home/*/www>
        AllowOverride FileInfo AuthConfig Limit Indexes
        Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec
        Require method GET POST OPTIONS
    </Directory>
</IfModule>
CONF

# Les futurs utilisateurs auront aussi un dossier www (copié depuis /etc/skel)
mkdir -p /etc/skel/www

# 3. Pour chaque "vrai" utilisateur (UID >= 1000, home dans /home)
users=$(getent passwd | awk -F: '$3 >= 1000 && $3 < 65534 && $6 ~ /^\/home\// {print $1}')

for user in $users; do
    home=$(getent passwd "$user" | cut -d: -f6)
    mkdir -p "$home/www"
    cat > "$home/www/index.html" <<HTML
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Page de $user</title></head>
<body><h1>Page personnelle de $user</h1></body>
</html>
HTML
    chown -R "$user:" "$home/www"      # le dossier appartient à l'utilisateur
    chmod 755 "$home/www"              # Apache (www-data) doit pouvoir le lire
    chmod 644 "$home/www/index.html"
    chmod o+x "$home"                  # ...et pouvoir traverser le home
done

# 4. Rechargement d'Apache puis test de chaque page
apache2ctl configtest || exit 1
systemctl enable --now apache2
systemctl reload apache2

ok=0; ko=0
for user in $users; do
    code=$(curl -s -o /dev/null -w '%{http_code}' "http://localhost/~$user/")
    if [[ "$code" == "200" ]]; then
        ok=$((ok + 1))
    else
        echo "[ECHEC] http://localhost/~$user/ -> code $code"
        ko=$((ko + 1))
    fi
done
echo "Pages accessibles : $ok | En échec : $ko"
echo "Exemple : curl http://localhost/~$(echo "$users" | head -n 1)/"
