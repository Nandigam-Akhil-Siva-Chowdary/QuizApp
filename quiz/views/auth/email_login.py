from django.shortcuts import render, redirect
from django.contrib import messages

from quiz.services.participant_api_service import ParticipantAPIService


def email_login_view(request):
    """
    Email-only login for quiz users.
    Fetches participant data from external API.
    """

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        if not email:
            messages.error(request, "Please enter your email.")
            return redirect("quiz:email_login")

        # Fetch participant from API
        participant_data = ParticipantAPIService.fetch_participant_by_email(email)
        
        if not participant_data:
            messages.error(
                request,
                "Email not found. Please use the email used during registration."
            )
            return redirect("quiz:email_login")

        # Store essential identity info in session
        request.session["quiz_user"] = {
            "id": participant_data.get("id"),
            "team_code": participant_data.get("team_code"),
            "team_name": participant_data.get("team_name"),
            "team_lead_name": participant_data.get("team_lead_name"),
            "team_lead_email": participant_data.get("email"),
            "college_name": participant_data.get("college_name"),
            "event": participant_data.get("event"),
            "phone_number": participant_data.get("phone_number", ""),
            "teammate1_name": participant_data.get("teammate1_name", ""),
            "teammate2_name": participant_data.get("teammate2_name", ""),
            "teammate3_name": participant_data.get("teammate3_name", ""),
            "teammate4_name": participant_data.get("teammate4_name", ""),
            "registration_date": participant_data.get("registration_date"),
            "idea_description": participant_data.get("idea_description", ""),
            "idea_file_url": participant_data.get("idea_file_url", ""),
        }

        messages.success(request, "Login successful.")
        return redirect("quiz:verify_registration")

    return render(
        request,
        "auth/email_login.html",
    )
