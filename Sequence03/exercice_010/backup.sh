#!/bin/bash
#
# Exercice 010 : Sauvegarde des partages avec rsync
#
# Usage : sudo ./backup.sh             -> sauvegarde maintenant + vérification
#         sudo ./backup.sh --install   -> en plus, sauvegarde automatique chaque nuit
#
# rsync copie un dossier vers un autre en ne recopiant que ce qui a changé.
# Chaque sauvegarde est un dossier daté dans /backup/samba/. Grâce à
# --link-dest, un fichier qui n'a pas changé depuis la veille n'est pas
# recopié : c'est un "lien dur" vers la copie de la veille (pas de place perdue),
# mais chaque dossier daté contient quand même TOUT.
#
#   1. rsync -a /srv/samba/ -> /backup/samba/<date>/ (+ lien "latest")
#   2. Garde les 7 dernières sauvegardes.
#   3. Vérifie l'intégrité : rsync --checksum compare le contenu de chaque
#      fichier (aucune différence = sauvegarde identique), + empreintes sha256.
#   4. --install : copie le script dans /usr/local/sbin et ajoute une tâche cron.

set -u

SRC="/srv/samba/"
DEST="/backup/samba"
KEEP=7
LOG="/var/log/samba-backup.log"

if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être lancé en root (sudo $0)." >&2
    exit 1
fi
command -v rsync >/dev/null || { apt-get update -qq; apt-get install -y -qq rsync >/dev/null; }

# 4. Installation de la sauvegarde automatique (tous les jours à 2h)
if [[ "${1:-}" == "--install" ]]; then
    install -m 755 "$0" /usr/local/sbin/samba-backup.sh
    echo "0 2 * * * root /usr/local/sbin/samba-backup.sh >> $LOG 2>&1" > /etc/cron.d/samba-backup
    echo "Sauvegarde automatique installée : /etc/cron.d/samba-backup (tous les jours à 2h)"
fi

# 1. Sauvegarde
mkdir -p "$DEST"
NOW=$(date +%Y-%m-%d_%H%M%S)
TARGET="$DEST/$NOW"
LINK=()
[[ -d "$DEST/latest" ]] && LINK=(--link-dest="$DEST/latest")
#   -a : garde droits, propriétaires, dates   -H : liens durs   -A -X : ACL et attributs
#   --delete : ce qui a été supprimé du partage n'est pas dans la nouvelle copie
#   --exclude lost+found : dossier système du disque des quotas (exercice 006)
echo "[$NOW] Sauvegarde de $SRC vers $TARGET"
rsync -aHAX --delete --exclude 'lost+found' "${LINK[@]}" --stats "$SRC" "$TARGET/" \
    | grep -E "Number of (regular )?files|transferred file size|Total file size"
ln -sfn "$TARGET" "$DEST/latest"

# 2. On ne garde que les $KEEP dernières
ls -1d "$DEST"/20*/ 2>/dev/null | head -n -"$KEEP" | xargs -r rm -rf

# 3. Vérification d'intégrité
echo "--- Vérification (rsync --checksum, aucune ligne = identique)"
diff_count=$(rsync -anc --delete --exclude 'lost+found' --itemize-changes "$SRC" "$TARGET/" | wc -l)
if [[ $diff_count -eq 0 ]]; then
    echo "OK : la sauvegarde est identique aux partages"
else
    echo "ATTENTION : $diff_count différences"
fi
( cd "$TARGET" && find . -type f -exec sha256sum {} + > "$DEST/$NOW.sha256" )
echo "Empreintes : $DEST/$NOW.sha256 (vérifier plus tard : cd $TARGET && sha256sum -c $DEST/$NOW.sha256)"
echo "--- Sauvegardes disponibles"
ls -1 "$DEST" | grep -v sha256
du -sh "$DEST"/20* 2>/dev/null | tail -n 3
