from django.core.mail import EmailMessage
from django.conf import settings


class EmailService:
    """
    Handles all outgoing quiz-related emails.
    """

    @staticmethod
    def send_certificate_email(
        *,
        to_email,
        subject,
        body,
        attachment_url=None
    ):
        """
        Send a certificate email.
        """

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )

        # If certificate URL is provided, include it in body
        if attachment_url:
            email.body += f"\n\nDownload Certificate:\n{attachment_url}"

        email.send(fail_silently=False)

    @staticmethod
    def send_bulk_certificates(
        *,
        emails_data
    ):
        """
        Send certificates to multiple team leaders.

        emails_data = [
            {
                "email": "...",
                "subject": "...",
                "body": "...",
                "certificate_url": "..."
            }
        ]
        """

        for data in emails_data:
            EmailService.send_certificate_email(
                to_email=data["email"],
                subject=data["subject"],
                body=data["body"],
                attachment_url=data.get("certificate_url")
            )
