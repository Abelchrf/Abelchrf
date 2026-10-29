#!/bin/bash
#
# Exercice 9 : Greylisting avec Postgrey
#
# Usage : sudo ./postgrey.sh
#
# Idée : quand un expéditeur INCONNU écrit pour la première fois, on répond
# "réessaie plus tard" (erreur temporaire 450). Un vrai serveur mail réessaie
# toujours quelques minutes après -> il passe. Beaucoup de robots spammeurs
# ne réessaient jamais -> bloqués.
# Postgrey retient chaque trio (IP du client, expéditeur, destinataire).
#
#   1. Installe Postgrey et règle le délai à 60 secondes.
#   2. Postfix lui demande son avis pour chaque destinataire
#      (check_policy_service). Les machines locales et les utilisateurs
#      connectés (SASL) ne sont pas concernés.
#   3. Test : on pose directement la question à Postgrey, comme Postfix.

set -u

DELAY=60

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# 1. Installation et réglages (/etc/default/postgrey)
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq postgrey netcat-openbsd >/dev/null
echo "POSTGREY_OPTS=\"--inet=127.0.0.1:10023 --delay=$DELAY\"" > /etc/default/postgrey
systemctl enable postgrey
systemctl restart postgrey
sleep 2

# 2. Postfix : règles appliquées à chaque destinataire, dans l'ordre
#    (la première qui répond OK ou REJECT décide)
postconf -e "smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination, check_policy_service inet:127.0.0.1:10023"
postfix check || exit 1
systemctl reload postfix

# 3. Test : la question que Postfix pose à Postgrey pour un inconnu
ask() {
    printf 'request=smtpd_access_policy\nprotocol_state=RCPT\nprotocol_name=ESMTP\nclient_address=203.0.113.66\nclient_name=robot.spam.example\nsender=promo@spam.example\nrecipient=root@etna.nx\n\n' \
        | nc -q 2 127.0.0.1 10023
}
echo "--- 1re tentative de l'inconnu"
ask
echo "--- 2e tentative tout de suite après : toujours refusé"
ask
echo
echo "Après $DELAY secondes, la même demande répond 'PREPEND X-Greylist...' : accepté."
echo "Liste des expéditeurs déjà vus : postgreyreport ou /var/lib/postgrey/"
