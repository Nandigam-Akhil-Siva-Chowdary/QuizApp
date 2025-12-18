from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from quiz.models.quiz import Quiz
from quiz.services.quiz_service import QuizService


def quiz_home_view(request):
    """
    User home page showing available quizzes.
    Only shows quizzes for the same event as the participant registration.
    """

    quiz_user = request.session.get("quiz_user")

    if not quiz_user:
        messages.error(request, "Please login to continue.")
        return redirect("quiz:email_login")

    now = timezone.now()
    user_event = quiz_user.get("event")

    # Show only active quizzes within time window, matching participant event if available
    filters = {
        "is_active": True,
        "start_time__lte": now,
        "end_time__gte": now,
    }
    if user_event:
        filters["event_name"] = user_event

    quizzes = Quiz.objects.filter(**filters).order_by("start_time")

    return render(
        request,
        "user/quiz_home.html",  # app template path: quiz/templates/user/quiz_home.html
        {
            "quiz_user": quiz_user,
            "quizzes": quizzes,
        }
    )
