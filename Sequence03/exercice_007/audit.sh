#!/bin/bash
#
# Exercice 007 : Surveiller les accès Samba
#
# Usage : sudo ./audit.sh            -> configure puis affiche un rapport
#         sudo ./audit.sh --rapport  -> affiche seulement le rapport
#
# Le module "full_audit" de Samba écrit une ligne pour chaque action :
#   tbutchers|192.168.1.20|partage|mkdirat|ok|dossier_test
#   (qui | depuis quelle IP | quel partage | quelle action | résultat | fichier)
# Ces lignes partent dans le journal système (rsyslog), qu'on dirige vers
# /var/log/samba-audit.log. Le script les analyse ensuite (qui fait quoi).
#
#   1. Installe rsyslog (journal) et logwatch (rapports de logs).
#   2. Active full_audit dans les réglages généraux de Samba.
#   3. Range les lignes d'audit dans /var/log/samba-audit.log (+ rotation).
#   4. Génère de l'activité, puis affiche le rapport.

set -u

AUDIT_LOG="/var/log/samba-audit.log"
GLOBAL="/etc/samba/conf.d/global.conf"
PASS_FILE="/root/samba_users.txt"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

rapport() {
    [[ -s "$AUDIT_LOG" ]] || { echo "Aucune activité dans $AUDIT_LOG"; return; }
    echo "=== Actions par utilisateur"
    grep -oE "smbd_audit: [^|]+" "$AUDIT_LOG" | awk '{print $2}' | sort | uniq -c | sort -rn
    echo "=== Actions par type"
    awk -F'|' '{print $4}' "$AUDIT_LOG" | sort | uniq -c | sort -rn
    echo "=== Partages utilisés"
    awk -F'|' '{print $3}' "$AUDIT_LOG" | sort | uniq -c | sort -rn
    echo "=== Échecs"
    grep "|fail" "$AUDIT_LOG" | tail -n 5
    echo "=== 10 dernières actions"
    tail -n 10 "$AUDIT_LOG"
}

if [[ "${1:-}" == "--rapport" ]]; then rapport; exit 0; fi

# 1. Outils
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends rsyslog logwatch >/dev/null

# 2. full_audit pour tous les partages (réglage général)
sed -i '/full_audit/d' "$GLOBAL"
cat >> "$GLOBAL" <<'CONF'
   vfs objects = full_audit
   full_audit:prefix = %u|%I|%S
   full_audit:success = connect disconnect mkdirat unlinkat renameat create_file pwrite
   full_audit:failure = connect create_file unlinkat
   full_audit:facility = LOCAL5
   full_audit:priority = NOTICE
CONF
testparm -s >/dev/null 2>&1 || { testparm -s; exit 1; }

# 3. rsyslog : tout ce qui arrive sur "local5" va dans audit.log
echo "local5.*    $AUDIT_LOG
& stop" > /etc/rsyslog.d/30-samba-audit.conf
# Fichier créé à l'avance (si rsyslog tourne sous l'utilisateur "syslog", il
# doit pouvoir y écrire)
touch "$AUDIT_LOG"
chown syslog:adm "$AUDIT_LOG" 2>/dev/null || chown root:adm "$AUDIT_LOG"
chmod 640 "$AUDIT_LOG"
cat > /etc/logrotate.d/samba-audit <<EOF2
$AUDIT_LOG {
    weekly
    rotate 4
    compress
    missingok
    notifempty
}
EOF2
systemctl enable rsyslog
systemctl restart rsyslog
systemctl reload smbd
sleep 1

# 4. Un peu d'activité pour remplir le journal
if [[ -f "$PASS_FILE" ]]; then
    read -r u p < <(sed -n 1p "$PASS_FILE" | tr ';' ' ')
    echo "rapport du jour" > /tmp/audit_test.txt
    smbclient "//localhost/$u" -U "$u%$p" -c "mkdir audit_dossier; put /tmp/audit_test.txt audit_dossier/rapport.txt; rename audit_dossier/rapport.txt audit_dossier/rapport_final.txt; del audit_dossier/rapport_final.txt; rmdir audit_dossier" >/dev/null 2>&1
    smbclient "//localhost/$u" -U "$u%mauvais_mdp" -c "ls" >/dev/null 2>&1
    rm -f /tmp/audit_test.txt
    sleep 2
fi

rapport
echo
echo "Suivre en direct : tail -f $AUDIT_LOG"
echo "Rapport logwatch : logwatch --detail high --range today --output stdout"
