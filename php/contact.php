<?php
/* Handler form "Apri il tuo negozio nel parco" */
require __DIR__ . '/lib.php';
$cfg = require __DIR__ . '/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    json_out(false, 'Metodo non consentito.', 405);
}

// Honeypot: i bot compilano il campo nascosto "website" → li accettiamo in silenzio
if (!empty($_POST['website'])) {
    json_out(true, 'Grazie!');
}

$ip = $_SERVER['REMOTE_ADDR'] ?? 'cli';
if (rate_limited('contact_' . $ip, 5, 60)) {
    json_out(false, 'Troppe richieste. Riprova tra qualche minuto.', 429);
}

$nome     = clean_field($_POST['nome'] ?? '');
$azienda  = clean_field($_POST['azienda'] ?? '');
$email    = clean_field($_POST['email'] ?? '');
$telefono = clean_field($_POST['telefono'] ?? '');
$messaggio = trim((string)($_POST['messaggio'] ?? ''));
// oggetto opzionale: distingue le richieste (es. "Pubblicità LED Wall").
// Se assente, vale la richiesta apertura attività.
$oggetto  = clean_field($_POST['oggetto'] ?? '');

if ($nome === '' || !valid_email($email)) {
    json_out(false, 'Controlla nome ed email e riprova.', 422);
}

$titolo = $oggetto !== '' ? $oggetto : "Richiesta per aprire un'attività nel Parco Ventoforte";

$body  = "Nuova richiesta: $titolo\n";
$body .= "------------------------------------------------------------\n\n";
$body .= "Nome e cognome : $nome\n";
$body .= "Insegna/Azienda: " . ($azienda !== '' ? $azienda : '-') . "\n";
$body .= "Email          : $email\n";
$body .= "Telefono       : " . ($telefono !== '' ? $telefono : '-') . "\n\n";
$body .= "Messaggio:\n" . ($messaggio !== '' ? $messaggio : '-') . "\n\n";
$body .= "------------------------------------------------------------\n";
$body .= "Inviato da ventoforte.it il " . date('d/m/Y H:i') . " (IP: $ip)\n";

log_submission('contatti.log', compact('oggetto', 'nome', 'azienda', 'email', 'telefono', 'messaggio'));

$subject = ($oggetto !== '' ? $oggetto : 'Richiesta apertura attività') . ' — ' . $nome;
$ok = send_mail($cfg['to'], $subject, $body, $cfg, $email);

if ($ok) {
    json_out(true, 'Richiesta inviata! Ti ricontatteremo al più presto. Grazie.');
} else {
    json_out(false, 'Invio non riuscito. Scrivici a ' . $cfg['to'] . ' o riprova più tardi.', 500);
}
