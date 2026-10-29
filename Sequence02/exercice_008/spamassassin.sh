#!/bin/bash
#
# Exercice 8 : Filtrage du spam avec SpamAssassin
#
# Usage : sudo ./spamassassin.sh
#
# SpamAssassin lit chaque mail entrant et lui donne une note de "spam"
# (mots suspects, liens, en-têtes bizarres...). Au-dessus de 5, c'est du spam :
# il ajoute "X-Spam-Flag: YES" et "*****SPAM*****" devant le sujet.
#
# Le chemin d'un mail qui arrive par le port 25 :
#   Postfix (smtp) -> content_filter "spamassassin" -> spamc -> spamd (analyse)
#   -> sendmail (réinjecte le mail marqué dans Postfix) -> boîte mail
#
#   1. Installe SpamAssassin (spamd = le service qui analyse, spamc = le client).
#   2. Règles locales (/etc/spamassassin/local.cf).
#   3. Ajoute le filtre dans /etc/postfix/master.cf.
#   4. Test avec GTUBE, un texte que tout anti-spam reconnaît comme spam.

set -u

DOMAIN="etna.nx"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi

# 1. Installation (sur Debian 12, spamd est un paquet à part)
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq spamassassin spamc spamd telnet >/dev/null

# 2. Configuration de SpamAssassin
cat > /etc/spamassassin/local.cf <<'CONF'
# Exercice 8
required_score      5.0               # note à partir de laquelle c'est du spam
rewrite_header      Subject *****SPAM*****
report_safe         0                 # garder le mail original (pas de pièce jointe)
use_bayes           1                 # apprentissage automatique
bayes_auto_learn    1
CONF
spamassassin --lint || exit 1           # vérifie les règles

systemctl enable spamd
systemctl restart spamd
sleep 3

# 3. Postfix : les mails reçus sur le port 25 passent par SpamAssassin
#    -f : le mail est rendu même si spamd ne répond pas (rien n'est perdu)
postconf -P "smtp/inet/content_filter=spamassassin"
postconf -M "spamassassin/unix=spamassassin unix - n n - - pipe user=debian-spamd argv=/usr/bin/spamc -f -e /usr/sbin/sendmail -oi -f \${sender} \${recipient}"
postfix check || exit 1
systemctl reload postfix
sleep 1

# 4. Test : un mail normal et un mail GTUBE envoyés à root par le port 25
send() {   # send SUJET TEXTE
    {
        sleep 1; echo "EHLO test.etna.nx"
        sleep 1; echo "MAIL FROM:<test@example.com>"
        sleep 1; echo "RCPT TO:<root@$DOMAIN>"
        sleep 1; echo "DATA"
        sleep 1; echo "Subject: $1"; echo; echo "$2"; echo "."
        sleep 1; echo "QUIT"
    } | telnet localhost 25 >/dev/null 2>&1
}
send "Mail normal" "Bonjour, ceci est un mail tout a fait normal."
send "Mail GTUBE" 'XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X'
sleep 6

echo "--- En-têtes ajoutés par SpamAssassin dans /var/spool/mail/root"
grep -E "^Subject: .*(Mail normal|Mail GTUBE)|^X-Spam-(Flag|Status)" /var/spool/mail/root | tail -n 5
echo
echo "Analyser un fichier à la main : spamc -R < message.eml"
