#!/bin/bash
#
# Exercice 007 : requêtes DNS avancées avec dig
#
# Usage : ./dig.sh [domaine ...]
#         (par défaut : exemple.com google.com gmail.com etna.io et le nom de la machine)
#
# Pour chaque domaine, le script affiche :
#   - A    : adresse(s) IPv4          - AAAA : adresse(s) IPv6
#   - NS   : serveurs DNS qui gèrent le domaine
#   - MX   : serveur(s) de mail du domaine (s'il y en a)
#   - le chemin de la résolution avec dig +trace :
#     serveurs racine (.) -> serveurs du .com -> serveurs du domaine

# dig est fourni par le paquet bind9-dnsutils
if ! command -v dig >/dev/null; then
    echo "Installation de bind9-dnsutils..."
    sudo apt-get update -qq && sudo apt-get install -y -qq bind9-dnsutils >/dev/null
fi

if [[ $# -gt 0 ]]; then
    domains=("$@")
else
    domains=(exemple.com google.com gmail.com etna.io "$(hostname)")
fi

# show TYPE DOMAINE : affiche la réponse courte de dig (+short), ou "aucun"
show() {
    local result
    result=$(dig +short "$2" "$1" | tr '\n' ' ')
    printf '  %-5s %s\n' "$1" "${result:-aucun}"
}

for domain in "${domains[@]}"; do
    echo "=================================================="
    echo " $domain"
    echo "=================================================="
    show A "$domain"
    show AAAA "$domain"
    show NS "$domain"

    # MX : "10 smtp.google.com." -> priorité puis nom du serveur de mail
    mx=$(dig +short "$domain" MX)
    if [[ -n "$mx" ]]; then
        echo "  Serveur(s) de mail :"
        echo "$mx" | sort -n | sed 's/^/    /'
    else
        echo "  Serveur(s) de mail : aucun"
    fi

    # +trace part des serveurs racine et descend jusqu'au domaine.
    # Chaque ligne ";; Received" = une étape (qui a répondu).
    echo "  Chemin de la résolution (dig +trace) :"
    dig +trace "$domain" | grep '^;; Received' | sed 's/^;; /    /'
    echo
done
