from django.shortcuts import render, redirect
from django.contrib import messages

from quiz.forms.participant_form import ParticipantConfirmationForm


def verify_registration_view(request):
    """
    Confirm participant details before allowing quiz attempt.
    """

    quiz_user = request.session.get("quiz_user")

    if not quiz_user:
        messages.error(request, "Session expired. Please login again.")
        return redirect("quiz:email_login")

    if request.method == "POST":
        form = ParticipantConfirmationForm(request.POST)

        if form.is_valid():
            # Update session with confirmed details
            quiz_user.update({
                "roll_number": form.cleaned_data["roll_number"],
                "extra_member_name": form.cleaned_data.get("extra_member_name"),
                "same_college": form.cleaned_data.get("same_college"),
                "confirmed_college": (
                    quiz_user.get("college_name")
                    if form.cleaned_data.get("same_college")
                    else form.cleaned_data.get("college_name")
                )
            })

            request.session["quiz_user"] = quiz_user
            request.session.modified = True

            messages.success(request, "Details confirmed.")
            return redirect("quiz:quiz_home")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = ParticipantConfirmationForm()

    return render(
        request,
        "auth/verify_registration.html",
        {
            "quiz_user": quiz_user,
            "form": form,
        }
    )
