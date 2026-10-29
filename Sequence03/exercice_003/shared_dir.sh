#!/bin/bash
#
# Exercice 003 : Un dossier partagé pour certains utilisateurs
#
# Usage : sudo ./shared_dir.sh [login1 login2 ...]
#         (par défaut : les 3 premiers utilisateurs de l'exercice 001)
#
#   1. Crée le groupe "partage" et y met les utilisateurs choisis.
#   2. Crée /srv/samba/partage (propriétaire root, groupe partage, 2770 :
#      seuls les membres entrent ; le "2" = setgid, les fichiers créés
#      appartiennent au groupe partage).
#   3. Donne un mot de passe Samba à ces utilisateurs (smbpasswd) : Samba a
#      sa propre liste de mots de passe, on reprend ceux de l'exercice 001.
#   4. Déclare le partage [partage] (valid users = @partage).
#   5. Tests avec smbclient (comme un autre client du réseau) + logs.

set -u

SHARE="partage"
DIR="/srv/samba/$SHARE"
CONF="/etc/samba/conf.d/$SHARE.conf"
PASS_FILE="/root/samba_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f "$PASS_FILE" ]] || { echo "Lancer d'abord l'exercice 001." >&2; exit 1; }

if [[ $# -gt 0 ]]; then users=("$@"); else mapfile -t users < <(head -n 3 "$PASS_FILE" | cut -d';' -f1); fi
pass_of() { grep "^$1;" "$PASS_FILE" | cut -d';' -f2; }

# 1. Groupe
getent group "$SHARE" >/dev/null || groupadd "$SHARE"
for u in "${users[@]}"; do usermod -aG "$SHARE" "$u"; done

# 2. Dossier
mkdir -p "$DIR"
chown root:"$SHARE" "$DIR"
chmod 2770 "$DIR"

# 3. Mots de passe Samba (-a : ajouter, -s : lire le mot de passe sur stdin)
for u in "${users[@]}"; do
    p=$(pass_of "$u")
    printf '%s\n%s\n' "$p" "$p" | smbpasswd -s -a "$u" >/dev/null
done

# 4. Le partage
cat > "$CONF" <<CONF
[$SHARE]
   comment = Dossier partagé (exercice 003)
   path = $DIR
   valid users = @$SHARE
   read only = no
   browseable = yes
   create mask = 0660
   directory mask = 2770
CONF
grep -q "include = $CONF" /etc/samba/smb.conf || echo "include = $CONF" >> /etc/samba/smb.conf
testparm -s >/dev/null 2>&1 || { testparm -s; exit 1; }
systemctl reload smbd

# 5. Tests
u="${users[0]}"; p=$(pass_of "$u")
echo "Bonjour depuis $u" > /tmp/test_$u.txt
echo "--- $u (membre) dépose un fichier et liste le partage"
smbclient "//localhost/$SHARE" -U "$u%$p" -c "put /tmp/test_$u.txt test_$u.txt; ls" 2>&1 | grep -vE "^$|blocks"
rm -f /tmp/test_$u.txt

outsider=$(cut -d';' -f1 "$PASS_FILE" | grep -vxF -f <(printf '%s\n' "${users[@]}") | head -n 1)
if [[ -n "$outsider" ]]; then
    po=$(pass_of "$outsider")
    printf '%s\n%s\n' "$po" "$po" | smbpasswd -s -a "$outsider" >/dev/null
    echo "--- $outsider (pas membre) essaie d'entrer"
    smbclient "//localhost/$SHARE" -U "$outsider%$po" -c "ls" 2>&1 | tail -n 1
fi

echo "--- ls -l $DIR"
ls -l "$DIR"
echo "--- Logs Samba (dernières connexions)"
#   "Auth: ... status [NT_STATUS_OK]"  = connexion acceptée (mot de passe bon)
#   "not permitted to access this share" = refus du partage (pas membre)
grep -rhE "Auth:|not permitted to access this share \($SHARE\)" /var/log/samba/ 2>/dev/null \
    | sed -E 's/ at \[[^]]*\]//; s/ workstation.*//' | tail -n 4
echo
echo "Depuis Windows : \\\\$(hostname -I | awk '{print $1}')\\$SHARE"
echo "Depuis Linux   : smbclient //$(hostname -I | awk '{print $1}')/$SHARE -U $u"
