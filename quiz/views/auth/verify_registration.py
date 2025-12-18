from django.shortcuts import render, redirect
from django.contrib import messages

from quiz.forms.participant_form import ParticipantConfirmationForm


def verify_registration_view(request):
    """
    Confirm participant details before allowing quiz attempt.
    Shows prefilled registration data from API.
    """

    quiz_user = request.session.get("quiz_user")

    if not quiz_user:
        messages.error(request, "Session expired. Please login again.")
        return redirect("quiz:email_login")

    if request.method == "POST":
        form = ParticipantConfirmationForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            # Team lead data
            quiz_user.update({
                "roll_number": cd.get("team_lead_roll", ""),
                "team_lead_roll": cd.get("team_lead_roll", ""),
                "team_lead_same_college": cd.get("team_lead_same_college", True),
            })

            # Up to 4 teammates
            for idx in range(1, 5):
                name_key = f"teammate{idx}_name"
                roll_key = f"teammate{idx}_roll"
                same_key = f"teammate{idx}_same_college"
                college_key = f"teammate{idx}_college_name"

                quiz_user[name_key] = cd.get(name_key, "").strip()
                quiz_user[roll_key] = cd.get(roll_key, "").strip()
                quiz_user[same_key] = cd.get(same_key, True)
                quiz_user[college_key] = cd.get(college_key, "").strip()

            # Overall same_college flag: true only if all marked same_college
            all_same = True
            for idx in range(1, 5):
                name = quiz_user.get(f"teammate{idx}_name", "").strip()
                same = quiz_user.get(f"teammate{idx}_same_college", True)
                if name and not same:
                    all_same = False
                    break

            quiz_user["same_college"] = all_same
            quiz_user["confirmed_college"] = quiz_user.get("college_name", "")

            request.session["quiz_user"] = quiz_user
            request.session.modified = True

            messages.success(request, "Details confirmed.")
            return redirect("quiz:quiz_home")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        # Prefill form with API data (names come from API, rolls empty)
        initial_data = {
            "team_lead_roll": "",
            "teammate1_name": quiz_user.get("teammate1_name", "") or "",
            "teammate2_name": quiz_user.get("teammate2_name", "") or "",
            "teammate3_name": quiz_user.get("teammate3_name", "") or "",
            "teammate4_name": quiz_user.get("teammate4_name", "") or "",
            "team_lead_same_college": True,
            "teammate1_same_college": True,
            "teammate2_same_college": True,
            "teammate3_same_college": True,
            "teammate4_same_college": True,
        }
        form = ParticipantConfirmationForm(initial=initial_data)

    return render(
        request,
        "auth/verify_registration.html",
        {
            "quiz_user": quiz_user,
            "form": form,
        }
    )
