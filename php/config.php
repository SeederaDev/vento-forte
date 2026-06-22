<?php
/* =====================================================================
   CONFIGURAZIONE EMAIL — Ventoforte
   Modifica SOLO i valori qui sotto, poi salva.
   ===================================================================== */

return [

    // Indirizzo che RICEVE le richieste dal form "Apri il tuo negozio".
    'to'             => 'info@ventoforte.it',

    // Indirizzo che RICEVE le iscrizioni alla newsletter
    // (può essere lo stesso di 'to').
    'newsletter_to'  => 'info@ventoforte.it',

    // MITTENTE dei messaggi.
    // IMPORTANTE: deve essere un indirizzo del TUO dominio ventoforte.it
    // (creane uno in Plesk → Posta, es. noreply@ventoforte.it).
    // Se metti un indirizzo di un altro dominio, le mail finiranno nello spam
    // o verranno rifiutate.
    'from'           => 'noreply@ventoforte.it',
    'from_name'      => 'Sito Ventoforte',

];
