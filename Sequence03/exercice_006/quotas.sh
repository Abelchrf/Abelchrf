#!/bin/bash
#
# Exercice 006 : Quotas disque pour les utilisateurs Samba
#
# Usage : sudo ./quotas.sh [soft] [hard]     (défaut : 5M et 10M par utilisateur)
#
# Un quota disque limite la place qu'un utilisateur peut occuper :
#   - limite "soft" (douce) : on peut la dépasser pendant 7 jours (avertissement)
#   - limite "hard" (dure)  : impossible d'aller au-delà
# Les quotas Linux s'activent sur un système de fichiers entier. Pour ne pas
# toucher au disque principal, on crée un petit disque virtuel (fichier de
# 200 Mo formaté en ext4) monté sur /srv/samba/quota avec l'option usrquota.
#
#   1. Installe les outils de quota, crée et monte le disque virtuel.
#   2. Active les quotas (quotacheck, quotaon).
#   3. Fixe un quota pour chaque utilisateur (setquota) et crée le partage [quota].
#   4. Tests : repquota, puis un utilisateur essaie d'envoyer 12 Mo -> refusé.

set -u

SOFT="${1:-5M}"
HARD="${2:-10M}"
IMG="/srv/samba-quota.img"
DIR="/srv/samba/quota"
CONF="/etc/samba/conf.d/quota.conf"
PASS_FILE="/root/samba_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f "$PASS_FILE" ]] || { echo "Lancer d'abord l'exercice 001." >&2; exit 1; }

# 1. Outils + disque virtuel (une seule fois)
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq quota >/dev/null
if [[ ! -f "$IMG" ]]; then
    dd if=/dev/zero of="$IMG" bs=1M count=200 status=none
    mkfs.ext4 -q "$IMG"
fi
mkdir -p "$DIR"
# fstab : le disque est remonté automatiquement au démarrage, avec usrquota
grep -q "^$IMG " /etc/fstab || echo "$IMG $DIR ext4 loop,usrquota 0 0" >> /etc/fstab
mountpoint -q "$DIR" || mount "$DIR" || exit 1
chmod 1777 "$DIR"            # tout le monde écrit, chacun ne supprime que ses fichiers

# 2. Activation des quotas : quotacheck compte ce que chacun occupe déjà
quotaoff "$DIR" 2>/dev/null
quotacheck -cum "$DIR"
quotaon "$DIR"

# 3. Quota par utilisateur (tailles en Ko pour setquota) + partage
to_kb() { numfmt --from=iec "$1" | awk '{print int($1 / 1024)}'; }
while IFS=';' read -r u p; do
    # setquota user soft_blocs hard_blocs soft_fichiers hard_fichiers dossier
    setquota -u "$u" "$(to_kb "$SOFT")" "$(to_kb "$HARD")" 0 0 "$DIR"
    printf '%s\n%s\n' "$p" "$p" | smbpasswd -s -a "$u" >/dev/null
done < "$PASS_FILE"

cat > "$CONF" <<CONF
[quota]
   comment = Partage avec quotas ($SOFT / $HARD par utilisateur)
   path = $DIR
   read only = no
   valid users = $(cut -d';' -f1 "$PASS_FILE" | tr '\n' ' ')
CONF
grep -q "include = $CONF" /etc/samba/smb.conf || echo "include = $CONF" >> /etc/samba/smb.conf
testparm -s >/dev/null 2>&1 || { testparm -s; exit 1; }
systemctl reload smbd

# 4. Tests
echo "--- repquota (5 premières lignes utilisateurs)"
repquota -s "$DIR" | head -n 10

read -r u p < <(sed -n 1p "$PASS_FILE" | tr ';' ' ')
head -c 4M /dev/urandom > /tmp/petit_4M
head -c 12M /dev/urandom > /tmp/gros_12M
echo "--- $u envoie 4 Mo (sous la limite)"
smbclient //localhost/quota -U "$u%$p" -c "put /tmp/petit_4M petit_4M" 2>&1 | tail -n 1
echo "--- $u envoie 12 Mo (au-dessus de la limite dure de $HARD)"
smbclient //localhost/quota -U "$u%$p" -c "put /tmp/gros_12M gros_12M" 2>&1 | tail -n 1
rm -f /tmp/petit_4M /tmp/gros_12M
echo "--- Quota de $u après le test"
quota -s -u "$u" | tail -n 2
