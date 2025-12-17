import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId

from quiz.models.answer import QuizAnswer
from quiz.models.attempt import QuizAttempt
from quiz.models.question import QuizQuestion


@require_POST
@csrf_exempt
def mark_review_view(request):
    """
    Mark or unmark a question for review.
    """
    try:
        data = json.loads(request.body)

        attempt_id = ObjectId(data.get("attempt_id"))
        question_id = ObjectId(data.get("question_id"))
        is_marked_for_review = data.get("is_marked_for_review", True)

        attempt = QuizAttempt.objects.get(
            id=attempt_id,
            status=QuizAttempt.STATUS_ACTIVE,
        )

        question = QuizQuestion.objects.get(id=question_id)

        answer, _ = QuizAnswer.objects.get_or_create(
            attempt=attempt,
            question=question,
        )

        answer.is_marked_for_review = is_marked_for_review
        answer.save()

        return JsonResponse({"success": True})

    except QuizAttempt.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Invalid or inactive attempt"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500
        )
