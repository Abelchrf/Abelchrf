# Séquence 01 : utilisateurs et groupes (exercices 001 à 003)

Rendu attendu dans le dépôt ETNA : `Sequence01/exercice_0xx/`.

```
Sequence01/
├── exercice_001/create_users.sh    + users.csv (à copier depuis l'intranet)
├── exercice_002/manage_groups.sh   (utilise aussi exercice_001/users.csv)
└── exercice_003/goinfre.sh
```

Tous les scripts se lancent **en root** sur la VM Debian 12, dans l'ordre :

```bash
sudo ./exercice_001/create_users.sh            # lit exercice_001/users.csv
sudo ./exercice_002/manage_groups.sh           # lit exercice_001/users.csv
sudo ./exercice_003/goinfre.sh
```

Chaque script peut être relancé sans rien casser (*idempotent*) : il ne recrée
pas ce qui existe déjà, il le met simplement en conformité.

---

## Rappels : où Linux stocke les comptes

| Fichier        | Contenu                                                     | Exemple |
|----------------|-------------------------------------------------------------|---------|
| `/etc/passwd`  | login, UID, GID principal, nom complet, home, shell          | `jdoe:x:1001:1001:John Doe:/home/jdoe:/bin/bash` |
| `/etc/shadow`  | mot de passe **haché** + dates d'expiration (lisible par root) | `jdoe:$y$j9T$...:0:0:99999:7:::` |
| `/etc/group`   | groupes et leurs membres secondaires                         | `dev:x:1005:jdoe,hdubois` |

