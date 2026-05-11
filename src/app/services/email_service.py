from pathlib import Path

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.settings import settings


class EmailService:
    def __init__(self):
        self.config = ConnectionConfig(
            MAIL_USERNAME=settings.email.mail_username,
            MAIL_PASSWORD=settings.email.mail_password,
            MAIL_FROM=settings.email.mail_from,
            MAIL_PORT=settings.email.mail_port,
            MAIL_SERVER=settings.email.mail_server,
            MAIL_FROM_NAME=settings.email.mail_from_name,
            MAIL_STARTTLS=settings.email.mail_starttls,
            MAIL_SSL_TLS=settings.email.mail_ssl_tls,
            USE_CREDENTIALS=settings.email.use_credentials,
            VALIDATE_CERTS=settings.email.validate_certs,
            TEMPLATE_FOLDER=Path(settings.email.template_folder),
        )
        self.mail = FastMail(self.config)

    async def send_template(
        self,
        background_tasks: BackgroundTasks,
        subject: str,
        recipients: list[str],
        template_name: str,
        template_body: dict,
    ) -> None:
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            template_body=template_body,
            subtype=MessageType.html,
        )

        background_tasks.add_task(
            self.mail.send_message,
            message,
            template_name,
        )
