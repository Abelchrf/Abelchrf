#!/bin/bash
#
# Exercice 002 : Gestion des groupes à partir d'un fichier CSV
#
# Usage : sudo ./manage_groups.sh [fichier.csv]
#         (par défaut : groups.csv placé à côté du script)
#
# Format attendu : une ligne par utilisateur, ses groupes séparés par ";" (ou "|")
#
#     username,groups
#     jdoe,dev;web
#     asmith,dev;admin;support
#
# Le script accepte aussi directement users.csv s'il possède une colonne de
# groupes (group, groups, groupe, department...) : le login est alors
# construit comme dans l'exercice 001 (initiale du prénom + nom).
#
# Pour chaque ligne :
#   1. chaque groupe absent du système est créé (groupadd) ;
#   2. l'utilisateur est ajouté à tous ses groupes (usermod -aG), sans être
#      retiré des groupes dont il fait déjà partie.

set -u

CSV="${1:-$(dirname "$0")/groups.csv}"

# --- Vérifications préalables -------------------------------------------------

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

if [[ ! -r "$CSV" ]]; then
    echo "Fichier CSV introuvable : $CSV" >&2
    exit 1
fi

# --- Fonctions utilitaires (mêmes principes que l'exercice 001) --------------

# Lit la première ligne (minuscules, sans BOM, sans guillemets ni \r).
# Si elle commence par un nombre, il n'y a pas d'en-tête (cas du users.csv de
# l'intranet : 1,Thorndike,Butchers,tbutchers0@...,Male,Outdoors,11/25/2023) :
# on utilise alors l'ordre des colonnes de ce fichier.
FIRST_LINE=$(head -n 1 "$CSV" | sed 's/^\xEF\xBB\xBF//' | tr -d '\r"' | tr 'A-Z' 'a-z')
if [[ "$FIRST_LINE" =~ ^[0-9]+, ]]; then
    HEADER=(id first_name last_name email gender department date)
    START=1
else
    IFS=, read -r -a HEADER <<< "$FIRST_LINE"
    START=2
fi

# col nom1 nom2 ... : index de la première colonne portant l'un de ces noms.
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

# get INDEX : valeur de la colonne INDEX pour la ligne courante (tableau F).
get() {
    [[ -z "$1" ]] && return
    echo "${F[$1]:-}" | tr -d '"' | sed 's/^ *//; s/ *$//'
}

# clean_login TEXTE : même règle que l'exercice 001, pour retrouver les
# mêmes logins (minuscules, sans accents, a-z 0-9, 32 caractères max).
clean_login() {
    local s
    s=$(echo "$1" | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null || echo "$1")
    s=$(echo "$s" | tr 'A-Z' 'a-z' | tr -cd 'a-z0-9')
    [[ "$s" =~ ^[a-z] ]] || s="u$s"
    echo "${s:0:32}"
}

# clean_group TEXTE : nom de groupe valide ("Ressources Humaines" ->
# ressources_humaines) : a-z 0-9 _ -, commence par une lettre, 32 max.
clean_group() {
    local s
    s=$(echo "$1" | sed 's/^ *//; s/ *$//' | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null || echo "$1")
    s=$(echo "$s" | tr 'A-Z ' 'a-z_' | tr -cd 'a-z0-9_-')
    [[ "$s" =~ ^[a-z] ]] || s="g$s"
    echo "${s:0:32}"
}

C_LOGIN=$(col username user_name login user utilisateur)
C_FIRST=$(col first_name firstname prenom prénom)
C_LAST=$(col last_name lastname nom)
C_GROUPS=$(col groups group groupes groupe department)

if [[ -z "$C_GROUPS" ]]; then
    echo "Aucune colonne de groupes (groups, group, groupe...) dans : ${HEADER[*]}" >&2
    exit 1
fi
if [[ -z "$C_LOGIN" && ( -z "$C_FIRST" || -z "$C_LAST" ) ]]; then
    echo "Le CSV doit contenir une colonne username/login, ou first_name et last_name." >&2
    exit 1
fi

# --- Traitement de chaque ligne -----------------------------------------------

new_groups=0; memberships=0; skipped=0

while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    [[ -z "$line" ]] && continue
    IFS=, read -r -a F <<< "$line"

    if [[ -n "$C_LOGIN" && -n "$(get "$C_LOGIN")" ]]; then
        login=$(clean_login "$(get "$C_LOGIN")")
    else
        first=$(get "$C_FIRST")
        login=$(clean_login "${first:0:1}$(get "$C_LAST")")
    fi

    # "dev;web|admin" -> une ligne par groupe -> tableau (séparateurs : ; ou |)
    mapfile -t wanted < <(get "$C_GROUPS" | tr ';|' '\n\n')

    valid=()
    for g in "${wanted[@]}"; do
        [[ -z "$g" ]] && continue
        g=$(clean_group "$g")
        # 1. getent interroge la base des groupes : s'il ne trouve rien, on crée
        if ! getent group "$g" >/dev/null; then
            groupadd "$g" || continue
            echo "[GROUPE] $g créé"
            new_groups=$((new_groups + 1))
        fi
        valid+=("$g")
    done
    [[ ${#valid[@]} -eq 0 ]] && continue

    if ! id "$login" >/dev/null 2>&1; then
        echo "[IGNORE] $login n'existe pas (lancer d'abord l'exercice 001)" >&2
        skipped=$((skipped + 1))
        continue
    fi

    # 2. -G : liste des groupes secondaires (séparés par des virgules)
    #    -a : AJOUTE à la liste existante. Sans -a, l'utilisateur serait retiré
    #         de tous les groupes non cités !
    #    Équivalent groupe par groupe : gpasswd -a "$login" "$g"
    usermod -aG "$(IFS=,; echo "${valid[*]}")" "$login"
    echo "[MEMBRE] $login -> ${valid[*]}"
    memberships=$((memberships + ${#valid[@]}))
done < <(tail -n +"$START" "$CSV")

echo
echo "Groupes créés : $new_groups | Affectations : $memberships | Utilisateurs ignorés : $skipped"
echo "Vérifier un utilisateur : id <login>    Vérifier un groupe : getent group <groupe>"
