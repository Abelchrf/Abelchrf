#!/bin/bash
#
# Exercice 11 : Rspamd
#
# Usage : sudo ./rspamd.sh
#
# Rspamd est un anti-spam plus moderne et plus rapide que SpamAssassin.
# Ici il le COMPLÈTE : SpamAssassin marque les mails (exercice 8), Rspamd
# les note aussi et peut refuser directement les pires.
# Il se branche comme un milter (comme ClamAV) sur le port 11332.
# Il utilise Redis (petite base de données en mémoire) pour retenir ce qu'il
# apprend (statistiques, réputation...).
#
#   1. Installe Rspamd et Redis.
#   2. Configuration dans /etc/rspamd/local.d/ (nos réglages, séparés des
#      fichiers d'origine) : Redis, milter, seuils, en-têtes ajoutés.
#   3. Ajoute Rspamd aux milters de Postfix.
#   4. Tests : analyse d'un mail normal et d'un mail GTUBE avec rspamc.

set -u

DOMAIN="etna.nx"
LOCAL="/etc/rspamd/local.d"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# 1. Installation
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq rspamd redis-server >/dev/null
systemctl enable redis-server
systemctl restart redis-server

# 2. Configuration
mkdir -p "$LOCAL"
echo 'servers = "127.0.0.1";' > "$LOCAL/redis.conf"

# Le "proxy" de Rspamd parle le langage milter avec Postfix
cat > "$LOCAL/worker-proxy.inc" <<'CONF'
bind_socket = "localhost:11332";
milter = yes;
timeout = 120s;
upstream "local" {
  default = yes;
  self_scan = yes;
}
CONF

# Que faire selon la note : en-tête "spam" à 6, refus à 15.
# Pas de greylisting ici : c'est le travail de Postgrey (exercice 9).
cat > "$LOCAL/actions.conf" <<'CONF'
add_header = 6;
reject = 15;
greylist = null;
CONF

# Ajoute X-Spamd-Result (le détail de la note) dans chaque mail,
# y compris ceux envoyés depuis la machine (pratique pour tester)
cat > "$LOCAL/milter_headers.conf" <<'CONF'
extended_spam_headers = true;
skip_local = false;
skip_authenticated = false;
CONF

rspamadm configtest || exit 1
systemctl enable rspamd
systemctl restart rspamd
sleep 3

# 3. Postfix : ajout du milter Rspamd (en gardant les autres)
add_milter() {
    local key cur
    for key in smtpd_milters non_smtpd_milters; do
        cur=$(postconf -h "$key")
        [[ "$cur" == *"$1"* ]] || postconf -e "$key = ${cur:+$cur, }$1"
    done
}
add_milter "inet:127.0.0.1:11332"
postconf -e "milter_default_action = accept"
postconf -e "milter_protocol = 6"
postconf -e "milter_mail_macros = i {mail_addr} {client_addr} {client_name} {auth_authen}"
postfix check || exit 1
systemctl reload postfix

# 4. Tests avec rspamc (le client en ligne de commande de Rspamd)
echo "--- Mail normal"
printf 'From: alice@%s\nTo: root@%s\nSubject: Bonjour\n\nUn mail normal.\n' "$DOMAIN" "$DOMAIN" \
    | rspamc | grep -E "^Action|^Spam|^Score"
echo "--- Mail GTUBE"
printf 'From: promo@spam.example\nTo: root@%s\nSubject: Gagnez\n\nXJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X\n' "$DOMAIN" \
    | rspamc | grep -E "^Action|^Spam|^Score"
echo
echo "Statistiques : rspamc stat    Interface web : http://localhost:11334"
