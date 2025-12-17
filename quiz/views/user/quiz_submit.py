from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from bson import ObjectId

from quiz.models.attempt import QuizAttempt
from quiz.models.quiz import Quiz
from quiz.services.attempt_service import AttemptService


def quiz_submit_view(request):
    """
    Final submission of a quiz attempt (manual or auto).
    """

    attempt_id = request.POST.get("attempt_id") or request.GET.get("attempt_id")
    if not attempt_id:
        messages.error(request, "Invalid submission.")
        return redirect("quiz:quiz_home")

    attempt = get_object_or_404(QuizAttempt, id=ObjectId(attempt_id))
    quiz = get_object_or_404(Quiz, id=attempt.quiz_id)

    if attempt.status != QuizAttempt.STATUS_ACTIVE:
        # Already submitted or disqualified
        return redirect("quiz:quiz_result", attempt_id=str(attempt.id))

    AttemptService.submit_attempt(attempt, auto=False)

    messages.success(request, "Quiz submitted successfully.")

    return redirect("quiz:quiz_result", attempt_id=str(attempt.id))
