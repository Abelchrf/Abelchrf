# Séquence 03 : Samba et SSH (exercices 001 à 012)

Mettre `users.csv` dans `exercice_001/`, puis lancer dans l'ordre :

```bash
sudo ./exercice_001/create_users.sh     # utilisateurs + /root/samba_users.txt
sudo ./exercice_002/install_samba.sh    # Samba + logs de connexion
sudo ./exercice_003/shared_dir.sh       # [partage] pour 3 utilisateurs
sudo ./exercice_004/homes.sh            # [homes] : un partage perso par utilisateur
sudo ./exercice_005/group_shares.sh     # un partage par groupe (colonne group)
sudo ./exercice_006/quotas.sh           # [quota] : 5M / 10M par utilisateur
sudo ./exercice_007/audit.sh            # full_audit -> /var/log/samba-audit.log
sudo ./exercice_008/secure.sh           # pas d'anonyme, SMB2+, chiffrement, mots de passe
sudo ./exercice_009/readonly.sh         # [lecture] : lecture seule sauf 1 rédacteur
sudo ./exercice_010/backup.sh --install # rsync -> /backup/samba/<date> + cron
./exercice_011/ssh_keys.sh [user@machine]     # clé SSH (défaut : localhost)
./exercice_012/scp_transfer.sh [user@machine] # transfert SCP + vérification
```

Configuration Samba : `/etc/samba/smb.conf` inclut nos fichiers de
`/etc/samba/conf.d/` (un par exercice). Vérifier : `testparm -s`.
Mots de passe (Linux et Samba) : `/root/samba_users.txt`.
