import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import config
import time

class EmailSender:
    def __init__(self, email_sender: str, email_password: str, smtp_server: str) -> None:
        """
        Initializes the EmailSender object.

        Args:
            smtp_server (str): SMTP server address.
            email_sender (str): Sender's email address.
            email_password (str): Sender's email password.
        """
        self.email_sender = email_sender
        self.email_password = email_password
        self.message = MIMEMultipart()
        self.smtp_server = smtp_server
        

    def create_message(self, email_receiver: str, email_subject: str, email_body: str) -> None:
        """
        Creates an email message with the specified receiver, subject, and body.

        Args:
            email_receiver (str): Receiver's email address.
            email_subject (str): Email subject.
            email_body (str): Email body text.
        """

        self.message["From"] = self.email_sender
        self.message["To"] = email_receiver
        self.message["Subject"] = email_subject # тема

#        message_body = MIMEText(email_body, "plain")
        message_body = MIMEText(email_body, "html")
        self.message.attach(message_body)

    def attach_file(self, filename: str) -> None:
        """
        Attaches a file to the email.

        Args:
            filename (str): File path to attach.
        """
        with open(filename, "rb") as attachment:
            payload = MIMEBase("application", "octet-stream")
            payload.set_payload(attachment.read())
            encoders.encode_base64(payload)
            payload.add_header("Content-Disposition", f"attachment; filename={filename}")

            self.message.attach(payload)

    def send_email(self) -> None:
        """
        Sends the email using the configured SMTP server and sender's credentials.
        """
        with smtplib.SMTP(self.smtp_server) as server:
            server.starttls()
            server.login(self.email_sender, self.email_password)
            server.send_message(self.message)


def mails_sender(id_telegram: str, filename: str) -> None:
    email_sender = config.EMAIL_SENDER
    email_password = config.EMAIL_PASSWORD
    smtp_server = config.SMTP_SERVER
    email = EmailSender(email_sender, email_password, smtp_server)

    if id_telegram in config.USERS_ID_LIST:
        email_receiver = config.USER_MAILS_DICT[id_telegram]
        email_subject = f'Тестовое письмо {filename}'
        email_body = f'Тестовое письмо {filename}'
        email.create_message(email_receiver, email_subject, email_body)
        email.attach_file(filename)
        email.send_email()
        time.sleep(35)
