#!/bin/bash
#
# Exercice 003 : Répertoires et permissions pour les groupes
#
# Usage : sudo ./goinfre.sh
#
#   1. Crée /Goinfre, accessible à tous en lecture/écriture/exécution (777).
#   2. Pour chaque groupe existant sur le système, crée /Goinfre/<groupe>.
#   3. Chaque sous-répertoire appartient à root (l'administrateur) et au
#      groupe associé, avec les droits 770 :
#        - root (propriétaire)  : rwx
#        - membres du groupe    : rwx
#        - les autres           : --- (aucun accès)
#
# Le script peut être relancé : mkdir -p ne fait rien si le dossier existe et
# chown/chmod remettent les bons droits (et les nouveaux groupes sont ajoutés).

set -u

GOINFRE="/Goinfre"
ADMIN="root"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# --- 1. Répertoire racine commun ---------------------------------------------

mkdir -p "$GOINFRE"
chown "$ADMIN:$ADMIN" "$GOINFRE"
chmod 777 "$GOINFRE"            # rwx pour le propriétaire, le groupe, les autres
echo "$GOINFRE : $(stat -c '%A %U:%G' "$GOINFRE")"

# --- 2 et 3. Un sous-répertoire par groupe -----------------------------------

# getent group liste tous les groupes (format nom:x:GID:membres) ;
# cut -d: -f1 ne garde que le nom.
count=0
for group in $(getent group | cut -d: -f1 | sort -u); do
    dir="$GOINFRE/$group"
    mkdir -p "$dir"
    chown "$ADMIN:$group" "$dir"    # propriétaire root, groupe = le groupe
    chmod 770 "$dir"                # rwx root, rwx groupe, rien pour les autres
    echo "$dir : $(stat -c '%A %U:%G' "$dir")"
    count=$((count + 1))
done

echo
echo "$count sous-répertoires configurés dans $GOINFRE"
