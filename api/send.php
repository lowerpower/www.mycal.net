<?php
declare(strict_types=1);

/**
 * send.php - minimal transactional email sender via SMTP.
 *
 * Auth:
 *   - Requires X-Mail-Secret header OR `secret` POST field matching MAIL_SEND_SECRET env var.
 *
 * Env vars required:
 *   - MAIL_SEND_SECRET   (shared secret to authorize API calls)
 *   - SMTP_HOST
 *   - SMTP_PORT          (default 587)
 *   - SMTP_USER          (mailbox user, e.g., noreply@anchorid.net)
 *   - SMTP_PASS          (mailbox password)
 *   - SMTP_FROM_EMAIL    (e.g., noreply@anchorid.net)
 *   - SMTP_FROM_NAME     (e.g., AnchorID)
 *
 * Request:
 *   POST JSON or x-www-form-urlencoded:
 *     to, subject, body
 *   Optional:
 *     reply_to, reply_to_name, is_html (true/false)
 */

header('Content-Type: application/json; charset=utf-8');

function respond(int $code, array $payload): void {
    http_response_code($code);
    echo json_encode($payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function env_required(string $key): string {
    $v = getenv($key);
    if ($v === false || trim($v) === '') {
        respond(500, ["ok" => false, "error" => "Server misconfigured: missing env " . $key]);
    }
    return $v;
}

function get_header(string $name): ?string {
    $key = 'HTTP_' . strtoupper(str_replace('-', '_', $name));
    return $_SERVER[$key] ?? null;
}

function read_input(): array {
    $ct = $_SERVER['CONTENT_TYPE'] ?? '';
    if (stripos($ct, 'application/json') !== false) {
        $raw = file_get_contents('php://input');
        $data = json_decode($raw ?: '{}', true);
        return is_array($data) ? $data : [];
    }
    return $_POST ?? [];
}

function is_valid_email(string $email): bool {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

// ---- Auth gate ----
$expectedSecret = env_required('ANCHORID_MAIL_SECRET');
$providedSecret = get_header('X-Mail-Secret') ?? ($_POST['secret'] ?? null);

$input = read_input();
if ($providedSecret === null && isset($input['secret'])) {
    $providedSecret = (string)$input['secret'];
}

if (!is_string($providedSecret) || !hash_equals($expectedSecret, $providedSecret)) {
    // Don’t reveal which part failed
    respond(401, ["ok" => false, "error" => "Unauthorized"]);
}

// ---- Validate inputs ----
$to = isset($input['to']) ? trim((string)$input['to']) : '';
$subject = isset($input['subject']) ? trim((string)$input['subject']) : '';
$body = isset($input['body']) ? (string)$input['body'] : '';

if ($to === '' || $subject === '' || $body === '') {
    respond(400, ["ok" => false, "error" => "Missing required fields: to, subject, body"]);
}
if (!is_valid_email($to)) {
    respond(400, ["ok" => false, "error" => "Invalid 'to' email"]);
}

// Optional fields
$replyTo = isset($input['reply_to']) ? trim((string)$input['reply_to']) : '';
$replyToName = isset($input['reply_to_name']) ? trim((string)$input['reply_to_name']) : '';
$isHtml = false;
if (isset($input['is_html'])) {
    $v = $input['is_html'];
    $isHtml = ($v === true || $v === 'true' || $v === 1 || $v === '1');
}

// ---- SMTP config ----
$smtpHost = env_required('SMTP_HOST');
$smtpPort = (int)(getenv('SMTP_PORT') ?: 587);
$smtpUser = env_required('SMTP_USER');
$smtpPass = env_required('SMTP_PASS');
$fromEmail = env_required('SMTP_FROM_EMAIL');
$fromName  = (string)(getenv('SMTP_FROM_NAME') ?: 'Mailer');

// ---- Send ----
$autoload = __DIR__ . '/vendor/autoload.php';
if (!file_exists($autoload)) {
    respond(500, ["ok" => false, "error" => "Missing PHPMailer dependency. Run: composer require phpmailer/phpmailer"]);
}

require $autoload;

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

$mail = new PHPMailer(true);

//$mail->SMTPDebug = 2;
//$mail->Debugoutput = function ($str, $level) {
//    error_log("SMTP[$level] $str");
//};


try {
    $mail->isSMTP();
    $mail->Host = $smtpHost;
    $mail->Port = $smtpPort;
    $mail->SMTPAuth = true;
    $mail->Username = $smtpUser;
    $mail->Password = $smtpPass;
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;

    // Safety
    $mail->CharSet = 'UTF-8';
    $mail->isHTML(false);
    $mail->XMailer = '';

    $mail->setFrom($fromEmail, $fromName);
    $mail->addAddress($to);

    if ($replyTo !== '') {
        if (!is_valid_email($replyTo)) {
            respond(400, ["ok" => false, "error" => "Invalid reply_to email"]);
        }
        $mail->addReplyTo($replyTo, $replyToName !== '' ? $replyToName : $replyTo);
    }

    $mail->Subject = $subject;

    $body = trim($body) . "\n\n-------\n" .
        "AnchorID\n" .
        "https://anchorid.net\n\n" .
        "This message was sent by a system you initiated.";

    if ($isHtml) {
        $mail->isHTML(true);
        $mail->Body = $body;
        $mail->AltBody = strip_tags($body);
    } else {
        $mail->isHTML(false);
        $mail->Body = $body;

    }

    $mail->send();

    respond(200, ["ok" => true, "message" => "Sent"]);
} catch (Exception $e) {
    // Avoid leaking sensitive details; log server-side if you want

error_log("MAIL ERROR: " . $mail->ErrorInfo);
error_log("EXCEPTION: " . $e->getMessage());


    respond(500, ["ok" => false, "error" => "Send failed"]);
}



