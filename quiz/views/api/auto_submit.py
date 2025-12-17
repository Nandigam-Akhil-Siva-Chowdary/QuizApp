from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId

from quiz.models.attempt import QuizAttempt
from quiz.models.quiz import Quiz
from quiz.services.attempt_service import AttemptService


@require_POST
@csrf_exempt
def auto_submit_view(request):
    """
    Auto-submit an active quiz attempt (time expiry or forced).
    """
    try:
        attempt_id = ObjectId(request.POST.get("attempt_id"))

        attempt = QuizAttempt.objects.get(
            id=attempt_id,
            status=QuizAttempt.STATUS_ACTIVE
        )

        quiz = Quiz.objects.get(id=attempt.quiz_id)

        AttemptService.submit_attempt(attempt, auto=True)

        return JsonResponse({"success": True})

    except QuizAttempt.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Attempt not found or already submitted"},
            status=400
        )

    except Quiz.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Quiz not found"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500
        )
