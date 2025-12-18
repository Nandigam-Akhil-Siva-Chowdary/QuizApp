import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from quiz.models.quiz import Quiz
from quiz.models.question import QuizQuestion, QuizOption
from quiz.forms.csv_upload_form import QuizCSVUploadForm
from quiz.services.csv_import_service import CSVImportService


@staff_member_required
def quiz_csv_upload_view(request, quiz_id):
    """
    Admin view to upload quiz questions via CSV.
    Parses and validates CSV but does NOT save questions yet.
    """

    # Quiz primary key is an integer (Djongo BigAutoField)
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == "POST":
        form = QuizCSVUploadForm(request.POST, request.FILES)

        if not form.is_valid():
            messages.error(request, "Invalid CSV upload.")
        else:
            csv_file = form.cleaned_data.get("csv_file")

            # If this is the confirmation post with preview data, create questions
            action = request.POST.get("action")
            preview_json = request.POST.get("preview_json")

            if action == "create" and preview_json:
                try:
                    preview_rows = json.loads(preview_json)
                except json.JSONDecodeError:
                    messages.error(request, "Unable to read preview data. Please re-upload.")
                    return redirect("quiz:quiz_csv_upload", quiz_id=str(quiz.id))

                created = 0
                for row in preview_rows:
                    # Djongo ArrayField expects list of dicts
                    options = []
                    correct_set = {opt.strip() for opt in row.get("correct_options", [])}
                    for text in row.get("options", []):
                        if text:
                            options.append({
                                "text": text,
                                "is_correct": text in correct_set,
                            })

                    QuizQuestion.objects.create(
                        quiz_id=quiz.id,
                        question_text=row.get("question_text", ""),
                        question_type=row.get("question_type", QuizQuestion.SINGLE),
                        options=options,
                        explanation_correct=row.get("explanation_correct", ""),
                        explanation_wrong=row.get("explanation_wrong", ""),
                    )
                    created += 1

                messages.success(request, f"{created} question(s) created from CSV preview.")
                return redirect("quiz:quiz_edit", quiz_id=str(quiz.id))

            # First stage: parse CSV and show preview/errors
            valid_rows, errors = CSVImportService.parse_csv(csv_file)

            if errors:
                messages.error(
                    request,
                    "CSV contains errors. Please review below or fix manually."
                )
                return render(
                    request,
                    "admin/quiz_csv_upload.html",
                    {
                        "quiz": quiz,
                        "form": form,
                        "errors": errors,
                        "preview_data": valid_rows,
                        "has_errors": True,
                    }
                )

            # No errors → show preview and ask for confirmation to create
            return render(
                request,
                "admin/quiz_csv_upload.html",
                {
                    "quiz": quiz,
                    "form": form,
                    "preview_data": valid_rows,
                    "preview_json": json.dumps(valid_rows),
                    "has_errors": False,
                }
            )
    else:
        form = QuizCSVUploadForm()

    return render(
        request,
        "admin/quiz_csv_upload.html",
        {
            "quiz": quiz,
            "form": form,
        }
    )
