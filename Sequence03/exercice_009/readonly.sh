#!/bin/bash
#
# Exercice 009 : Partage en lecture seule
#
# Usage : sudo ./readonly.sh
#
# Le partage [lecture] (/srv/samba/lecture) est en lecture seule pour ses
# lecteurs, et un seul utilisateur (le "rédacteur") peut y écrire.
# Deux niveaux de protection :
#   - Samba : read only = yes, write list = le rédacteur
#   - Linux : dossier 755 appartenant au rédacteur (les autres : r-x)
#
#   1. Crée le dossier et un document d'exemple.
#   2. Crée le partage (lecteurs = utilisateurs 2 et 3, rédacteur = utilisateur 1).
#   3. Tests : le lecteur lit mais ne peut pas écrire ; le rédacteur écrit ; ls -l.

set -u

SHARE="lecture"
DIR="/srv/samba/$SHARE"
CONF="/etc/samba/conf.d/$SHARE.conf"
PASS_FILE="/root/samba_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f "$PASS_FILE" ]] || { echo "Lancer d'abord l'exercice 001." >&2; exit 1; }

read -r writer wpass < <(sed -n 1p "$PASS_FILE" | tr ';' ' ')
read -r reader rpass < <(sed -n 2p "$PASS_FILE" | tr ';' ' ')
reader2=$(sed -n 3p "$PASS_FILE" | cut -d';' -f1)
for u in "$writer" "$reader" "$reader2"; do
    p=$(grep "^$u;" "$PASS_FILE" | cut -d';' -f2)
    printf '%s\n%s\n' "$p" "$p" | smbpasswd -s -a "$u" >/dev/null
done

# 1. Dossier
mkdir -p "$DIR"
echo "Règlement intérieur : à lire, pas à modifier." > "$DIR/reglement.txt"
chown -R "$writer": "$DIR"
chmod 755 "$DIR"
chmod 644 "$DIR/reglement.txt"

# 2. Partage
cat > "$CONF" <<CONF
[$SHARE]
   comment = Documents en lecture seule
   path = $DIR
   valid users = $writer $reader $reader2
   read only = yes
   write list = $writer
CONF
grep -q "include = $CONF" /etc/samba/smb.conf || echo "include = $CONF" >> /etc/samba/smb.conf
testparm -s >/dev/null 2>&1 || { testparm -s; exit 1; }
systemctl reload smbd

# 3. Tests
echo "nouveau" > /tmp/ro_test.txt
echo "--- $reader (lecteur) lit le règlement"
smbclient "//localhost/$SHARE" -U "$reader%$rpass" -c "get reglement.txt /tmp/reglement_lu.txt" 2>&1 | tail -n 1
echo "--- $reader (lecteur) essaie d'écrire"
smbclient "//localhost/$SHARE" -U "$reader%$rpass" -c "put /tmp/ro_test.txt essai.txt" 2>&1 | tail -n 1
echo "--- $writer (rédacteur) écrit"
smbclient "//localhost/$SHARE" -U "$writer%$wpass" -c "put /tmp/ro_test.txt note_$writer.txt" 2>&1 | tail -n 1
rm -f /tmp/ro_test.txt /tmp/reglement_lu.txt
echo "--- ls -l $DIR"
ls -l "$DIR"
