from django.contrib import admin

from quiz.models.quiz import Quiz
from quiz.models.question import QuizQuestion
from quiz.models.attempt import QuizAttempt
from quiz.models.answer import QuizAnswer
from quiz.models.certificate import QuizCertificate


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "time_limit_minutes",
        "max_attempts",
        "warnings_allowed",
        "shuffle_questions",
        "shuffle_options",
        "allow_immediate_results",
        "start_time",
        "end_time",
        "is_active",
    )
    list_filter = ("is_active", "allow_immediate_results")
    search_fields = ("title",)
    ordering = ("-created_at",)


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question_text",
        "question_type",
        "quiz_id",
        "created_at",
    )
    search_fields = ("question_text",)
    readonly_fields = ("created_at",)
    # Manage questions via custom UI/CSV, not via admin embedded options
    exclude = ("options",)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "team_code",
        "team_lead_email",
        "quiz_id",
        "attempt_number",
        "status",
        "warnings_used",
        "fullscreen_violations",
        "devtools_violations",
        "started_at",
        "ended_at",
    )
    list_filter = ("status",)
    search_fields = ("team_code", "team_lead_email")
    readonly_fields = (
        "started_at",
        "ended_at",
        "question_order",
        "option_order_map",
    )
    ordering = ("-created_at",)


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "attempt",
        "question",
        "is_marked_for_review",
        "answered_at",
    )
    readonly_fields = (
        "attempt",
        "question",
        "selected_option_ids",
        "answered_at",
    )


@admin.register(QuizCertificate)
class QuizCertificateAdmin(admin.ModelAdmin):
    list_display = (
        "team_code",
        "quiz_id",
        "sent_to_email",
        "sent_at",
    )
    search_fields = ("team_code", "sent_to_email")
    readonly_fields = (
        "certificate_url",
        "cloudinary_public_id",
        "created_at",
    )
