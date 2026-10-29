# Séquence 04 : les logs (exercices 1 à 5)

```bash
sudo ./exercice_001/explore_logs.sh [lignes]                 # 20 dernières lignes de chaque log, documentées
sudo ./exercice_002/user_events.sh [user] [début] [fin]      # défaut : root, aujourd'hui
sudo ./exercice_003/ssh_failures.sh [seuil]                  # échecs SSH + ALERTE si >= seuil (défaut 5)
sudo ./exercice_004/find_errors.sh [motif]                   # erreurs dans tout /var/log, archives .gz comprises
sudo ./exercice_005/period.sh <début> <fin> [fichiers...]    # ex : "today 08:00" "today 12:00"
```

Les dates s'écrivent comme pour `date -d` : `"2026-10-29 08:00"`, `"1 hour ago"`, `"yesterday"`.

Debian 12 n'installe plus rsyslog par défaut : sans `/var/log/syslog` ni
`/var/log/auth.log`, les scripts lisent le journal systemd (`journalctl`).
Pour avoir les fichiers texte : `sudo apt install rsyslog`.
