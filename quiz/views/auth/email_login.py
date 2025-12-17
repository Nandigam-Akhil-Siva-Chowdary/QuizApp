from django.shortcuts import render, redirect
from django.contrib import messages

from quiz.models.quiz import Quiz

# Import the SAME Participant/Event model used in NexusOfThings
# Adjust this import path if your events app is in a different location
from quiz.models.participant import Participant


def email_login_view(request):
    """
    Email-only login for quiz users.
    """

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        if not email:
            messages.error(request, "Please enter your email.")
            return redirect("quiz:email_login")

        try:
            participant = Participant.objects.get(team_lead_email=email)
        except Participant.DoesNotExist:
            messages.error(
                request,
                "Email not found. Please use the email used during registration."
            )
            return redirect("quiz:email_login")

        # Store essential identity info in session
        request.session["quiz_user"] = {
            "team_code": participant.team_code,
            "team_name": participant.team_name,
            "team_lead_email": participant.team_lead_email,
            "college_name": participant.college_name,
            "event": participant.event,
        }

        messages.success(request, "Login successful.")
        return redirect("quiz:verify_registration")

    return render(
        request,
        "auth/email_login.html",
    )
