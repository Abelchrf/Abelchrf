#!/bin/bash
#
# Exercice 3 : Création des utilisateurs du serveur mail depuis un CSV
#
# Usage : sudo ./mail_users.sh [fichier.csv]
#         (par défaut : users.csv placé à côté du script)
#
# Sur ce serveur, un compte mail = un utilisateur Linux :
#   login "tbutchers"  ->  adresse tbutchers@etna.nx, boîte /var/spool/mail/tbutchers
#
#   1. Lit le CSV (colonnes repérées par leur nom dans l'en-tête).
#   2. Crée l'utilisateur s'il n'existe pas, avec le shell /usr/sbin/nologin :
#      il peut lire ses mails mais pas se connecter en SSH.
#   3. Lui donne un mot de passe (pwgen), noté dans /root/mail_users.txt.
#   4. Si le CSV contient une adresse mail (tbutchers0@howstuffworks.com),
#      sa partie avant @ devient un alias : tbutchers0@etna.nx -> tbutchers.

set -u

CSV="${1:-$(dirname "$0")/users.csv}"
DOMAIN="etna.nx"
PASS_FILE="/root/mail_users.txt"        # format : adresse;login;mot_de_passe

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -r "$CSV" ]] || { echo "Fichier CSV introuvable : $CSV" >&2; exit 1; }
command -v pwgen >/dev/null || apt-get install -y -qq pwgen >/dev/null

# Copie nettoyée : sans \r ni BOM, un utilisateur par ligne (le copier-coller
# depuis l'intranet peut tout coller sur une seule ligne)
CLEAN=$(mktemp)
trap 'rm -f "$CLEAN"' EXIT
sed 's/^\xEF\xBB\xBF//' "$CSV" | tr -d '\r"' | sed -E 's/[[:space:]]+([0-9]+,)/\n\1/g' > "$CLEAN"

IFS=, read -r -a HEADER < <(head -n 1 "$CLEAN" | tr 'A-Z' 'a-z')

# col nom1 nom2 ... : index de la première colonne portant l'un de ces noms
col() {
    local name i
    for name in "$@"; do
        for i in "${!HEADER[@]}"; do
            [[ "${HEADER[$i]// /}" == "$name" ]] && { echo "$i"; return; }
        done
    done
}
# get INDEX : valeur de cette colonne pour la ligne courante (tableau F)
get() { [[ -n "$1" ]] && echo "${F[$1]:-}" | sed 's/^ *//; s/ *$//'; }
# clean NOM : minuscules, sans accents, uniquement a-z et 0-9
clean() {
    local s
    s=$(echo "$1" | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null || echo "$1")
    s=$(echo "$s" | tr 'A-Z' 'a-z' | tr -cd 'a-z0-9')
    [[ "$s" =~ ^[a-z] ]] || s="u$s"
    echo "${s:0:32}"
}

C_LOGIN=$(col username login user)
C_FIRST=$(col first_name firstname prenom)
C_LAST=$(col last_name lastname nom)
C_EMAIL=$(col email mail e-mail adresse)
if [[ -z "$C_LOGIN" && -z "$C_EMAIL" && ( -z "$C_FIRST" || -z "$C_LAST" ) ]]; then
    echo "Colonnes attendues : username, ou first_name + last_name, ou email." >&2
    echo "En-tête trouvé : ${HEADER[*]}" >&2
    exit 1
fi

( umask 077; touch "$PASS_FILE" )
created=0; existing=0; aliases=0

while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" ]] && continue
    IFS=, read -r -a F <<< "$line"
    email=$(get "$C_EMAIL")
    first=$(get "$C_FIRST"); last=$(get "$C_LAST")

    # 1. Login : colonne username, sinon initiale + nom (comme la séquence 01),
    #    sinon la partie avant @ de l'adresse
    if [[ -n "$C_LOGIN" && -n "$(get "$C_LOGIN")" ]]; then
        login=$(clean "$(get "$C_LOGIN")")
    elif [[ -n "$first$last" ]]; then
        login=$(clean "${first:0:1}$last")
    else
        login=$(clean "${email%%@*}")
    fi

    # 2. Création du compte (pas de shell : compte mail uniquement)
    if id "$login" >/dev/null 2>&1; then
        existing=$((existing + 1))
    else
        useradd -m -s /usr/sbin/nologin -c "$first $last" "$login" || continue
        created=$((created + 1))
    fi

    # 3. Mot de passe : un seul par utilisateur (relancer le script ne le
    #    change pas). chpasswd prend "login:motdepasse" sur l'entrée standard.
    if ! grep -q ";$login;" "$PASS_FILE"; then
        password=$(pwgen -s 12 1)
        echo "$login:$password" | chpasswd
        echo "$login@$DOMAIN;$login;$password" >> "$PASS_FILE"
    fi

    # 4. Alias depuis l'adresse du CSV (tbutchers0 -> tbutchers)
    alias_name=$(echo "${email%%@*}" | tr 'A-Z' 'a-z' | tr -cd 'a-z0-9._-')
    if [[ -n "$alias_name" && "$alias_name" != "$login" ]] && ! grep -q "^$alias_name:" /etc/aliases; then
        echo "$alias_name: $login" >> /etc/aliases
        aliases=$((aliases + 1))
    fi
done < <(tail -n +2 "$CLEAN")

newaliases                       # prise en compte de /etc/aliases par Postfix

echo "Comptes créés : $created | Déjà existants : $existing | Alias ajoutés : $aliases"
echo "Adresses et mots de passe : $PASS_FILE (root uniquement)"
first_user=$(head -n 1 "$PASS_FILE" | cut -d';' -f2)
if [[ -n "$first_user" ]]; then
    echo "Test : mail envoyé à $first_user@$DOMAIN"
    echo "Bienvenue sur le serveur mail $DOMAIN" | mail -s "Bienvenue $first_user" "$first_user@$DOMAIN"
    sleep 2
    grep -c "^From " "/var/spool/mail/$first_user" | sed "s/^/  messages dans la boîte de $first_user : /"
fi
