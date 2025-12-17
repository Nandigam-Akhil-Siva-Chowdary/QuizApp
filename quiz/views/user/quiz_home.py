from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from quiz.models.quiz import Quiz
from quiz.services.quiz_service import QuizService


def quiz_home_view(request):
    """
    User home page showing available quizzes.
    """

    quiz_user = request.session.get("quiz_user")

    if not quiz_user:
        messages.error(request, "Please login to continue.")
        return redirect("quiz:email_login")

    now = timezone.now()

    # Show only active quizzes within time window
    quizzes = Quiz.objects.filter(
        is_active=True,
        start_time__lte=now,
        end_time__gte=now
    ).order_by("start_time")

    return render(
        request,
        "quiz/user/quiz_home.html",
        {
            "quiz_user": quiz_user,
            "quizzes": quizzes,
        }
    )
