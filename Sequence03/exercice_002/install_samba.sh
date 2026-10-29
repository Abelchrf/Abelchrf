#!/bin/bash
#
# Exercice 002 : Installation de Samba
#
# Usage : sudo ./install_samba.sh
#
# Samba permet de partager des dossiers Linux sur le réseau avec le protocole
# des partages Windows (SMB) : on y accède depuis Windows (\\serveur\partage),
# Linux ou Mac.
#   - smbd : le service qui sert les fichiers (ports 139 et 445)
#   - nmbd : le service qui annonce les noms sur le réseau local
#
#   1. Installe samba (serveur) et smbclient (client pour tester).
#   2. Garde une copie de la configuration d'origine et prépare
#      /etc/samba/conf.d/ (nos réglages, un fichier par exercice).
#   3. Active et démarre les services, affiche systemctl status smbd.

set -u

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq samba smbclient >/dev/null

[[ -f /etc/samba/smb.conf.orig ]] || cp /etc/samba/smb.conf /etc/samba/smb.conf.orig
mkdir -p /etc/samba/conf.d            # nos partages, un fichier par exercice

# Nos réglages généraux vont dans conf.d/global.conf, inclus juste sous
# [global]. auth_audit:3 : Samba note chaque connexion (qui, d'où, OK ou refus).
GLOBAL="/etc/samba/conf.d/global.conf"
grep -q "log level" "$GLOBAL" 2>/dev/null || echo "   log level = 1 auth_audit:3" >> "$GLOBAL"
grep -q "include = $GLOBAL" /etc/samba/smb.conf || sed -i "/^\[global\]/a include = $GLOBAL" /etc/samba/smb.conf

testparm -s >/dev/null 2>&1 || { testparm -s; exit 1; }   # vérifie smb.conf
systemctl enable smbd nmbd
systemctl restart smbd nmbd

echo "--- Version"
smbd --version
echo "--- systemctl status smbd"
systemctl status smbd --no-pager | head -n 5
echo "--- Ports à l'écoute"
ss -ltnp | grep smbd
