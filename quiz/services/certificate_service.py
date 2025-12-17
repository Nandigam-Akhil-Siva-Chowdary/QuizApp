import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.utils import timezone

from quiz.models.certificate import QuizCertificate
from quiz.services.cloudinary_service import CloudinaryService


class CertificateService:
    """
    Generates and uploads quiz certificates.
    """

    @staticmethod
    def generate_certificate(
        *,
        quiz_id,
        team_code,
        recipient_name,
        college_name,
        roll_number,
        email,
        background_url
    ):
        """
        Generate a certificate PDF and upload to Cloudinary.
        """

        buffer = io.BytesIO()

        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Load Canva background (PNG/JPG)
        background = ImageReader(background_url)
        c.drawImage(background, 0, 0, width=width, height=height)

        # Overlay text (positions can be adjusted later)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(width / 2, height / 2 + 40, recipient_name)

        c.setFont("Helvetica", 14)
        c.drawCentredString(width / 2, height / 2, college_name)

        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, height / 2 - 30, f"Roll No: {roll_number}")

        c.showPage()
        c.save()

        buffer.seek(0)

        # Upload to Cloudinary
        upload_result = CloudinaryService.upload_pdf(
            file_bytes=buffer,
            filename=f"{team_code}_certificate.pdf"
        )

        certificate = QuizCertificate.objects.create(
            quiz_id=quiz_id,
            team_code=team_code,
            certificate_url=upload_result["secure_url"],
            cloudinary_public_id=upload_result["public_id"],
            sent_to_email=email,
            sent_at=timezone.now(),
        )

        return certificate
