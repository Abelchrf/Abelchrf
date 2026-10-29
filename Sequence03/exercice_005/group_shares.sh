#!/bin/bash
#
# Exercice 005 : Partages par groupe
#
# Usage : sudo ./group_shares.sh [fichier.csv]
#         (défaut : ../exercice_001/users.csv, colonne "group")
#
# Chaque groupe du CSV (Outdoors, Toys...) a son partage, ouvert à ses
# seuls membres :  \\serveur\outdoors  ->  /srv/samba/groupes/outdoors
#   1. Lit la colonne group : crée le groupe Linux, y ajoute l'utilisateur.
#   2. Crée le dossier (root:groupe, 2770) et le partage [groupe]
#      (valid users = @groupe, force group : fichiers partagés par le groupe).
#   3. Test : un membre se connecte ; pendant la connexion, smbstatus montre
#      qui est connecté, à quel partage ; un non-membre est refusé.

set -u

CSV="${1:-$(dirname "$0")/../exercice_001/users.csv}"
BASE="/srv/samba/groupes"
CONF="/etc/samba/conf.d/groupes.conf"
PASS_FILE="/root/samba_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -r "$CSV" && -f "$PASS_FILE" ]] || { echo "Lancer d'abord l'exercice 001 (users.csv)." >&2; exit 1; }

CLEAN=$(mktemp)
trap 'rm -f "$CLEAN"' EXIT
sed 's/^\xEF\xBB\xBF//' "$CSV" | tr -d '\r"' | sed -E 's/[[:space:]]+([0-9]+,)/\n\1/g' > "$CLEAN"
IFS=, read -r -a HEADER < <(head -n 1 "$CLEAN" | tr 'A-Z' 'a-z')
col() { local i; for i in "${!HEADER[@]}"; do [[ "${HEADER[$i]// /}" == "$1" ]] && { echo "$i"; return; }; done; }
clean() {
    local s
    s=$(echo "$1" | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null || echo "$1")
    s=$(echo "$s" | tr 'A-Z' 'a-z' | tr -cd 'a-z0-9')
    [[ "$s" =~ ^[a-z] ]] || s="g$s"
    echo "${s:0:32}"
}
C_FIRST=$(col first_name); C_LAST=$(col last_name); C_GROUP=$(col group)
[[ -n "$C_GROUP" ]] || { echo "Pas de colonne group dans $CSV" >&2; exit 1; }

# 1. Groupes et membres
declare -A GROUPS_SEEN
while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" ]] && continue
    IFS=, read -r -a F <<< "$line"
    login=$(clean "${F[$C_FIRST]:0:1}${F[$C_LAST]}")
    group=$(clean "${F[$C_GROUP]:-}")
    [[ -z "${F[$C_GROUP]:-}" ]] && continue
    getent group "$group" >/dev/null || groupadd "$group"
    id "$login" >/dev/null 2>&1 && usermod -aG "$group" "$login"
    GROUPS_SEEN[$group]=1
done < <(tail -n +2 "$CLEAN")

# 2. Un dossier + un partage par groupe
: > "$CONF"
for group in $(printf '%s\n' "${!GROUPS_SEEN[@]}" | sort); do
    mkdir -p "$BASE/$group"
    chown root:"$group" "$BASE/$group"
    chmod 2770 "$BASE/$group"
    cat >> "$CONF" <<CONF
[$group]
   comment = Partage du groupe $group
   path = $BASE/$group
   valid users = @$group
   force group = $group
   read only = no
   create mask = 0660
   directory mask = 2770

CONF
done
grep -q "include = $CONF" /etc/samba/smb.conf || echo "include = $CONF" >> /etc/samba/smb.conf
testparm -s >/dev/null 2>&1 || { testparm -s; exit 1; }
systemctl reload smbd
echo "${#GROUPS_SEEN[@]} partages de groupe créés dans $BASE"

# 3. Test avec le premier utilisateur et son groupe
read -r u p < <(sed -n 1p "$PASS_FILE" | tr ';' ' ')
printf '%s\n%s\n' "$p" "$p" | smbpasswd -s -a "$u" >/dev/null
g=$(id -nG "$u" | tr ' ' '\n' | grep -xF -f <(printf '%s\n' "${!GROUPS_SEEN[@]}") | head -n 1)
other=$(printf '%s\n' "${!GROUPS_SEEN[@]}" | grep -vx "$g" | head -n 1)
echo "--- $u (groupe $g) se connecte à \\\\serveur\\$g et y reste 4 secondes"
{ echo "mkdir test_$u"; sleep 4; echo "quit"; } | smbclient "//localhost/$g" -U "$u%$p" >/dev/null 2>&1 &
sleep 2
echo "--- smbstatus pendant la connexion"
smbstatus -S
smbstatus -b | tail -n +4
wait
echo "--- $u essaie le partage d'un autre groupe ($other)"
smbclient "//localhost/$other" -U "$u%$p" -c "ls" 2>&1 | tail -n 1
echo "--- Droits"
ls -ld "$BASE/$g" "$BASE/$g/test_$u"