- Chaque utilisateur a **un groupe principal** (sur Debian, `useradd` crée un
  groupe du même nom que l'utilisateur) et **des groupes secondaires**.
- Commandes de lecture utiles : `id jdoe`, `getent passwd jdoe`,
  `getent group dev`, `chage -l jdoe`.

---

## Exercice 001 : création d'utilisateurs

**Ce que fait le script, ligne par ligne du CSV :**

1. **Lire le CSV** : l'en-tête est `id,first_name,last_name,email,gender,group,last_login`.
   Le script repère les colonnes par leur nom. Piège du fichier : certaines
   lignes contiennent deux utilisateurs collés (`...,7/31/2024 5,Abeu,...`),
   le script les sépare avant de commencer. Si le CSV a une
   colonne `username`, elle sert de login ; sinon le login est
   *initiale du prénom + nom* (`John Doe` → `jdoe`), sans accents ni caractères
   spéciaux (`Seán O'Hara` → `sohara`). Deux « John Doe » donnent `jdoe` et `jdoe2`.
2. **Créer le compte** :
   ```bash
   useradd -m -d /home/jdoe -s /bin/bash -c "John Doe" jdoe
   ```
   - `-m` crée le répertoire personnel (copie de `/etc/skel`)
   - `-d` chemin du home, `-s` shell de connexion, `-c` nom complet
3. **Si le compte existe déjà**, on ne le recrée pas : `usermod -s` remet le
   bon shell, `usermod -d ... -m` déplace le home s'il a changé.
4. **Mot de passe** (uniquement pour un nouveau compte) :
   - celui du CSV s'il y a une colonne `password`, sinon
     `pwgen -s 12 1` (`-s` = vraiment aléatoire, `12` caractères, `1` mot de passe) ;
   - `passwd` demande le mot de passe deux fois, on les lui envoie sur l'entrée
     standard : `printf '%s\n%s\n' "$pw" "$pw" | passwd jdoe` ;
   - `passwd -e jdoe` le marque expiré : l'utilisateur **devra le changer à sa
     première connexion** (vérifiable avec `chage -l jdoe`) ;
   - les identifiants sont notés dans `/root/users_passwords.txt` en droits
     `600` (root seul) pour pouvoir les transmettre.

**Vérifier :** `tail /etc/passwd`, `id jdoe`, `ls -la /home`,
`sudo cat /root/users_passwords.txt`.

**Questions classiques en soutenance :**
- *Pourquoi `/etc/shadow` et pas le mot de passe dans `/etc/passwd` ?*
  `/etc/passwd` est lisible par tout le monde, `/etc/shadow` seulement par root,
  et il ne contient qu'un hash (`$y$` = yescrypt sur Debian 12).
- *Différence `useradd` / `adduser` ?* `useradd` est la commande bas niveau
  (scriptable, sans questions) ; `adduser` est un script Debian interactif.
- *Pourquoi ne pas régénérer les mots de passe à chaque lancement ?* Sinon
  relancer le script changerait le mot de passe de tout le monde.

---

## Exercice 002 : gestion des groupes

Le script lit la colonne `group` de `exercice_001/users.csv` :
`1,Thorndike,Butchers,...,Outdoors,...` → groupe `outdoors` créé, `tbutchers`
ajouté dedans. Le login est recalculé avec la même règle que l'exercice 001.
Une case peut contenir plusieurs groupes séparés par `;` (`Toys;Games`).

**Ce que fait le script :**

1. Pour chaque groupe : `getent group dev` vérifie s'il existe ; sinon
   `groupadd dev` le crée.
2. Ajoute l'utilisateur à tous ses groupes d'un coup :
   ```bash
   usermod -aG dev,web jdoe
   ```
   - `-G` donne la liste des groupes **secondaires**
   - `-a` (*append*) **ajoute** à la liste existante.
     ⚠️ Sans `-a`, `usermod -G dev jdoe` **retire** jdoe de tous ses autres groupes.

**Équivalents avec `gpasswd`** (groupe par groupe) :
`gpasswd -a jdoe dev` (ajouter), `gpasswd -d jdoe dev` (retirer),
`gpasswd -M jdoe,hdubois dev` (définir la liste complète des membres).

**Vérifier :** `id jdoe`, `getent group dev`, `groups jdoe`.

> Un utilisateur déjà connecté ne voit ses nouveaux groupes qu'après s'être
> reconnecté (ou avec `newgrp dev`).

---

## Exercice 003 : répertoires et permissions

**Rappel sur les droits** : `rwx` pour **u**ser (propriétaire), **g**roup,
**o**thers ; r=4, w=2, x=1. Sur un **répertoire** : `r` = lister le contenu,
`w` = créer/supprimer des fichiers dedans, `x` = pouvoir y entrer (`cd`).

| Chemin              | Propriétaire | Groupe   | Droits | Signification |
|---------------------|--------------|----------|--------|---------------|
| `/Goinfre`          | root         | root     | `777` `drwxrwxrwx` | tout le monde peut tout faire |
| `/Goinfre/<groupe>` | root         | `<groupe>` | `770` `drwxrwx---` | root et les membres : rwx ; les autres : rien |

**Ce que fait le script :**

```bash
mkdir -p /Goinfre && chmod 777 /Goinfre
for group in $(getent group | cut -d: -f1); do   # tous les groupes du système
    mkdir -p /Goinfre/$group
    chown root:$group /Goinfre/$group            # propriétaire : l'administrateur
    chmod 770 /Goinfre/$group                    # rwx rwx ---
done
```

- `mkdir -p` ne fait pas d'erreur si le dossier existe déjà.
- `getent group` liste **tous** les groupes (y compris les groupes système
  comme `adm`, `sudo`, `www-data`...), comme le demande le sujet. Pour ne
  garder que les groupes créés par l'admin (GID ≥ 1000) :
  `getent group | awk -F: '$3 >= 1000 && $3 < 65534 {print $1}'`.

**Tester en vrai :**

```bash
# runuser (en root) exécute une commande sous l'identité d'un autre utilisateur
runuser -u tbutchers -- touch /Goinfre/outdoors/test   # OK : tbutchers est dans outdoors
runuser -u bmattiazzo -- ls /Goinfre/outdoors        # Permission denied : elle n'y est pas
ls -l /Goinfre
```

(`su tbutchers` demanderait d'abord de changer le mot de passe, à cause du
`passwd -e` de l'exercice 001.)

**Améliorations à mentionner en soutenance** (non demandées par le sujet) :
- `chmod 1777 /Goinfre` : le *sticky bit* (comme sur `/tmp`) empêche un
  utilisateur de supprimer ou renommer les fichiers des autres.
- `chmod 2770 /Goinfre/dev` : le *setgid* sur un répertoire fait que les
  fichiers créés dedans appartiennent au groupe `dev` (et pas au groupe
  principal de leur créateur).
