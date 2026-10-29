#!/bin/bash
#
# Exercice 004 : Un partage personnel par utilisateur
#
# Usage : sudo ./homes.sh
#
# Samba a une section spéciale [homes] : quand "tbutchers" se connecte à
# \\serveur\tbutchers, Samba lui partage automatiquement /home/tbutchers.
# Pas besoin d'écrire un partage par personne.
#   1. Active [homes] : seul le propriétaire entre (valid users = %S),
#      partage invisible dans la liste (browseable = no).
#   2. Donne un mot de passe Samba à tous les utilisateurs de l'exercice 001.
#   3. Tests smbclient : un utilisateur écrit dans SON partage, et un autre
#      utilisateur est refusé.

set -u

CONF="/etc/samba/conf.d/homes.conf"
PASS_FILE="/root/samba_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f "$PASS_FILE" ]] || { echo "Lancer d'abord l'exercice 001." >&2; exit 1; }

# 1. Le smb.conf de Debian contient déjà un [homes] : on le désactive et on
#    met le nôtre dans conf.d
sed -i 's/^\[homes\]/[homes-debian-desactive]/' /etc/samba/smb.conf
cat > "$CONF" <<'CONF'
[homes]
   comment = Dossier personnel de %S
   # %S = nom du partage demandé = le login ; seul lui peut entrer
   valid users = %S
   read only = no
   browseable = no
   create mask = 0600
   directory mask = 0700
CONF
grep -q "include = $CONF" /etc/samba/smb.conf || echo "include = $CONF" >> /etc/samba/smb.conf
testparm -s >/dev/null 2>&1 || { testparm -s; exit 1; }

# 2. Mots de passe Samba de tous les utilisateurs
count=0
while IFS=';' read -r u p; do
    printf '%s\n%s\n' "$p" "$p" | smbpasswd -s -a "$u" >/dev/null && count=$((count + 1))
done < "$PASS_FILE"
echo "$count utilisateurs Samba (liste : pdbedit -L)"
systemctl reload smbd

# 3. Tests
read -r u1 p1 < <(sed -n 1p "$PASS_FILE" | tr ';' ' ')
read -r u2 p2 < <(sed -n 2p "$PASS_FILE" | tr ';' ' ')
echo "Fichier de $u1" > /tmp/perso.txt
echo "--- $u1 écrit dans \\\\serveur\\$u1"
smbclient "//localhost/$u1" -U "$u1%$p1" -c "put /tmp/perso.txt perso.txt; ls perso.txt" 2>&1 | grep perso
echo "--- $u2 essaie d'ouvrir \\\\serveur\\$u1"
smbclient "//localhost/$u1" -U "$u2%$p2" -c "ls" 2>&1 | tail -n 1
rm -f /tmp/perso.txt
echo "--- Droits sur le disque"
ls -l "/home/$u1/perso.txt"
