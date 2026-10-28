#!/bin/bash
#
# Exercice 011 : Résolution inverse (PTR)
#
# Usage : sudo ./ptr.sh      (après l'exercice 009)
#
# Résolution normale : nom -> IP     (dig www.domaine)
# Résolution inverse : IP  -> nom    (dig -x 192.168.1.42)
#
# L'inverse utilise une zone spéciale : les 3 premiers nombres de l'IP à
# l'envers + ".in-addr.arpa". Pour 192.168.1.42 :
#   zone 1.168.192.in-addr.arpa, enregistrement "42 IN PTR me.<domaine>."
#
# Le script trouve l'IP tout seul (hostname -I), crée cette zone, ajoute
# "me" dans la zone normale, vérifie, redémarre BIND et teste avec dig -x.

set -u

DOMAIN="je-le-trouve-beau-mon-domain-donc-il-est-beau.com"
ZONE_FILE="/etc/bind/db.$DOMAIN"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f "$ZONE_FILE" ]] || { echo "Lancer d'abord l'exercice 009." >&2; exit 1; }

# 1. L'IP de la machine, découpée en 4 nombres : 192.168.1.42 -> a b c d
IP=$(hostname -I | awk '{print $1}')
IFS=. read -r a b c d <<< "$IP"
REV_ZONE="$c.$b.$a.in-addr.arpa"            # 1.168.192.in-addr.arpa
REV_FILE="/etc/bind/db.$a.$b.$c"
echo "IP : $IP  ->  zone inverse : $REV_ZONE"

# 2. Fichier de la zone inverse
cat > "$REV_FILE" <<ZONE
\$TTL 86400
@   IN  SOA ns1.$DOMAIN. admin.$DOMAIN. (
        $(date +%Y%m%d)01 ; serial
        3600 900 604800 86400 )

@       IN  NS   ns1.$DOMAIN.
$d      IN  PTR  me.$DOMAIN.
ZONE

# 3. Déclaration de la zone inverse (une seule fois)
if ! grep -q "zone \"$REV_ZONE\"" /etc/bind/named.conf.local; then
    cat >> /etc/bind/named.conf.local <<CONF

zone "$REV_ZONE" {
    type master;
    file "$REV_FILE";
};
CONF
fi

# 4. "me" doit aussi exister dans la zone normale (nom -> IP), serial + 1
MARK="; exercice 011"
sed -i "/$MARK/d" "$ZONE_FILE"
echo "me            IN  A      $IP                 $MARK" >> "$ZONE_FILE"
old=$(grep -oE '[0-9]+ *; serial' "$ZONE_FILE" | grep -oE '^[0-9]+')
sed -i "s/$old *; serial/$((old + 1)) ; serial/" "$ZONE_FILE"

# 5. Vérifications, redémarrage, tests
named-checkzone "$REV_ZONE" "$REV_FILE" || exit 1
named-checkzone "$DOMAIN" "$ZONE_FILE" || exit 1
named-checkconf || exit 1
systemctl restart named
sleep 1

echo "--- dig -x $IP   (IP -> nom)"
dig +short -x "$IP" @127.0.0.1
echo "--- dig me.$DOMAIN   (nom -> IP)"
dig +short "me.$DOMAIN" @127.0.0.1
