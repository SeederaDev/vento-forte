# Ventoforte — Come attivare il feed Instagram

La sezione **"Seguici su Instagram"** in home è già pronta. Adesso mostra una
**anteprima temporanea** (6 foto del sito). Per farla diventare il **vero feed che si
aggiorna da solo** quando pubblichi su Instagram, segui questi passi (5 minuti).

Usiamo **LightWidget**: è gratuito, **senza pubblicità e senza logo**, e si aggiorna in
automatico. (Esistono alternative come SnapWidget o Elfsight, ma nella versione gratuita
aggiungono il loro logo o limiti: LightWidget è la più pulita.)

---

## 1. Crea il widget su LightWidget

1. Vai su **https://lightwidget.com** e clicca **“Create your widget”** / Registrati
   (puoi entrare con email o con Instagram).
2. Clicca **“Connect with Instagram”** e accedi con l'account **Instagram di Ventoforte**.
   Autorizza l'accesso (solo lettura delle foto pubbliche).
3. Scegli le impostazioni consigliate:
   - **Layout:** Grid (griglia)
   - **Columns:** 6 (così resta su una riga come l'anteprima)
   - **Number of photos:** 6 (o 12 se vuoi due righe)
   - **Spacing:** 14px · **Hover:** attivo · **Rounded corners:** sì
4. Clicca **“Save & get code”**: ti darà un codice simile a questo 👇

```html
<script src="https://cdn.lightwidget.com/widgets/lightwidget.js"></script>
<iframe src="//lightwidget.com/widgets/XXXXXXXXXXXXXXXX.html"
        scrolling="no" allowtransparency="true"
        class="lightwidget-widget"
        style="width:100%;border:0;overflow:hidden;"></iframe>
```

> `XXXX…` sarà un codice unico tuo. **Copia tutto.**

---

## 2. Incolla il codice nel sito

Apri **`index.html`** e cerca questo blocco (è segnalato da una cornice di `░░░`):

```html
<div class="ig__feed reveal" id="instagram-feed">

  <!-- ▼▼▼ ANTEPRIMA TEMPORANEA — sostituiscila con il widget ▼▼▼ -->
  <div class="ig__preview">
     ... (le 6 foto di anteprima) ...
  </div>
  <!-- ▲▲▲ FINE ANTEPRIMA ▲▲▲ -->

</div>
```

**Cancella tutto ciò che sta tra i due commenti** `▼▼▼` e `▲▲▲` (la `<div class="ig__preview">…</div>`)
e **incolla al suo posto** il codice copiato da LightWidget. Deve restare così:

```html
<div class="ig__feed reveal" id="instagram-feed">

  <script src="https://cdn.lightwidget.com/widgets/lightwidget.js"></script>
  <iframe src="//lightwidget.com/widgets/XXXXXXXXXXXXXXXX.html"
          scrolling="no" allowtransparency="true"
          class="lightwidget-widget"
          style="width:100%;border:0;overflow:hidden;"></iframe>

</div>
```

Salva e ricarica il file sul server. Fatto: il feed ora è reale e si aggiorna da solo. 🎉

---

## 3. Nome utente

I link puntano già al profilo reale **@ventoforteparco**
(https://www.instagram.com/ventoforteparco/): pulsante "Segui", tag nella sezione
Instagram e icone nel footer. Se un domani cambiate handle, basta dirmelo e li aggiorno.

---

## Note
- Il widget gratuito di LightWidget aggiorna le foto **ogni 24 ore**. La versione “premium”
  (10 € una tantum) aggiorna più spesso e toglie ogni limite — ma per un parco commerciale
  la versione gratuita va benissimo.
- Se un domani Instagram chiede di ricollegare l'account (capita ogni tanto per motivi di
  sicurezza), basta rifare il login su LightWidget: il codice nel sito **non cambia**.
- L'anteprima temporanea non dà fastidio: finché non incolli il widget, mostra 6 belle foto
  che linkano al profilo Instagram. Quindi la sezione è già pubblicabile anche subito.
