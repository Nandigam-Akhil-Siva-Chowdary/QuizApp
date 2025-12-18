from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from quiz.models.quiz import Quiz
from quiz.models.attempt import QuizAttempt
from quiz.services.quiz_service import QuizService


def quiz_instructions_view(request, quiz_id):
    """
    Show quiz instructions and rules before starting attempt.

    NOTE:
    We do NOT hard-block users from viewing the instructions page based on
    attempts used. The hard limit is enforced when actually creating / resuming
    an attempt in `quiz_attempt_view`. Here we only show information and, if
    needed, disable the "Start Quiz" button.
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

    # Check attempt eligibility and compute remaining attempts for display only.
    can_attempt = QuizService.can_attempt_quiz(
        quiz=quiz,
        team_code=quiz_user["team_code"],
    )

    used_attempts = QuizAttempt.objects.filter(
        quiz_id=quiz.id,
        team_code=quiz_user["team_code"],
        status__in=[
            QuizAttempt.STATUS_SUBMITTED,
            QuizAttempt.STATUS_AUTO_SUBMITTED,
            QuizAttempt.STATUS_DISQUALIFIED,
        ],
    ).count()

    remaining_attempts = max(0, quiz.max_attempts - used_attempts)

    return render(
        request,
        "user/quiz_instructions.html",  # matches quiz/templates/user/quiz_instructions.html
        {
            "quiz": quiz,
            "quiz_user": quiz_user,
            "can_attempt": can_attempt,
            "used_attempts": used_attempts,
            "remaining_attempts": remaining_attempts,
        },
    )
