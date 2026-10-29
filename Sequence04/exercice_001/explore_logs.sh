#!/bin/bash
#
# Exercice 1 : Exploration des logs système de Debian 12
#
# Usage : sudo ./explore_logs.sh [nombre_de_lignes]     (défaut : 20)
#
# Affiche les dernières lignes des principaux logs, avec à quoi sert chacun.
# Sur Debian 12, deux systèmes coexistent :
#   - le JOURNAL de systemd (journalctl) : toujours présent, format binaire ;
#   - des fichiers texte dans /var/log, écrits par rsyslog s'il est installé
#     (Debian 12 ne l'installe plus par défaut : apt install rsyslog).
# Le script affiche donc les fichiers qui existent, et le journal sinon.
#
# Autres façons de lire un log :
#   cat fichier        : tout le fichier d'un coup
#   less fichier       : page par page (flèches, /mot pour chercher, q pour quitter)
#   tail -f fichier    : en direct (Ctrl+C pour arrêter)

N="${1:-20}"

if [[ $EUID -ne 0 ]]; then
    echo "Lancer en root (sudo $0) : beaucoup de logs ne sont lisibles que par root." >&2
    exit 1
fi

# show FICHIER "DESCRIPTION" : titre, description, puis les N dernières lignes
show() {
    echo "=================================================================="
    echo " $1"
    echo " -> $2"
    echo "=================================================================="
    if [[ -f "$1" ]]; then
        tail -n "$N" "$1"
    else
        echo "(absent sur cette machine)"
    fi
    echo
}

# --- Fichiers texte -----------------------------------------------------------
show /var/log/syslog        "Journal général : presque tous les messages des services (rsyslog)"
show /var/log/auth.log      "Authentifications : connexions SSH, sudo, su, échecs de mot de passe"
show /var/log/kern.log      "Messages du noyau Linux : matériel, disques, réseau, pilotes"
show /var/log/dpkg.log      "Paquets installés, mis à jour ou supprimés (dpkg)"
show /var/log/apt/history.log "Commandes apt lancées (install, upgrade...) et par qui"
show /var/log/boot.log      "Démarrage de la machine (services lancés au boot)"
show /var/log/alternatives.log "Changements de programmes par défaut (update-alternatives)"
show /var/log/apache2/access.log "Apache : chaque page demandée (si Apache est installé)"
show /var/log/apache2/error.log  "Apache : erreurs du serveur web"

# --- Fichiers binaires : on les lit avec une commande dédiée ------------------
echo "=================================================================="
echo " /var/log/wtmp (lu avec : last)"
echo " -> Historique des connexions et redémarrages"
echo "=================================================================="
last -n "$N" 2>/dev/null || echo "(absent)"
echo

echo "=================================================================="
echo " /var/log/btmp (lu avec : lastb)"
echo " -> Tentatives de connexion échouées"
echo "=================================================================="
lastb -n "$N" 2>/dev/null || echo "(absent)"
echo

# --- Le journal systemd -------------------------------------------------------
echo "=================================================================="
echo " Journal systemd (lu avec : journalctl)"
echo " -> Tous les messages du système, stockés dans /var/log/journal"
echo "    journalctl -u ssh : un service    -p err : erreurs    -f : en direct"
echo "=================================================================="
journalctl -n "$N" --no-pager 2>/dev/null || echo "(journal indisponible)"
