#!/bin/bash
#
# Exercice 008 : Sécuriser les partages Samba
#
# Usage : sudo ./secure.sh
#
#   1. Réglages de sécurité généraux :
#        - plus d'accès invité/anonyme (map to guest = never, restrict anonymous = 2)
#        - protocole SMB2 minimum (SMB1 est vieux et dangereux), NTLMv2 seulement
#        - chiffrement des échanges proposé (smb encrypt = desired)
#   2. Politique de mots de passe Samba (pdbedit) : 10 caractères minimum,
#      compte bloqué 30 min après 5 erreurs.
#   3. Mots de passe Samba de tous les utilisateurs (synchronisés avec
#      /root/samba_users.txt de l'exercice 001).
#   4. Tests smbclient : anonyme, mauvais mot de passe, bon mot de passe,
#      puis les lignes d'authentification dans les logs.

set -u

SECURITY="/etc/samba/conf.d/security.conf"
PASS_FILE="/root/samba_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
[[ -f "$PASS_FILE" ]] || { echo "Lancer d'abord l'exercice 001." >&2; exit 1; }

# 1. Réglages généraux, dans leur propre fichier inclus sous [global]
cat > "$SECURITY" <<'CONF'
   map to guest = never
   restrict anonymous = 2
   server min protocol = SMB2_10
   ntlm auth = ntlmv2-only
   smb encrypt = desired
CONF
grep -q "include = $SECURITY" /etc/samba/smb.conf || sed -i "/^\[global\]/a include = $SECURITY" /etc/samba/smb.conf
testparm -s >/dev/null 2>&1 || { testparm -s; exit 1; }

# 2. Politique de mots de passe
pdbedit -P "min password length" -C 10 >/dev/null
pdbedit -P "bad lockout attempt" -C 5 >/dev/null
pdbedit -P "lockout duration" -C 30 >/dev/null

# 3. Mots de passe Samba
count=0
while IFS=';' read -r u p; do
    printf '%s\n%s\n' "$p" "$p" | smbpasswd -s -a "$u" >/dev/null && count=$((count + 1))
    smbpasswd -e "$u" >/dev/null                      # compte activé
done < "$PASS_FILE"
echo "$count comptes Samba synchronisés"
systemctl restart smbd
sleep 2

# 4. Tests
read -r u p < <(sed -n 1p "$PASS_FILE" | tr ';' ' ')
echo "--- Accès anonyme (sans compte)"
smbclient -N -L //localhost 2>&1 | tail -n 1
echo "--- $u avec un mauvais mot de passe"
smbclient "//localhost/$u" -U "$u%mauvais" -c "ls" 2>&1 | tail -n 1
echo "--- $u avec son mot de passe, connexion chiffrée (vue par smbstatus)"
{ echo "ls"; sleep 3; echo "quit"; } \
    | smbclient "//localhost/$u" -U "$u%$p" --option='client smb encrypt=required' >/dev/null 2>&1 &
sleep 1.5
smbstatus -b | sed -n '3p;5,$p'          # colonne Encryption : AES-128-GCM
wait
echo "--- Logs d'authentification"
grep -rh "Auth:" /var/log/samba/ 2>/dev/null | sed -E 's/ at \[[^]]*\]//; s/ workstation.*//' | tail -n 3
echo
echo "Changer le mot de passe Samba d'un utilisateur : smbpasswd <login>"
echo "Désactiver un compte : smbpasswd -d <login>    Liste : pdbedit -L -v"
