import json
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from bson import ObjectId

from quiz.models.quiz import Quiz
from quiz.models.question import QuizQuestion, QuizOption
from quiz.forms.unified_quiz_form import UnifiedQuizForm
from quiz.services.csv_import_service import CSVImportService


@staff_member_required
def unified_quiz_create_view(request):
    """
    Unified view to create quiz with questions in one page.
    Supports CSV upload to prefill questions.
    """

    csv_preview_data = None
    csv_errors = None
    has_csv_errors = False

    if request.method == "POST":
        # Debug: log incoming POST
        print("UNIFIED_QUIZ_CREATE POST DATA:", dict(request.POST))

        form = UnifiedQuizForm(request.POST, request.FILES)

        # Determine action robustly: check button name as well as hidden field
        action = request.POST.get("action", "preview")
        if "create_quiz" in request.POST:
            action = "create_quiz"

        print("UNIFIED_QUIZ_CREATE action:", action)

        # Handle CSV upload
        if "csv_file" in request.FILES and request.FILES["csv_file"]:
            csv_file = request.FILES["csv_file"]
            valid_rows, errors = CSVImportService.parse_csv(csv_file)

            if errors:
                csv_errors = errors
                has_csv_errors = True
                messages.warning(
                    request,
                    "CSV contains errors. Please review below. You can still create the quiz manually."
                )
                print("UNIFIED_QUIZ_CREATE CSV errors:", errors)
            else:
                csv_preview_data = valid_rows
                messages.success(
                    request,
                    f"CSV parsed successfully. {len(valid_rows)} question(s) ready to add."
                )
                print("UNIFIED_QUIZ_CREATE CSV valid rows count:", len(valid_rows))

        # Handle quiz creation with questions
        if action == "create_quiz":
            if not form.is_valid():
                # Debug form errors
                print("UNIFIED_QUIZ_CREATE form errors:", form.errors.as_json())
                messages.error(request, "Please fix the errors in the quiz details.")
            else:
                quiz = form.save()
                print("UNIFIED_QUIZ_CREATE quiz created with id:", quiz.id)

                # Get questions from form or CSV preview
                questions_json = request.POST.get("questions_json", "[]")
                try:
                    questions_data = json.loads(questions_json)
                except json.JSONDecodeError:
                    questions_data = []

                print("UNIFIED_QUIZ_CREATE questions_data length:", len(questions_data))

                # Create questions
                created_count = 0
                for q_data in questions_data:
                    # Djongo ArrayField expects a list of dicts, not model instances
                    options = []
                    correct_set = {opt.strip() for opt in q_data.get("correct_options", [])}

                    for text in q_data.get("options", []):
                        if text:  # Only add non-empty options
                            options.append({
                                "text": text,
                                "is_correct": text in correct_set,
                            })

                    if options and q_data.get("question_text"):
                        QuizQuestion.objects.create(
                            quiz_id=quiz.id,
                            question_text=q_data.get("question_text", ""),
                            question_type=q_data.get("question_type", QuizQuestion.SINGLE),
                            options=options,
                            explanation_correct=q_data.get("explanation_correct", ""),
                            explanation_wrong=q_data.get("explanation_wrong", ""),
                        )
                        created_count += 1

                print("UNIFIED_QUIZ_CREATE questions created:", created_count)

                if created_count > 0:
                    messages.success(
                        request,
                        f"Quiz '{quiz.title}' created with {created_count} question(s)."
                    )
                else:
                    messages.success(
                        request,
                        f"Quiz '{quiz.title}' created. You can add questions later."
                    )

                return redirect("quiz:quiz_edit", quiz_id=str(quiz.id))

        # For preview or invalid create, fall through to re-render page
    else:
        form = UnifiedQuizForm()

    return render(
        request,
        "admin/unified_quiz_create.html",
        {
            "form": form,
            "csv_preview_data": csv_preview_data,
            "csv_errors": csv_errors,
            "has_csv_errors": has_csv_errors,
            "preview_json": json.dumps(csv_preview_data) if csv_preview_data else "[]",
        }
    )

