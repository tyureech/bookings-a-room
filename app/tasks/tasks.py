import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings
from app.tasks.celery import celery_app


@celery_app.task
def send_mail(to_emails: list, subject: str, message: str):
    with smtplib.SMTP_SSL(settings.SMPT_HOST, settings.SMPT_PORT) as smtp:
        smtp.login(settings.SMPT_LOGIN, settings.SMPT_PASS)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        html = MIMEText(message, "html")
        msg.attach(html)

        smtp.sendmail(settings.SMPT_EMAIL, to_emails, msg.as_string())
