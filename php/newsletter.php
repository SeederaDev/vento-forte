<?php
/* Handler iscrizione newsletter */
require __DIR__ . '/lib.php';
$cfg = require __DIR__ . '/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    json_out(false, 'Metodo non consentito.', 405);
}

// Honeypot anti-bot
if (!empty($_POST['website'])) {
    json_out(true, 'Grazie!');
}

$ip = $_SERVER['REMOTE_ADDR'] ?? 'cli';
if (rate_limited('news_' . $ip, 8, 60)) {
    json_out(false, 'Troppe richieste. Riprova tra qualche minuto.', 429);
}

$email = clean_field($_POST['email'] ?? '');
if (!valid_email($email)) {
    json_out(false, 'Inserisci un indirizzo email valido.', 422);
}

// salva l'iscritto (così hai sempre la lista, anche senza un servizio esterno)
log_submission('newsletter.log', ['email' => $email, 'ip' => $ip]);

$body  = "Nuova iscrizione alla newsletter Ventoforte\n";
$body .= "-------------------------------------------\n\n";
$body .= "Email: $email\n";
$body .= "Data : " . date('d/m/Y H:i') . "\n";

$ok = send_mail($cfg['newsletter_to'], 'Nuova iscrizione newsletter', $body, $cfg, $email);

// L'iscrizione è comunque salvata nel log: confermiamo all'utente anche se
// la mail di notifica non parte.
json_out(true, 'Iscrizione completata! Grazie, ti terremo aggiornato. 🎉');
