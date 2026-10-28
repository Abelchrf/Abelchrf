#!/bin/bash
#
# Exercice 013 : Configuration des logs BIND
#
# Usage : sudo ./bind_logs.sh
#
# Deux types de logs, chacun dans son fichier :
#   - /var/log/named/default.log : le fonctionnement de BIND (démarrage,
#     chargement des zones, erreurs...)
#   - /var/log/named/queries.log : chaque question reçue (qui a demandé quoi)
#
#   1. Crée le dossier des logs (propriétaire bind, l'utilisateur de BIND).
#   2. Écrit /etc/bind/named.conf.logging et l'inclut dans named.conf.
#   3. Vérifie, redémarre BIND, active les requêtes avec rndc querylog on.
#   4. Fait quelques requêtes puis affiche les logs.

set -u

LOG_DIR="/var/log/named"
CONF="/etc/bind/named.conf.logging"
DOMAIN="je-le-trouve-beau-mon-domain-donc-il-est-beau.com"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# 1. Dossier des logs
mkdir -p "$LOG_DIR"
chown bind:bind "$LOG_DIR"

# 2. Configuration : un "channel" = une destination (fichier, taille max,
#    nombre d'anciens fichiers gardés) ; une "category" = un type de message
cat > "$CONF" <<CONF
logging {
    channel default_log {
        file "$LOG_DIR/default.log" versions 3 size 5m;
        severity info;
        print-time yes;
        print-severity yes;
        print-category yes;
    };
    channel query_log {
        file "$LOG_DIR/queries.log" versions 3 size 5m;
        severity info;
        print-time yes;
    };

    category default { default_log; };
    category queries { query_log; };
};
CONF

grep -q "include \"$CONF\";" /etc/bind/named.conf || echo "include \"$CONF\";" >> /etc/bind/named.conf

# 3. Vérification, redémarrage, logs de requêtes activés
named-checkconf || exit 1
systemctl restart named
sleep 1
rndc querylog on

# 4. Quelques requêtes pour remplir les logs, puis affichage
for name in www toto me; do
    dig +short "$name.$DOMAIN" @127.0.0.1 >/dev/null
done
dig +short google.com @127.0.0.1 >/dev/null
sleep 1

echo "=== $LOG_DIR/default.log (fin)"
tail -n 10 "$LOG_DIR/default.log"
echo
echo "=== $LOG_DIR/queries.log (fin)"
tail -n 10 "$LOG_DIR/queries.log"
echo
echo "Suivre en direct : tail -f $LOG_DIR/queries.log"
echo "Couper / remettre les logs de requêtes : rndc querylog off / on"
