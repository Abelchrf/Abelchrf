#!/bin/bash
#
# Exercice 012 : Copier des fichiers avec SCP
#
# Usage : ./scp_transfer.sh [utilisateur@machine]
#         (par défaut : soi-même sur localhost ; lancer l'exercice 011 avant)
#
# scp = "secure copy" : copie des fichiers à travers SSH (chiffré), avec la
# même clé que l'exercice 011, donc sans mot de passe.
#   scp fichier  user@machine:/dossier/   -> envoyer
#   scp user@machine:/dossier/fichier .   -> récupérer
#   scp -r dossier user@machine:/dossier/ -> un dossier entier
#
#   1. Prépare un dossier de test (3 fichiers).
#   2. L'envoie sur la machine distante (scp -r).
#   3. Vérifie à distance : ls -l, et compare les empreintes sha256
#      (identiques = fichiers intacts).
#   4. Récupère un fichier dans l'autre sens.
#   5. Affiche les logs SSH (chaque scp = une connexion).

set -u

TARGET="${1:-$(whoami)@localhost}"
KEY="$HOME/.ssh/id_ed25519"
SSH_OPTS=(-o BatchMode=yes -i "$KEY")
STAMP=$(date +%Y%m%d_%H%M%S)
LOCAL_DIR="/tmp/scp_envoi_$STAMP"
REMOTE_DIR="/tmp/scp_recu_$STAMP"

[[ -f "$KEY" ]] || { echo "Pas de clé SSH : lancer d'abord l'exercice 011." >&2; exit 1; }

# 1. Fichiers de test
mkdir -p "$LOCAL_DIR"
echo "Rapport de la séquence 03" > "$LOCAL_DIR/rapport.txt"
date > "$LOCAL_DIR/date.txt"
head -c 1M /dev/urandom > "$LOCAL_DIR/donnees.bin"

# 2. Envoi (-r : récursif, -p : garde les dates et les droits)
echo "--- Envoi de $LOCAL_DIR vers $TARGET:$REMOTE_DIR"
scp "${SSH_OPTS[@]}" -rp "$LOCAL_DIR" "$TARGET:$REMOTE_DIR" || exit 1

# 3. Vérifications à distance
echo "--- ls -l sur la machine distante"
ssh "${SSH_OPTS[@]}" "$TARGET" "ls -l $REMOTE_DIR"
local_sum=$(cd "$LOCAL_DIR" && sha256sum * | sort)
remote_sum=$(ssh "${SSH_OPTS[@]}" "$TARGET" "cd $REMOTE_DIR && sha256sum * | sort")
if [[ "$local_sum" == "$remote_sum" ]]; then
    echo "OK : les 3 fichiers sont identiques (sha256)"
else
    echo "ERREUR : les fichiers diffèrent"
fi

# 4. Récupération dans l'autre sens
mkdir -p "$HOME/scp_retour"
scp "${SSH_OPTS[@]}" -p "$TARGET:$REMOTE_DIR/rapport.txt" "$HOME/scp_retour/rapport_$STAMP.txt"
echo "--- Fichier récupéré"
ls -l "$HOME/scp_retour/rapport_$STAMP.txt"

# 5. Logs
echo "--- Logs SSH (côté serveur, si c'est cette machine)"
if [[ -f /var/log/auth.log ]]; then
    sudo grep -E 'sshd\[[0-9]+\]: Accepted publickey' /var/log/auth.log | tail -n 3
else
    sudo journalctl -u ssh --no-pager -n 50 2>/dev/null | grep "Accepted publickey" | tail -n 3
fi
rm -rf "$LOCAL_DIR"
