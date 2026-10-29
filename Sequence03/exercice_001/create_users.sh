#!/bin/bash
#
# Exercice 001 : Création des utilisateurs depuis users.csv (Mockaroo)
#
# Usage : sudo ./create_users.sh [fichier.csv]   (défaut : users.csv à côté du script)
#
#   1. Lit le CSV (colonnes repérées par leur nom : first_name, last_name...).
#   2. Login = initiale du prénom + nom (Thorndike Butchers -> tbutchers).
#   3. Crée l'utilisateur (useradd) s'il n'existe pas.
#   4. Lui donne un mot de passe (pwgen), noté dans /root/samba_users.txt :
#      il servira aussi pour Samba (exercices suivants).
#   5. Observabilité : affiche les comptes avec getent passwd.

set -u

CSV="${1:-$(dirname "$0")/users.csv}"
PASS_FILE="/root/samba_users.txt"            # format : login;mot_de_passe

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -r "$CSV" ]] || { echo "Fichier CSV introuvable : $CSV" >&2; exit 1; }
command -v pwgen >/dev/null || { apt-get update -qq; apt-get install -y -qq pwgen >/dev/null; }

# Copie nettoyée : sans \r ni guillemets, un utilisateur par ligne
CLEAN=$(mktemp)
trap 'rm -f "$CLEAN"' EXIT
sed 's/^\xEF\xBB\xBF//' "$CSV" | tr -d '\r"' | sed -E 's/[[:space:]]+([0-9]+,)/\n\1/g' > "$CLEAN"
IFS=, read -r -a HEADER < <(head -n 1 "$CLEAN" | tr 'A-Z' 'a-z')

col() {   # col nom1 nom2... : index de la colonne qui porte l'un de ces noms
    local name i
    for name in "$@"; do
        for i in "${!HEADER[@]}"; do
            [[ "${HEADER[$i]// /}" == "$name" ]] && { echo "$i"; return; }
        done
    done
}
get() { [[ -n "$1" ]] && echo "${F[$1]:-}" | sed 's/^ *//; s/ *$//'; }
clean() {   # minuscules, sans accents, a-z 0-9 uniquement
    local s
    s=$(echo "$1" | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null || echo "$1")
    s=$(echo "$s" | tr 'A-Z' 'a-z' | tr -cd 'a-z0-9')
    [[ "$s" =~ ^[a-z] ]] || s="u$s"
    echo "${s:0:32}"
}

C_LOGIN=$(col username login user)
C_FIRST=$(col first_name firstname prenom)
C_LAST=$(col last_name lastname nom)
if [[ -z "$C_LOGIN" && ( -z "$C_FIRST" || -z "$C_LAST" ) ]]; then
    echo "Colonnes attendues : username, ou first_name et last_name. En-tête : ${HEADER[*]}" >&2
    exit 1
fi

( umask 077; touch "$PASS_FILE" )
created=0; existing=0
logins=()

while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" ]] && continue
    IFS=, read -r -a F <<< "$line"
    first=$(get "$C_FIRST"); last=$(get "$C_LAST")
    if [[ -n "$C_LOGIN" && -n "$(get "$C_LOGIN")" ]]; then
        login=$(clean "$(get "$C_LOGIN")")
    else
        login=$(clean "${first:0:1}$last")
    fi

    if id "$login" >/dev/null 2>&1; then
        existing=$((existing + 1))
    else
        # -m : crée /home/<login>   -s : shell   -c : nom complet
        useradd -m -s /bin/bash -c "$first $last" "$login" || continue
        created=$((created + 1))
    fi

    # Un mot de passe par utilisateur, gardé si le script est relancé
    if ! grep -q "^$login;" "$PASS_FILE"; then
        password=$(pwgen -s 12 1)
        echo "$login:$password" | chpasswd        # chpasswd lit "login:motdepasse"
        echo "$login;$password" >> "$PASS_FILE"
    fi
    logins+=("$login")
done < <(tail -n +2 "$CLEAN")

echo "Créés : $created | Déjà existants : $existing"
echo "Mots de passe : $PASS_FILE (root uniquement)"
echo
echo "--- getent passwd (5 premiers comptes du CSV)"
for login in "${logins[@]:0:5}"; do getent passwd "$login"; done
