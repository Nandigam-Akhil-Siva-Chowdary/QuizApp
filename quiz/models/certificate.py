from django.db import models
from djongo import models as djongo_models


class QuizCertificate(models.Model):
    # MongoDB quiz reference
    quiz_id = djongo_models.ObjectIdField()
    team_code = models.CharField(max_length=50)

    # Cloudinary details
    certificate_url = models.URLField()
    cloudinary_public_id = models.CharField(max_length=255)

    sent_to_email = models.EmailField()
    sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quiz_certificates"
        indexes = [
            models.Index(fields=["quiz_id", "team_code"]),
        ]

    def __str__(self):
        return f"Certificate - {self.team_code}"
