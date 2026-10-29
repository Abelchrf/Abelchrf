#!/bin/bash
#
# Exercice 2 : Envoyer un mail "à la main" en SMTP via telnet
#
# Usage : ./telnet_smtp.sh [serveur] [port]     (par défaut : localhost 25)
#
# SMTP est un protocole texte : on parle au serveur ligne par ligne, et il
# répond par un code (220, 250, 354...). La séquence à taper à la main :
#
#   telnet localhost 25
#   <- 220 mail.etna.nx ESMTP Postfix          le serveur dit bonjour
#   EHLO skynet.etna.nx                        on se présente
#   <- 250-mail.etna.nx ...                    il liste ce qu'il sait faire
#   MAIL FROM:<t-800@skynet.etna.nx>           l'expéditeur (l'enveloppe)
#   <- 250 2.1.0 Ok
#   RCPT TO:<root@etna.nx>                     le destinataire
#   <- 250 2.1.5 Ok
#   DATA                                       on va écrire le message
#   <- 354 End data with <CR><LF>.<CR><LF>
#   Subject: ...                               en-têtes, ligne vide, texte
#   .                                          un point seul = fin du message
#   <- 250 2.0.0 Ok: queued as ABC123
#   QUIT
#   <- 221 2.0.0 Bye
#
# Le script fait la même chose : il envoie chaque ligne à telnet, avec un
# sleep entre chaque pour laisser le serveur répondre.

SERVER="${1:-localhost}"
PORT="${2:-25}"

command -v telnet >/dev/null || { sudo apt-get install -y -qq telnet >/dev/null; }

{
    sleep 1; echo "EHLO skynet.etna.nx"
    sleep 1; echo "MAIL FROM:<t-800@skynet.etna.nx>"
    sleep 1; echo "RCPT TO:<root@etna.nx>"
    sleep 1; echo "DATA"
    sleep 1
    echo "From: T-800 <t-800@skynet.etna.nx>"
    echo "To: Sarah Connor <root@etna.nx>"
    echo "Subject: I'll be back (en SMTP, a la main)"
    echo ""
    echo "Bonjour Sarah,"
    echo ""
    echo "Ce message a ete tape ligne par ligne via telnet."
    echo "Le S de SMTP veut bien dire Simple : 5 commandes et c'est envoye."
    echo ""
    echo "Hasta la vista, baby."
    echo "-- Cyberdyne Systems, modele 101"
    echo "."
    sleep 1; echo "QUIT"
    sleep 1
} | telnet "$SERVER" "$PORT"

echo
echo "Vérifier la réception : sudo tail -n 20 /var/spool/mail/root"
