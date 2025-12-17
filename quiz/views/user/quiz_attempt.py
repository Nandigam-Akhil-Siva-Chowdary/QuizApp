from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from bson import ObjectId

from quiz.models.quiz import Quiz
from quiz.models.attempt import QuizAttempt
from quiz.services.quiz_service import QuizService
from quiz.services.attempt_service import AttemptService


def quiz_attempt_view(request, quiz_id):
    """
    Start or resume a quiz attempt.
    """

    quiz_user = request.session.get("quiz_user")
    if not quiz_user:
        messages.error(request, "Please login to continue.")
        return redirect("quiz:email_login")

    quiz = get_object_or_404(Quiz, id=ObjectId(quiz_id))
    now = timezone.now()

    if not quiz.is_live(now):
        messages.error(request, "Quiz is not active.")
        return redirect("quiz:quiz_home")

    # Check if there's an active attempt
    attempt = QuizAttempt.objects.filter(
        quiz_id=quiz.id,
        team_code=quiz_user["team_code"],
        status=QuizAttempt.STATUS_ACTIVE
    ).first()

    # If no active attempt, create one
    if not attempt:
        if not QuizService.can_attempt_quiz(
            quiz=quiz,
            team_code=quiz_user["team_code"]
        ):
            messages.error(
                request,
                "You have already used all allowed attempts."
            )
            return redirect("quiz:quiz_home")

        attempt = QuizService.create_attempt(
            quiz=quiz,
            team_code=quiz_user["team_code"],
            team_lead_email=quiz_user["team_lead_email"],
            roll_number=quiz_user.get("roll_number", ""),
            college_name=quiz_user.get("confirmed_college", quiz_user.get("college_name", "")),
            extra_member_name=quiz_user.get("extra_member_name", ""),
            same_college=quiz_user.get("same_college", True),
        )

    # Auto-submit if time already expired
    if AttemptService.check_time_expiry(attempt, quiz):
        return redirect("quiz:quiz_submit")

    remaining_seconds = attempt.time_remaining_seconds(quiz)

    questions = QuizService.get_questions_for_attempt(attempt)

    return render(
        request,
        "quiz/user/quiz_attempt.html",
        {
            "quiz": quiz,
            "attempt": attempt,
            "questions": questions,
            "remaining_seconds": int(remaining_seconds),
        }
    )
