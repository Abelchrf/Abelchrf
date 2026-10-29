#!/bin/bash
#
# Exercice 12 : Signature DKIM des mails sortants (OpenDKIM)
#
# Usage : sudo ./dkim.sh
#
# DKIM = une signature électronique sur chaque mail envoyé :
#   - le serveur signe avec une clé PRIVÉE (gardée secrète) ;
#   - la clé PUBLIQUE est publiée dans le DNS du domaine
#     (enregistrement TXT "mail._domainkey.etna.nx") ;
#   - le destinataire vérifie la signature avec la clé publique : il sait que
#     le mail vient bien de etna.nx et qu'il n'a pas été modifié en route.
#
#   1. Installe OpenDKIM et génère la paire de clés (sélecteur "mail").
#   2. Configure OpenDKIM (domaine, clé, port 8891).
#   3. Ajoute OpenDKIM aux milters de Postfix.
#   4. Test : un mail envoyé depuis le serveur doit avoir un en-tête DKIM-Signature.
#   5. Affiche l'enregistrement DNS à publier.

set -u

DOMAIN="etna.nx"
SELECTOR="mail"
KEY_DIR="/etc/opendkim/keys/$DOMAIN"
CONF="/etc/opendkim.conf"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

set_conf() {   # set_conf CLE VALEUR : remplace ou ajoute la ligne dans opendkim.conf
    if grep -qE "^$1[[:space:]]" "$CONF"; then sed -i -E "s|^$1[[:space:]].*|$1\t\t$2|" "$CONF"; else printf '%s\t\t%s\n' "$1" "$2" >> "$CONF"; fi
}

# 1. Installation et clés (2048 bits)
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq opendkim opendkim-tools >/dev/null
mkdir -p "$KEY_DIR"
if [[ ! -f "$KEY_DIR/$SELECTOR.private" ]]; then
    opendkim-genkey -b 2048 -d "$DOMAIN" -D "$KEY_DIR" -s "$SELECTOR"
fi
chown -R opendkim:opendkim /etc/opendkim
chmod 600 "$KEY_DIR/$SELECTOR.private"           # clé privée : secrète

# 2. Configuration
#   Mode sv : signe (s) les mails sortants et vérifie (v) les entrants
set_conf Domain "$DOMAIN"
set_conf Selector "$SELECTOR"
set_conf KeyFile "$KEY_DIR/$SELECTOR.private"
set_conf Mode sv
set_conf Canonicalization relaxed/simple
set_conf Socket "inet:8891@127.0.0.1"
sed -i 's|^SOCKET=.*|SOCKET=inet:8891@127.0.0.1|' /etc/default/opendkim 2>/dev/null
opendkim -n -x "$CONF" || exit 1                 # vérifie la configuration
systemctl enable opendkim
systemctl restart opendkim
sleep 2

# 3. Postfix
add_milter() {
    local key cur
    for key in smtpd_milters non_smtpd_milters; do
        cur=$(postconf -h "$key")
        [[ "$cur" == *"$1"* ]] || postconf -e "$key = ${cur:+$cur, }$1"
    done
}
add_milter "inet:127.0.0.1:8891"
postconf -e "milter_default_action = accept"
postconf -e "milter_protocol = 6"
postfix check || exit 1
systemctl reload postfix
sleep 1

# 4. Test
# -r : expéditeur root@etna.nx (OpenDKIM ne signe que les mails de $DOMAIN)
echo "Ce mail est signe avec DKIM" | mail -r "root@$DOMAIN" -s "Test DKIM" "root@$DOMAIN"
sleep 4
echo "--- Signature trouvée dans le dernier mail de root"
grep -A2 "^DKIM-Signature" /var/spool/mail/root | tail -n 3

# 5. La clé publique à mettre dans le DNS du domaine
echo
echo "--- Enregistrement DNS à publier dans la zone $DOMAIN ($KEY_DIR/$SELECTOR.txt)"
cat "$KEY_DIR/$SELECTOR.txt"
echo "Vérification une fois publié : opendkim-testkey -d $DOMAIN -s $SELECTOR -vvv"
