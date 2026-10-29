#!/bin/bash
#
# Exercice 10 : Antivirus ClamAV pour les mails
#
# Usage : sudo ./clamav.sh
#
# ClamAV analyse les mails entrants et leurs pièces jointes. Un mail avec
# un virus est REFUSÉ avant d'être livré.
#   - clamd           : le moteur antivirus (garde les signatures en mémoire)
#   - freshclam       : télécharge les signatures de virus
#   - clamav-milter   : le lien entre Postfix et clamd. Un "milter" (mail
#                       filter) est un programme que Postfix consulte
#                       pendant la réception du mail.
#   1. Installe ClamAV et met à jour les signatures.
#   2. Configure clamav-milter (socket dans le dossier de Postfix, refus des virus).
#   3. Ajoute le milter à Postfix.
#   4. Test avec EICAR, un faux virus inoffensif reconnu par tous les antivirus.

set -u

DOMAIN="etna.nx"
MILTER_CONF="/etc/clamav/clamav-milter.conf"
SOCKET_DIR="/var/spool/postfix/clamav"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# set_conf FICHIER CLE VALEUR : remplace la ligne "CLE ..." ou l'ajoute
set_conf() {
    if grep -q "^$2 " "$1"; then sed -i "s|^$2 .*|$2 $3|" "$1"; else echo "$2 $3" >> "$1"; fi
}

# 1. Installation + signatures (première fois : quelques minutes)
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq clamav clamav-daemon clamav-milter telnet >/dev/null
systemctl stop clamav-freshclam
freshclam --quiet || echo "freshclam : mise à jour impossible (réseau ?), on continue"
systemctl enable clamav-freshclam clamav-daemon
systemctl start clamav-freshclam
systemctl restart clamav-daemon
echo "Attente du chargement des signatures par clamd..."
for i in $(seq 1 60); do [[ -S /var/run/clamav/clamd.ctl ]] && break; sleep 2; done

# 2. clamav-milter : socket accessible à Postfix, virus = mail refusé
mkdir -p "$SOCKET_DIR"
chown clamav:postfix "$SOCKET_DIR"
usermod -aG postfix clamav
set_conf "$MILTER_CONF" MilterSocket "$SOCKET_DIR/clamav-milter.ctl"
set_conf "$MILTER_CONF" MilterSocketGroup postfix
set_conf "$MILTER_CONF" MilterSocketMode 660
set_conf "$MILTER_CONF" OnInfected Reject
set_conf "$MILTER_CONF" RejectMsg "Virus detecte : %v"
set_conf "$MILTER_CONF" AddHeader Replace          # ajoute X-Virus-Scanned
systemctl enable clamav-milter
systemctl restart clamav-milter
sleep 2

# 3. Postfix consulte le milter (chemin relatif : Postfix tourne "enfermé"
#    dans /var/spool/postfix). Les autres milters éventuels sont gardés.
#    milter_default_action = accept : si l'antivirus est en panne, on livre quand même.
add_milter() {
    local key cur
    for key in smtpd_milters non_smtpd_milters; do
        cur=$(postconf -h "$key")
        [[ "$cur" == *"$1"* ]] || postconf -e "$key = ${cur:+$cur, }$1"
    done
}
add_milter "unix:clamav/clamav-milter.ctl"
postconf -e "milter_default_action = accept"
postfix check || exit 1
systemctl reload postfix
sleep 1

# 4. Test : mail contenant EICAR envoyé par le port 25
echo "--- Envoi d'un mail avec EICAR"
{
    sleep 1; echo "EHLO test.etna.nx"
    sleep 1; echo "MAIL FROM:<test@example.com>"
    sleep 1; echo "RCPT TO:<root@$DOMAIN>"
    sleep 1; echo "DATA"
    sleep 1; echo "Subject: Piece jointe dangereuse"; echo
    echo 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
    echo "."
    sleep 5; echo "QUIT"; sleep 1
} | telnet localhost 25 2>/dev/null | grep -E "^5[0-9]{2}|^250 2.0.0|queued"
echo "(attendu : 550 ... Virus detecte : Eicar-Signature)"
echo
echo "Scanner un fichier à la main : clamscan fichier   ou   clamdscan fichier"
