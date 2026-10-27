#!/bin/bash
#
# Exercice 008 : Installation de BIND9
#
# Usage : sudo ./bind9.sh
#
# BIND9 (service "named") est un serveur DNS : il répond aux questions
# "quelle est l'adresse de google.com ?".
#   1. Installe bind9 et ses outils (apt install bind9).
#   2. Écrit sa configuration (/etc/bind/named.conf.options) : il répond au
#      réseau local et transmet ce qu'il ne connaît pas à 8.8.8.8 / 1.1.1.1.
#   3. Vérifie la configuration, démarre le service (systemctl).
#   4. Teste comme l'exercice 006, mais en interrogeant NOTRE serveur (127.0.0.1).

set -u

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# 1. Installation
apt-get update -qq
apt-get install -y -qq bind9 bind9-utils bind9-dnsutils >/dev/null

# 2. Configuration (copie de sauvegarde de l'original la première fois)
[[ -f /etc/bind/named.conf.options.orig ]] || cp /etc/bind/named.conf.options /etc/bind/named.conf.options.orig

cat > /etc/bind/named.conf.options <<'CONF'
options {
    directory "/var/cache/bind";

    // Écoute sur toutes les interfaces de la machine
    listen-on { any; };
    listen-on-v6 { any; };

    // Qui a le droit de poser des questions : la machine et son réseau local
    allow-query { localhost; localnets; };

    // Résolution des domaines extérieurs (google.com...) pour ces clients,
    // en demandant aux DNS publics de Google et Cloudflare
    recursion yes;
    allow-recursion { localhost; localnets; };
    forwarders { 8.8.8.8; 1.1.1.1; };

    dnssec-validation auto;
};
CONF

# 3. Vérification de la syntaxe puis démarrage
named-checkconf || exit 1
systemctl enable named
systemctl restart named
systemctl is-active named

# 4. Tests : "@127.0.0.1" / "127.0.0.1" = poser la question à notre BIND
for domain in exemple.com google.com etna.io "$(hostname)"; do
    echo "--- nslookup $domain 127.0.0.1"
    nslookup "$domain" 127.0.0.1 | tail -n +4
    echo "--- host $domain 127.0.0.1"
    host "$domain" 127.0.0.1 | tail -n +5
    echo
done
