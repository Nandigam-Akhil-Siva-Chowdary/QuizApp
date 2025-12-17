import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId

from quiz.models.attempt import QuizAttempt
from quiz.models.quiz import Quiz
from quiz.services.anti_cheat_service import AntiCheatService


@require_POST
@csrf_exempt
def warn_violation_view(request):
    """
    Record an anti-cheat violation during an active quiz attempt.
    """
    try:
        data = json.loads(request.body)

        attempt_id = ObjectId(data.get("attempt_id"))
        violation_type = data.get("type")

        attempt = QuizAttempt.objects.get(
            id=attempt_id,
            status=QuizAttempt.STATUS_ACTIVE
        )

        quiz = Quiz.objects.get(id=attempt.quiz_id)

        AntiCheatService.handle_violation(
            attempt=attempt,
            quiz=quiz,
            violation_type=violation_type
        )

        return JsonResponse({"success": True})

    except QuizAttempt.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Invalid or inactive attempt"},
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
