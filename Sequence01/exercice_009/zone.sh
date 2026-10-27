#!/bin/bash
#
# Exercice 009 : Création d'une zone DNS avec BIND
#
# Usage : sudo ./zone.sh      (après l'exercice 008, et 004/005 pour le site)
#
# Une "zone" = l'annuaire d'un domaine. Ici notre machine devient LE serveur
# DNS du domaine fictif ci-dessous :
#   1. Écrit le fichier de zone /etc/bind/db.<domaine> (les enregistrements).
#   2. Déclare la zone dans /etc/bind/named.conf.local.
#   3. Vérifie (named-checkzone, named-checkconf) et redémarre BIND.
#   4. Configure la machine pour utiliser son propre DNS (/etc/resolv.conf).
#   5. Ajoute le nom au site Apache de l'exercice 004 et teste.

set -u

DOMAIN="je-le-trouve-beau-mon-domain-donc-il-est-beau.com"
ZONE_FILE="/etc/bind/db.$DOMAIN"
IP=$(hostname -I | awk '{print $1}')     # adresse IP de la machine

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
command -v named >/dev/null || { echo "Lancer d'abord l'exercice 008 (BIND9)." >&2; exit 1; }

# 1. Le fichier de zone
#   SOA : fiche d'identité de la zone (serveur principal, email admin, serial...)
#         le serial doit augmenter à chaque modification (format AAAAMMJJnn)
#   NS  : le serveur DNS de la zone        A : nom -> adresse IPv4
cat > "$ZONE_FILE" <<ZONE
\$TTL 86400
@   IN  SOA ns1.$DOMAIN. admin.$DOMAIN. (
        $(date +%Y%m%d)01 ; serial
        3600       ; refresh
        900        ; retry
        604800     ; expire
        86400 )    ; TTL négatif

@       IN  NS  ns1.$DOMAIN.
ns1     IN  A   $IP
@       IN  A   $IP
www     IN  A   $IP
ZONE

# 2. Déclaration de la zone (une seule fois)
if ! grep -q "zone \"$DOMAIN\"" /etc/bind/named.conf.local; then
    cat >> /etc/bind/named.conf.local <<CONF

zone "$DOMAIN" {
    type master;
    file "$ZONE_FILE";
};
CONF
fi

# 3. Vérifications puis redémarrage
named-checkzone "$DOMAIN" "$ZONE_FILE" || exit 1
named-checkconf || exit 1
systemctl restart named

# 4. La machine pose désormais ses questions DNS à son propre BIND
[[ -f /etc/resolv.conf.orig ]] || cp /etc/resolv.conf /etc/resolv.conf.orig
echo "nameserver 127.0.0.1" > /etc/resolv.conf

# 5. Le site de l'exercice 004 répond aussi à ce nom
VHOST="/etc/apache2/sites-available/monsite.local.conf"
if [[ -f "$VHOST" ]] && ! grep -q "$DOMAIN" "$VHOST"; then
    sed -i "/ServerName/a\\    ServerAlias www.$DOMAIN $DOMAIN" "$VHOST"
    systemctl reload apache2
fi

echo
echo "--- dig www.$DOMAIN"
dig +short "www.$DOMAIN"
if command -v curl >/dev/null; then
    echo "--- curl http://www.$DOMAIN"
    curl -s "http://www.$DOMAIN" | grep "<h1>"
fi
echo
echo "Depuis un autre PC : mettre $IP comme serveur DNS, puis ouvrir http://www.$DOMAIN"
