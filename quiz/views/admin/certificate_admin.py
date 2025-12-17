from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from bson import ObjectId

from quiz.models.quiz import Quiz
from quiz.models.attempt import QuizAttempt
from quiz.models.certificate import QuizCertificate
from quiz.services.certificate_service import CertificateService
from quiz.services.email_service import EmailService


@staff_member_required
def certificate_review_view(request, quiz_id):
    """
    Admin view to review and send certificates.
    Certificates are sent ONLY to team leader email.
    """

    quiz = get_object_or_404(Quiz, id=ObjectId(quiz_id))

    # Only submitted (not disqualified) attempts get certificates
    eligible_attempts = QuizAttempt.objects.filter(
        quiz_id=quiz.id,
        status__in=[
            QuizAttempt.STATUS_SUBMITTED,
            QuizAttempt.STATUS_AUTO_SUBMITTED
        ]
    )

    existing_certificates = {
        cert.team_code: cert
        for cert in QuizCertificate.objects.filter(quiz_id=quiz.id)
    }

    if request.method == "POST":
        selected_teams = set(request.POST.getlist("team_codes"))
        background_url = request.POST.get("background_url", "").strip()
        action = request.POST.get("action")

        selected_attempts = [
            att for att in eligible_attempts if att.team_code in selected_teams
        ]

        if not selected_attempts:
            messages.error(request, "No teams selected.")
            return redirect("quiz:certificate_review", quiz_id=str(quiz.id))

        if action == "review":
            # Just show the selected emails/teams for confirmation
            return render(
                request,
                "quiz/admin/certificate_review.html",
                {
                    "quiz": quiz,
                    "eligible_attempts": eligible_attempts,
                    "existing_certificates": existing_certificates,
                    "selected_attempts": selected_attempts,
                    "background_url": background_url,
                    "review_selected": True,
                },
            )

        # Default / send path
        if not background_url:
            messages.error(request, "Please provide the Canva background URL.")
            return redirect("quiz:certificate_review", quiz_id=str(quiz.id))

        sent_count = 0

        for attempt in selected_attempts:
            # Avoid duplicate certificate generation
            if attempt.team_code in existing_certificates:
                continue

            certificate = CertificateService.generate_certificate(
                quiz_id=quiz.id,
                team_code=attempt.team_code,
                recipient_name=attempt.team_code,
                college_name=attempt.college_name,
                roll_number=attempt.roll_number,
                email=attempt.team_lead_email,
                background_url=background_url,
            )

            EmailService.send_certificate_email(
                to_email=attempt.team_lead_email,
                subject=f"Certificate for {quiz.title}",
                body="Congratulations! Please find your certificate below.",
                attachment_url=certificate.certificate_url,
            )

            sent_count += 1

        messages.success(
            request,
            f"{sent_count} certificate(s) sent successfully."
        )

        return redirect("quiz:certificate_review", quiz_id=str(quiz.id))

    return render(
        request,
        "quiz/admin/certificate_review.html",
        {
            "quiz": quiz,
            "eligible_attempts": eligible_attempts,
            "existing_certificates": existing_certificates,
        }
    )
