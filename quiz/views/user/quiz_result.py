from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from bson import ObjectId

from quiz.models.attempt import QuizAttempt
from quiz.models.quiz import Quiz
from quiz.models.answer import QuizAnswer
from quiz.models.question import QuizQuestion


def quiz_result_view(request, attempt_id):
    """
    Show quiz results to the user (if allowed).
    """

    quiz_user = request.session.get("quiz_user")
    if not quiz_user:
        messages.error(request, "Please login to continue.")
        return redirect("quiz:email_login")

    attempt = get_object_or_404(QuizAttempt, id=ObjectId(attempt_id))
    quiz = get_object_or_404(Quiz, id=attempt.quiz_id)

    # If results are not allowed immediately
    if not quiz.allow_immediate_results:
        return render(
            request,
            "quiz/user/quiz_result.html",
            {
                "quiz": quiz,
                "attempt": attempt,
                "results_available": False,
            }
        )

    # Fetch answers for this attempt
    answers = QuizAnswer.objects.filter(attempt=attempt)

    result_data = []

    for answer in answers:
        question = answer.question

        correct_option_ids = [
            str(opt.id)
            for opt in question.options
            if opt.is_correct
        ]

        is_correct = set(answer.selected_option_ids) == set(correct_option_ids)

        result_data.append({
            "question": question.question_text,
            "selected": answer.selected_option_ids,
            "correct": correct_option_ids,
            "is_correct": is_correct,
            "explanation_correct": question.explanation_correct,
            "explanation_wrong": question.explanation_wrong,
        })

    return render(
        request,
        "quiz/user/quiz_result.html",
        {
            "quiz": quiz,
            "attempt": attempt,
            "results_available": True,
            "result_data": result_data,
        }
    )
