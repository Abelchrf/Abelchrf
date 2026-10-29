# Séquence 02 : serveur mail (exercices 1 à 12)

Domaine : `etna.nx`, serveur `mail.etna.nx`. Lancer les scripts en root, dans l'ordre :

```bash
sudo ./exercice_001/postfix.sh
./exercice_002/telnet_smtp.sh
sudo ./exercice_003/mail_users.sh          # users.csv à placer dans exercice_003/
sudo ./exercice_004/postfix_tls.sh
sudo ./exercice_005/dovecot.sh
sudo ./exercice_006/quotas.sh
sudo ./exercice_007/sasl.sh
sudo ./exercice_008/spamassassin.sh
sudo ./exercice_009/postgrey.sh
sudo ./exercice_010/clamav.sh
sudo ./exercice_011/rspamd.sh
sudo ./exercice_012/dkim.sh
```

## Le chemin d'un mail à la fin de la séquence

```
expéditeur --SMTP port 25--> Postfix
                               ├─ Postgrey (9)    inconnu ? "réessaie plus tard"
                               ├─ ClamAV (10)     virus ? refusé
                               ├─ Rspamd (11)     note de spam, refus si énorme
                               ├─ OpenDKIM (12)   signe les mails qui sortent
                               └─ SpamAssassin (8) marque *****SPAM*****
                             ──LMTP──> Dovecot (5) ── quota (6) ──> /var/spool/mail/<user>
utilisateur <──IMAP 993── Dovecot          utilisateur ──SMTP 587 + mot de passe (7)──> Postfix
```

| Ex | Rôle | Fichiers modifiés |
|----|------|-------------------|
| 1 | Postfix, domaine etna.nx | `/etc/postfix/main.cf` |
| 2 | Dialogue SMTP à la main | — |
| 3 | Comptes mail (utilisateurs Linux) | `/etc/passwd`, `/etc/aliases`, `/root/mail_users.txt` |
| 4 | TLS (STARTTLS) | certificat `/etc/ssl/certs/mail.etna.nx.pem` |
| 5 | Dovecot IMAP + livraison LMTP | `/etc/dovecot/conf.d/99-etna.conf` |
| 6 | Quotas | `/etc/dovecot/conf.d/99-quota.conf` |
| 7 | SASL + port 587 | `/etc/dovecot/conf.d/99-sasl.conf`, `master.cf` |
| 8 | SpamAssassin | `/etc/spamassassin/local.cf`, `master.cf` |
| 9 | Postgrey | `/etc/default/postgrey` |
| 10 | ClamAV | `/etc/clamav/clamav-milter.conf` |
| 11 | Rspamd | `/etc/rspamd/local.d/` |
| 12 | DKIM | `/etc/opendkim.conf`, clés dans `/etc/opendkim/keys/` |

Journal de Postfix : `tail -f /var/log/postfix.log`
