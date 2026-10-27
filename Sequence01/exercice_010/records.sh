#!/bin/bash
#
# Exercice 010 : Enregistrements A et CNAME
#
# Usage : sudo ./records.sh     (après l'exercice 009)
#
#   A     : nom -> adresse IP              (toto -> 192.168.x.x)
#   CNAME : nom -> autre nom (un alias)    (www2 -> www, pokemon -> www.pokemon.com)
#
#   1. Ajoute les enregistrements à la fin du fichier de zone.
#   2. Augmente le serial (sinon les autres DNS ne voient pas le changement).
#   3. Vérifie la zone (named-checkzone) et la recharge (rndc reload).
#   4. Teste chaque nom avec dig.

set -u

DOMAIN="je-le-trouve-beau-mon-domain-donc-il-est-beau.com"
ZONE_FILE="/etc/bind/db.$DOMAIN"
IP=$(hostname -I | awk '{print $1}')
MARK="; exercice 010"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f "$ZONE_FILE" ]] || { echo "Lancer d'abord l'exercice 009." >&2; exit 1; }

# 1. On retire les lignes d'un lancement précédent, puis on les (ré)ajoute.
#    Un nom qui finit par "." est complet ; sinon le domaine est ajouté.
sed -i "/$MARK/d" "$ZONE_FILE"
cat >> "$ZONE_FILE" <<ZONE
toto          IN  A      $IP                 $MARK
www2          IN  CNAME  www                 $MARK
pokemon       IN  CNAME  www.pokemon.com.    $MARK
casserlavoix  IN  CNAME  www.youtube.com.    $MARK
ultrastar     IN  CNAME  open.spotify.com.   $MARK
ZONE

# 2. serial + 1  (ex : 2026102701 -> 2026102702)
old=$(grep -oE '[0-9]+ *; serial' "$ZONE_FILE" | grep -oE '^[0-9]+')
sed -i "s/$old *; serial/$((old + 1)) ; serial/" "$ZONE_FILE"

# 3. Vérification puis rechargement de la zone, sans couper le service
named-checkzone "$DOMAIN" "$ZONE_FILE" || exit 1
rndc reload "$DOMAIN"

# 4. Tests
sleep 1
for name in toto www2 pokemon casserlavoix ultrastar; do
    echo "--- $name.$DOMAIN"
    dig +noall +answer "$name.$DOMAIN" @127.0.0.1
done
