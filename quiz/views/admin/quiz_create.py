from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from quiz.forms.quiz_form import QuizForm


@staff_member_required
def quiz_create_view(request):
    """
    Admin view to create a quiz (rules & configuration only).
    Questions will be added later manually or via CSV.
    """

    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            messages.success(
                request,
                f"Quiz '{quiz.title}' created successfully. You can now add questions."
            )
            return redirect("quiz:quiz_edit", quiz_id=str(quiz.id))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = QuizForm()

    return render(
        request,
        "quiz/admin/quiz_create.html",
        {
            "form": form
        }
    )
