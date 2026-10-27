#!/bin/bash
#
# Exercice 006 : requêtes DNS avec nslookup et host
#
# Usage : ./dns.sh [domaine ...]
#         (par défaut : exemple.com google.com etna.io et le nom de la machine)
#
# Le DNS traduit un nom (google.com) en adresse IP (142.250.x.x).
# Pour chaque domaine, le script affiche :
#   - la réponse de nslookup (serveur DNS interrogé + adresses trouvées) ;
#   - la réponse de host (plus courte : adresses IPv4/IPv6 et serveurs mail).

# nslookup et host sont fournis par le paquet bind9-dnsutils
if ! command -v nslookup >/dev/null || ! command -v host >/dev/null; then
    echo "Installation de bind9-dnsutils..."
    sudo apt-get update -qq && sudo apt-get install -y -qq bind9-dnsutils >/dev/null
fi

if [[ $# -gt 0 ]]; then
    domains=("$@")
else
    domains=(exemple.com google.com etna.io "$(hostname)")
fi

for domain in "${domains[@]}"; do
    echo "=================================================="
    echo " $domain"
    echo "=================================================="
    echo "--- nslookup $domain"
    nslookup "$domain" || echo "(aucune réponse pour $domain)"
    echo "--- host $domain"
    host "$domain" || echo "(aucune réponse pour $domain)"
    echo
done
