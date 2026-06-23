# Ventoforte — Proteggere il sito con una password

Vuoi che il sito chieda **utente e password** prima di mostrarsi (es. mentre è ancora
in costruzione)? Ecco i due modi. **Il primo è quello consigliato**: è tutto dal
pannello Plesk, non tocca file e non può rompere il sito.

---

## ✅ Metodo 1 — Dal pannello Plesk (consigliato)

Plesk ha una funzione apposita, **“Directory protette da password”**.

1. Entra in Plesk → **Siti web e domini** → seleziona **ventoforte.it**.
2. Cerca la voce **“Directory protette da password”**
   (in inglese *Password-Protected Directories*; di solito sotto **Sicurezza**,
   oppure clicca **“Mostra altro / Show More”** se non la vedi subito).
3. Clicca **“Aggiungi una directory protetta”**.
4. Nel campo **Nome directory** scrivi una sola barra: **`/`**
   (significa “tutto il sito”). Lascia il resto com'è e salva.
5. Ora apri quella directory protetta e clicca **“Aggiungi utente”**:
   scegli **nome utente** e **password** che vuoi, e salva.

Fatto. Da adesso, aprendo `ventoforte.it`, il browser chiede utente e password.

> Per **togliere** la protezione (quando vai online): stessa schermata →
> rimuovi la directory protetta `/` (o togli la spunta). Niente file da modificare.

---

## 🔧 Metodo 2 — Con i file .htaccess (alternativa)

Da usare solo se preferisci i file. Più delicato: un percorso sbagliato manda il
sito in errore 500.

Nel progetto trovi già il file **`.htaccess.esempio`** pronto. Passi:

1. **Crea il file delle password** `.htpasswd`.
   Il modo più semplice è generarlo online: cerca *“htpasswd generator”*, inserisci
   utente e password, e copia la riga che ottieni (è del tipo
   `mario:$apr1$xxxx....`). Mettila in un file di testo chiamato **`.htpasswd`**.
2. Carica `.htpasswd` nella cartella `httpdocs` del dominio (via Plesk File Manager).
3. Rinomina `.htaccess.esempio` in **`.htaccess`** e aprilo: nella riga
   `AuthUserFile` metti il **percorso assoluto** del file `.htpasswd` sul server.
   Su Plesk lo vedi in File Manager (proprietà del file), di solito:
   `/var/www/vhosts/ventoforte.it/httpdocs/.htpasswd`
4. Salva. Il sito ora chiede la password.

> Per togliere la protezione: rinomina o cancella il file `.htaccess`.

---

## Note importanti

- **Le password NON vanno su GitHub.** Il file `.htpasswd` è già escluso dal repository
  (`.gitignore`): le credenziali restano solo sul server, mai nel codice pubblico.
- La protezione Basic Auth copre **tutto** il sito, comprese le pagine e i form.
- Se ti serve solo nascondere il sito a Google (ma lasciarlo aperto a chi ha il link),
  è un'altra cosa (un `robots.txt` / meta noindex): dimmelo e te lo preparo.
- Se mi dici **quale dei due metodi** preferisci e (per il metodo 2) utente/password,
  ti lascio tutto pronto. Per sicurezza, però, la password è meglio impostarla tu
  direttamente in Plesk, così non passa da qui.
