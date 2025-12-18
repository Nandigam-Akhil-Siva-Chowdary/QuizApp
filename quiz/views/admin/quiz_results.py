from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from bson import ObjectId

from quiz.models.quiz import Quiz
from quiz.models.attempt import QuizAttempt
from quiz.models.answer import QuizAnswer
from quiz.models.question import QuizQuestion


@staff_member_required
def quiz_results_view(request, quiz_id):
    """
    Admin view to see quiz attempts with scores and filters.
    """

    # Quiz uses integer primary key (BigAutoField), not ObjectId
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Get filter parameter
    filter_type = request.GET.get('filter', 'all')

    # Get all quiz questions for scoring
    total_questions = QuizQuestion.objects.filter(quiz_id=quiz.id).count()

    # Get all attempts
    attempts = QuizAttempt.objects.filter(
        quiz_id=quiz.id
    ).order_by("-created_at")

    # Calculate score for each attempt
    attempts_with_scores = []
    for attempt in attempts:
        score = calculate_attempt_score(attempt, total_questions)
        attempts_with_scores.append({
            'attempt': attempt,
            'score': score['score'],
            'total': score['total'],
            'percentage': score['percentage'],
            'correct': score['correct'],
            'wrong': score['wrong'],
            'unanswered': score['unanswered'],
        })

    # Apply filters
    if filter_type == 'top':
        # Sort by percentage descending, show only submitted attempts
        attempts_with_scores = [
            a for a in attempts_with_scores 
            if a['attempt'].status in ['submitted', 'auto_submitted']
        ]
        attempts_with_scores.sort(key=lambda x: x['percentage'], reverse=True)
    elif filter_type == 'lowest':
        # Sort by percentage ascending, show only submitted attempts
        attempts_with_scores = [
            a for a in attempts_with_scores 
            if a['attempt'].status in ['submitted', 'auto_submitted']
        ]
        attempts_with_scores.sort(key=lambda x: x['percentage'])
    elif filter_type == 'completed':
        # Show only completed attempts
        attempts_with_scores = [
            a for a in attempts_with_scores 
            if a['attempt'].status in ['submitted', 'auto_submitted']
        ]
    elif filter_type == 'active':
        # Show only active attempts
        attempts_with_scores = [
            a for a in attempts_with_scores 
            if a['attempt'].status == 'active'
        ]
    elif filter_type == 'disqualified':
        # Show only disqualified attempts
        attempts_with_scores = [
            a for a in attempts_with_scores 
            if a['attempt'].status == 'disqualified'
        ]

    return render(
        request,
        "admin/quiz_results.html",
        {
            "quiz": quiz,
            "attempts_with_scores": attempts_with_scores,
            "filter_type": filter_type,
            "total_attempts": len(attempts_with_scores),
        }
    )


def calculate_attempt_score(attempt, total_questions):
    """
    Calculate score for a quiz attempt.
    Returns dict with score details.
    """
    answers = QuizAnswer.objects.filter(attempt=attempt)
    
    correct = 0
    wrong = 0
    unanswered = 0

    for answer in answers:
        question = answer.question
        
        # Get correct options from question
        correct_options = set()
        for opt in question.options or []:
            if isinstance(opt, dict) and opt.get('is_correct'):
                correct_options.add(opt.get('text'))
        
        # Get selected options from answer
        selected_options = set(answer.selected_option_ids or [])
        
        # Check if answer is correct
        if selected_options == correct_options and len(selected_options) > 0:
            correct += 1
        elif len(selected_options) > 0:
            wrong += 1
        # If no selection, it's counted in unanswered below
    
    # Calculate unanswered questions
    answered_count = answers.count()
    unanswered = total_questions - answered_count
    
    # Calculate percentage
    percentage = (correct / total_questions * 100) if total_questions > 0 else 0
    
    return {
        'score': correct,
        'total': total_questions,
        'percentage': round(percentage, 2),
        'correct': correct,
        'wrong': wrong,
        'unanswered': unanswered,
    }
