# Ventoforte — Guida invio email (Plesk)

Il sito è statico (HTML/CSS/JS), ma i due form — **richiesta apertura negozio** e
**iscrizione newsletter** — inviano una vera email tramite due piccoli script PHP.
Plesk esegue PHP di default, quindi non serve installare nulla.

---

## 1. Carica i file sul server

Carica **tutta la cartella** dentro `httpdocs` (la radice del dominio) mantenendo la
struttura così com'è:

```
httpdocs/
├── index.html
├── contatti.html
├── css/
├── js/
├── assets/
└── php/
    ├── config.php        ← da modificare (punto 2)
    ├── contact.php
    ├── newsletter.php
    └── lib.php
```

> La cartella `docs/` (screenshot e script di test) **non va caricata**: serve solo a noi.

---

## 2. Imposta gli indirizzi email

Apri `php/config.php` (in Plesk: **File Manager** → matita per modificare) e cambia i 4 valori:

```php
'to'            => 'info@ventoforte.it',   // dove arrivano le richieste negozio
'newsletter_to' => 'info@ventoforte.it',   // dove arrivano le iscrizioni newsletter
'from'          => 'noreply@ventoforte.it', // MITTENTE: deve essere @ventoforte.it
'from_name'     => 'Sito Ventoforte',
```

**Importante sul mittente (`from`):** deve essere un indirizzo del **tuo dominio**
`ventoforte.it`. Se metti una Gmail o un dominio diverso, le mail finiscono nello spam
o vengono rifiutate.

---

## 3. Crea le caselle in Plesk

In Plesk → **Posta** → *Crea indirizzo email*:

1. `info@ventoforte.it` — la casella dove **leggerai** le richieste.
2. `noreply@ventoforte.it` — la casella mittente (puoi anche non leggerla mai, ma deve
   esistere perché il server la riconosca come propria).

Plesk configura in automatico SPF e DKIM per il dominio: è ciò che fa arrivare le mail
nella posta in arrivo e non nello spam.

---

## 4. Prova

1. Vai su `https://ventoforte.it/contatti.html`, compila il form e invia.
   Deve comparire **“Richiesta inviata!”** e ti arriva l'email su `info@ventoforte.it`.
2. Vai in home, in fondo, e iscriviti alla newsletter: deve comparire
   **“Iscrizione completata!”**.

---

## 5. Dove finiscono i dati (backup automatico)

Oltre all'email, **ogni invio viene salvato** sul server in:

```
php/_data/contatti.log      → tutte le richieste negozio
php/_data/newsletter.log    → tutti gli indirizzi iscritti
```

Così, anche se una mail non partisse, **non perdi nessun contatto**. La cartella
`_data` è protetta dall'accesso via web.
La lista newsletter è qui: ti basta scaricare `newsletter.log` quando vuoi.

---

## 6. Se le email NON arrivano

1. **Controlla lo spam** della casella `info@ventoforte.it`.
2. In Plesk → **Posta → Impostazioni del servizio di posta**: verifica che l'invio sia
   attivo e che il dominio usi il mail server locale.
3. Verifica che `noreply@ventoforte.it` **esista** come casella (punto 3).
4. Controlla che la cartella `php/_data` sia scrivibile (permessi 755/775). Se il log si
   crea, PHP gira correttamente: il problema è solo di consegna posta.

### Opzione più robusta (SMTP)
Se il provider blocca la funzione `mail()`, si può passare all'invio via **SMTP
autenticato** (con le credenziali della casella Plesk). È una modifica di pochi minuti:
fammelo sapere e ti preparo la versione SMTP di `lib.php`.

---

## Note tecniche
- Protezione anti-spam: ogni form ha un campo nascosto “honeypot” e un limite di invii
  per IP (anti-flood). Nessun CAPTCHA fastidioso per gli utenti.
- I form funzionano in **AJAX** (niente ricaricamento pagina) ma degradano comunque a un
  normale invio POST se JavaScript è disattivato.
- Richiede PHP 7.0 o superiore (qualsiasi Plesk recente va bene).
