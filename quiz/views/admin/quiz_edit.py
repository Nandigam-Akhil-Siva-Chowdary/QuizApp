from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from bson import ObjectId

from quiz.models.quiz import Quiz
from quiz.models.question import QuizQuestion
from quiz.forms.quiz_form import QuizForm


@staff_member_required
def quiz_edit_view(request, quiz_id):
    """
    Admin view to edit quiz configuration and manage questions.
    """

    quiz = get_object_or_404(Quiz, id=ObjectId(quiz_id))

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, "Quiz updated successfully.")
            return redirect("quiz:quiz_edit", quiz_id=str(quiz.id))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = QuizForm(instance=quiz)

    questions = QuizQuestion.objects.filter(quiz_id=quiz.id)

    return render(
        request,
        "quiz/admin/quiz_edit.html",
        {
            "quiz": quiz,
            "form": form,
            "questions": questions,
        }
    )
