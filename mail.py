import imaplib, smtplib, email, re
from email.message import EmailMessage
from secret_manager import get_gmail_creds


INBOX_EMAIL, INBOX_PASSWORD = get_gmail_creds()

def get_code():

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(INBOX_EMAIL, INBOX_PASSWORD)
    mail.select("inbox")

    _, data = mail.search(None, '(UNSEEN FROM "office@nextbike.net")')

    # Obtener el ID del último correo
    mail_ids = data[0].split()
    latest_email_id = mail_ids[-1]

    # Obtener los datos del correo
    _, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Obtener el cuerpo del mensaje
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type in ["text/plain", "text/html"] and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
    else: body = msg.get_payload(decode=True).decode(errors="ignore")

    # Limpiar etiquetas HTML
    body_clean = re.sub(r"<[^>]+>", "", body)

    # Buscar el número dentro del texto
    match = re.search(r"use the code\s+(\d+)", body_clean, re.IGNORECASE)
    codigo = match.group(1)

    mail.store(latest_email_id, '+X-GM-LABELS', '\\Trash') # Llevar el correo a la papelera
    mail.expunge()
    mail.logout()

    return codigo

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = INBOX_EMAIL
    msg["To"] = f"{to}@sagulpa.com"
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(INBOX_EMAIL, INBOX_PASSWORD)
        server.send_message(msg)
