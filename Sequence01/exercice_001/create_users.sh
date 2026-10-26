#!/bin/bash
#
# Exercice 001 : Création d'utilisateurs à partir de users.csv (Mockaroo)
#
# Usage : sudo ./create_users.sh [fichier.csv]
#         (par défaut : users.csv placé à côté du script)
#
# Pour chaque ligne du CSV, le script :
#   1. construit un login valide (colonne username/login, sinon initiale du
#      prénom + nom : "John Doe" -> jdoe) ;
#   2. crée l'utilisateur avec son home et son shell (useradd), ou le met à
#      jour s'il existe déjà (usermod) : on peut relancer le script sans casse ;
#   3. pour un nouvel utilisateur : prend le mot de passe du CSV ou en génère
#      un avec pwgen, l'applique avec passwd et force son changement à la
#      première connexion ;
#   4. note les identifiants générés dans un fichier lisible par root seul.

set -u

CSV="${1:-$(dirname "$0")/users.csv}"
DEFAULT_SHELL="/bin/bash"
HOME_BASE="/home"
PASS_FILE="/root/users_passwords.txt"

# --- Vérifications préalables -------------------------------------------------

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

if [[ ! -r "$CSV" ]]; then
    echo "Fichier CSV introuvable : $CSV" >&2
    exit 1
fi

if ! command -v pwgen >/dev/null; then
    echo "pwgen absent, installation..."
    apt-get update -qq && apt-get install -y -qq pwgen >/dev/null || {
        echo "Impossible d'installer pwgen." >&2
        exit 1
    }
fi

# --- Fonctions utilitaires ----------------------------------------------------

# Lit l'en-tête du CSV : minuscules, sans BOM, sans guillemets ni \r.
IFS=, read -r -a HEADER < <(head -n 1 "$CSV" | sed 's/^\xEF\xBB\xBF//' | tr -d '\r"' | tr 'A-Z' 'a-z')

# col nom1 nom2 ... : affiche l'index de la première colonne qui porte l'un de
# ces noms (rien si aucune). On ne dépend donc pas de l'ordre des colonnes.
col() {
    local name i
    for name in "$@"; do
        for i in "${!HEADER[@]}"; do
            if [[ "$(echo "${HEADER[$i]}" | sed 's/^ *//; s/ *$//')" == "$name" ]]; then
                echo "$i"
                return
            fi
        done
    done
}

# get INDEX : valeur de la colonne INDEX pour la ligne courante (tableau F),
# sans guillemets ni espaces autour. Vide si la colonne n'existe pas.
get() {
    [[ -z "$1" ]] && return
    echo "${F[$1]:-}" | tr -d '"' | sed 's/^ *//; s/ *$//'
}

# clean_login TEXTE : minuscules, accents retirés, uniquement a-z et 0-9,
# commence par une lettre, 32 caractères maximum (limite de useradd).
clean_login() {
    local s
    s=$(echo "$1" | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null || echo "$1")
    s=$(echo "$s" | tr 'A-Z' 'a-z' | tr -cd 'a-z0-9')
    [[ "$s" =~ ^[a-z] ]] || s="u$s"
    echo "${s:0:32}"
}

C_LOGIN=$(col username user_name login user utilisateur)
C_FIRST=$(col first_name firstname prenom prénom)
C_LAST=$(col last_name lastname nom)
C_PASS=$(col password mot_de_passe passwd)
C_SHELL=$(col shell)
C_HOME=$(col home home_directory homedir)

if [[ -z "$C_LOGIN" && ( -z "$C_FIRST" || -z "$C_LAST" ) ]]; then
    echo "Le CSV doit contenir une colonne username/login, ou first_name et last_name." >&2
    echo "En-tête trouvé : ${HEADER[*]}" >&2
    exit 1
fi

# Fichier des mots de passe générés : créé avec les droits 600 (root seul).
( umask 077; touch "$PASS_FILE" )

# --- Traitement de chaque ligne -----------------------------------------------

declare -A SEEN          # logins déjà attribués pendant cette exécution
created=0; updated=0; failed=0

while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"                      # fichiers au format Windows
    [[ -z "$line" ]] && continue
    IFS=, read -r -a F <<< "$line"

    first=$(get "$C_FIRST")
    last=$(get "$C_LAST")

    # 1. Login
    if [[ -n "$C_LOGIN" && -n "$(get "$C_LOGIN")" ]]; then
        login=$(clean_login "$(get "$C_LOGIN")")
    else
        login=$(clean_login "${first:0:1}${last}")
    fi
    # Deux personnes avec le même login dans le CSV : jdoe, jdoe2, jdoe3...
    base="$login"; n=2
    while [[ -n "${SEEN[$login]:-}" ]]; do
        login="${base:0:30}$n"; n=$((n + 1))
    done
    SEEN[$login]=1

    # 2. Home et shell (valeurs du CSV si présentes et valides)
    home=$(get "$C_HOME")
    [[ -z "$home" ]] && home="$HOME_BASE/$login"
    shell=$(get "$C_SHELL")
    [[ -x "$shell" ]] || shell="$DEFAULT_SHELL"
    fullname=$(echo "$first $last" | tr -d ':,' | sed 's/^ *//; s/ *$//')

    if id "$login" >/dev/null 2>&1; then
        # Utilisateur existant : on aligne son shell et son home sur le CSV.
        # usermod -d ... -m déplace le contenu de l'ancien home vers le nouveau.
        if [[ "$(getent passwd "$login" | cut -d: -f6)" != "$home" ]]; then
            usermod -d "$home" -m "$login"
        fi
        usermod -s "$shell" "$login"
        echo "[MAJ]   $login ($fullname) home=$home shell=$shell"
        updated=$((updated + 1))
        continue
    fi

    # -m : crée le home (copie de /etc/skel), -d : chemin du home,
    # -s : shell de connexion, -c : nom complet (champ GECOS)
    if ! useradd -m -d "$home" -s "$shell" -c "$fullname" "$login"; then
        echo "[ECHEC] $login : useradd a échoué" >&2
        failed=$((failed + 1))
        continue
    fi

    # 3. Mot de passe : celui du CSV, sinon 12 caractères aléatoires (pwgen -s)
    password=$(get "$C_PASS")
    [[ -z "$password" ]] && password=$(pwgen -s 12 1)

    # passwd demande le mot de passe deux fois : on les lui envoie sur stdin.
    printf '%s\n%s\n' "$password" "$password" | passwd "$login" >/dev/null 2>&1
    # -e : mot de passe expiré, l'utilisateur devra le changer à la 1re connexion
    passwd -e "$login" >/dev/null

    echo "$login:$password" >> "$PASS_FILE"
    echo "[CREE]  $login ($fullname) home=$home shell=$shell"
    created=$((created + 1))
done < <(tail -n +2 "$CSV")

echo
echo "Créés : $created | Mis à jour : $updated | Échecs : $failed"
echo "Mots de passe des nouveaux comptes : $PASS_FILE (lisible par root uniquement)"
