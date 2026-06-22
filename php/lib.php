<?php
/* Funzioni condivise per i form di Ventoforte */

/* Risposta JSON e stop */
function json_out($ok, $message, $code = 200) {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['ok' => (bool)$ok, 'message' => $message], JSON_UNESCAPED_UNICODE);
    exit;
}

/* Pulisce un campo a riga singola e rimuove tentativi di header-injection */
function clean_field($s) {
    $s = (string)($s ?? '');
    $s = str_replace(["\r", "\n", "%0a", "%0d", "%0A", "%0D"], ' ', $s);
    return trim($s);
}

/* Valida email */
function valid_email($e) {
    return (bool)filter_var($e, FILTER_VALIDATE_EMAIL);
}

/* Salva una copia locale della richiesta (backup se la mail non parte) */
function log_submission($file, array $data) {
    $dir = __DIR__ . '/_data';
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
        // protegge la cartella da accessi web diretti
        @file_put_contents($dir . '/.htaccess', "Require all denied\nDeny from all\n");
    }
    $line = date('c') . "\t" . json_encode($data, JSON_UNESCAPED_UNICODE) . PHP_EOL;
    @file_put_contents($dir . '/' . $file, $line, FILE_APPEND | LOCK_EX);
}

/* Invia una email di testo semplice con header corretti (UTF-8) */
function send_mail($to, $subject, $body, array $cfg, $replyTo = null) {
    $from     = $cfg['from'];
    $fromName = '=?UTF-8?B?' . base64_encode($cfg['from_name']) . '?=';

    $headers   = [];
    $headers[] = 'From: ' . $fromName . ' <' . $from . '>';
    if ($replyTo && valid_email($replyTo)) {
        $headers[] = 'Reply-To: ' . $replyTo;
    }
    $headers[] = 'MIME-Version: 1.0';
    $headers[] = 'Content-Type: text/plain; charset=UTF-8';
    $headers[] = 'Content-Transfer-Encoding: 8bit';
    $headers[] = 'X-Mailer: PHP/' . phpversion();

    $subjectEnc = '=?UTF-8?B?' . base64_encode($subject) . '?=';

    // -f imposta il Return-Path = migliore recapito su Plesk
    return @mail($to, $subjectEnc, $body, implode("\r\n", $headers), '-f' . $from);
}

/* Semplice limite anti-flood per IP (max N invii / minuto) */
function rate_limited($key, $max = 5, $window = 60) {
    $dir = __DIR__ . '/_data';
    if (!is_dir($dir)) @mkdir($dir, 0700, true);
    $f = $dir . '/rate_' . md5($key) . '.json';
    $now = time();
    $hits = [];
    if (is_file($f)) {
        $hits = json_decode(@file_get_contents($f), true) ?: [];
    }
    $hits = array_filter($hits, function ($t) use ($now, $window) { return $t > $now - $window; });
    if (count($hits) >= $max) return true;
    $hits[] = $now;
    @file_put_contents($f, json_encode(array_values($hits)), LOCK_EX);
    return false;
}
