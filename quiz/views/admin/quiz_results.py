from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from bson import ObjectId

from quiz.models.quiz import Quiz
from quiz.models.attempt import QuizAttempt


@staff_member_required
def quiz_results_view(request, quiz_id):
    """
    Admin view to see quiz attempts and violations.
    """

    quiz = get_object_or_404(Quiz, id=ObjectId(quiz_id))

    attempts = QuizAttempt.objects.filter(
        quiz_id=quiz.id
    ).order_by("-created_at")

    return render(
        request,
        "admin/quiz_results.html",
        {
            "quiz": quiz,
            "attempts": attempts,
        }
    )
