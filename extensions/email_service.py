from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class EmailService:
    @staticmethod
    def send_email(subject: str, to: list[str], template_name: str, context: dict):
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            to,
            html_message=html_message,
        )
