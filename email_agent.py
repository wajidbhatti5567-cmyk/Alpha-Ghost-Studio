import imaplib
import email
import smtplib
import os
import logging
from email.message import EmailMessage

# Setup logging for production tracking
logging.basicConfig(level=logging.INFO, filename='studio_log.log')

class EmailAgent:
    def __init__(self):
        # Automatically fetches secrets from your Environment/GitHub Secrets
        self.user = os.getenv("STUDIO_EMAIL")
        self.password = os.getenv("STUDIO_PASSWORD")
        self.imap_server = "imap.gmail.com"
        self.smtp_server = "smtp.gmail.com"

    def get_latest_command(self):
        """Connects to Gmail and fetches the latest unread command."""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.user, self.password)
            mail.select("inbox")
            
            _, data = mail.search(None, 'UNSEEN')
            if not data[0]:
                return None
            
            latest_id = data[0].split()[-1]
            _, msg_data = mail.fetch(latest_id, '(RFC822)')
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"]
                    body = self._extract_body(msg)
                    return {"title": subject, "body": body}
        except Exception as e:
            logging.error(f"Failed to fetch email: {e}")
        return None

    def _extract_body(self, msg):
        """Helper to extract text from email multi-part."""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return msg.get_payload(decode=True).decode()

    def send_email_update(self, subject, content):
        """Sends production status updates back to the user."""
        try:
            msg = EmailMessage()
            msg.set_content(content)
            msg["Subject"] = f"Alpha Ghost Studio: {subject}"
            msg["From"] = self.user
            msg["To"] = self.user
            
            with smtplib.SMTP_SSL(self.smtp_server, 465) as smtp:
                smtp.login(self.user, self.password)
                smtp.send_message(msg)
            logging.info(f"Update sent: {subject}")
        except Exception as e:
            logging.error(f"Failed to send update: {e}")
