#!/bin/bash
#
# Exercice 011 : Connexion SSH avec une clé publique
#
# Usage : ./ssh_keys.sh [utilisateur@machine]
#         (par défaut : soi-même sur cette machine, localhost)
#
# Au lieu d'un mot de passe, on se connecte avec une paire de clés :
#   - clé privée  ~/.ssh/id_ed25519      : reste sur NOTRE machine, secrète
#   - clé publique ~/.ssh/id_ed25519.pub : copiée sur la machine distante,
#     dans ~/.ssh/authorized_keys ("les clés autorisées à entrer")
# À la connexion, le serveur vérifie qu'on possède la clé privée
# correspondante, sans qu'elle ne circule jamais sur le réseau.
# (C'est ce que tu as fait pour te connecter au GitLab de l'ETNA !)
#
#   1. Installe et démarre le serveur SSH (si besoin).
#   2. Génère la paire de clés (si elle n'existe pas).
#   3. Copie la clé publique sur la machine cible (ssh-copy-id).
#   4. Teste la connexion avec ssh -v (on doit voir "publickey").
#   5. Affiche les logs SSH du serveur (si c'est cette machine).

set -u

TARGET="${1:-$(whoami)@localhost}"
KEY="$HOME/.ssh/id_ed25519"

# 1. Serveur SSH
if ! command -v sshd >/dev/null && [[ ! -x /usr/sbin/sshd ]]; then
    sudo apt-get update -qq && sudo apt-get install -y -qq openssh-server >/dev/null
fi
sudo systemctl enable ssh >/dev/null 2>&1
sudo systemctl start ssh

# 2. Paire de clés (-N "" : sans passphrase, pour l'automatisation)
mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"
if [[ ! -f "$KEY" ]]; then
    ssh-keygen -t ed25519 -N "" -C "$(whoami)@$(hostname)" -f "$KEY"
fi
echo "Clé publique : $(cat "$KEY.pub")"

# 3. Copie de la clé publique
#    Pour soi-même sur localhost : ajout direct dans authorized_keys.
#    Sinon : ssh-copy-id (demande UNE fois le mot de passe de la machine distante).
if [[ "$TARGET" == "$(whoami)@localhost" ]]; then
    touch "$HOME/.ssh/authorized_keys"
    grep -qF "$(cat "$KEY.pub")" "$HOME/.ssh/authorized_keys" || cat "$KEY.pub" >> "$HOME/.ssh/authorized_keys"
    chmod 600 "$HOME/.ssh/authorized_keys"
    ssh-keyscan -t ed25519 localhost 2>/dev/null >> "$HOME/.ssh/known_hosts"
else
    ssh-copy-id -i "$KEY.pub" "$TARGET" || exit 1
fi

# 4. Test : BatchMode = interdiction de demander un mot de passe
#    -> si ça marche, c'est forcément la clé qui a été utilisée
echo "--- ssh -v $TARGET (extraits)"
ssh -v -o BatchMode=yes -i "$KEY" "$TARGET" 'echo "Connecté sur $(hostname) en tant que $(whoami)"' 2>&1 \
    | grep -E "Connecté|Offering public key|Server accepts key|Authenticated to|Authentication succeeded"

# 5. Logs du serveur SSH
echo "--- Logs SSH (côté serveur)"
if [[ -f /var/log/auth.log ]]; then
    sudo grep -E 'sshd\[[0-9]+\]: Accepted publickey' /var/log/auth.log | tail -n 3
else
    sudo journalctl -u ssh --no-pager -n 50 2>/dev/null | grep "Accepted publickey" | tail -n 3
fi
