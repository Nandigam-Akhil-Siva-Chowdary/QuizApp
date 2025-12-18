from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from quiz.models.quiz import Quiz
from quiz.services.quiz_service import QuizService


def quiz_instructions_view(request, quiz_id):
    """
    Show quiz instructions and rules before starting attempt.
    """

    quiz_user = request.session.get("quiz_user")
    if not quiz_user:
        messages.error(request, "Please login to continue.")
        return redirect("quiz:email_login")

    # Quiz primary key is an integer (Djongo BigAutoField)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    now = timezone.now()

    if not quiz.is_live(now):
        messages.error(request, "This quiz is not currently available.")
        return redirect("quiz:quiz_home")

    # Check attempt limit
    can_attempt = QuizService.can_attempt_quiz(
        quiz=quiz,
        team_code=quiz_user["team_code"]
    )

    if not can_attempt:
        messages.error(
            request,
            "You have already used all allowed attempts for this quiz."
        )
        return redirect("quiz:quiz_home")

    return render(
        request,
        "user/quiz_instructions.html",  # matches quiz/templates/user/quiz_instructions.html
        {
            "quiz": quiz,
            "quiz_user": quiz_user,
        }
    )
