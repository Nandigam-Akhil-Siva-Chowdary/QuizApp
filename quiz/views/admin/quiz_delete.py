from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from bson import ObjectId

from quiz.models.quiz import Quiz
from quiz.models.question import QuizQuestion
from quiz.models.attempt import QuizAttempt
from quiz.models.answer import QuizAnswer
from quiz.models.certificate import QuizCertificate


@staff_member_required
def quiz_delete_view(request, quiz_id):
    """
    Admin view to delete a quiz and all its related data.
    """

    quiz = get_object_or_404(Quiz, id=ObjectId(quiz_id))

    if request.method == "POST":
        # Delete related data first (important for MongoDB hygiene)
        QuizQuestion.objects.filter(quiz_id=quiz.id).delete()
        QuizAttempt.objects.filter(quiz_id=quiz.id).delete()
        QuizAnswer.objects.filter(
            attempt__in=QuizAttempt.objects.filter(quiz_id=quiz.id)
        ).delete()
        QuizCertificate.objects.filter(quiz_id=quiz.id).delete()

        quiz_title = quiz.title
        quiz.delete()

        messages.success(
            request,
            f"Quiz '{quiz_title}' and all related data were deleted successfully."
        )

        return redirect("quiz:admin_quiz_list")

    return render(
        request,
        "admin/quiz_delete_confirm.html",
        {
            "quiz": quiz
        }
    )
