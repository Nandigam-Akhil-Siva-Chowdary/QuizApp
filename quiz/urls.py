from django.urls import path

# Admin views
from quiz.views.admin.quiz_create import quiz_create_view
from quiz.views.admin.unified_quiz_create import unified_quiz_create_view
from quiz.views.admin.quiz_edit import quiz_edit_view
from quiz.views.admin.quiz_csv_upload import quiz_csv_upload_view
from quiz.views.admin.quiz_results import quiz_results_view
from quiz.views.admin.certificate_admin import certificate_review_view
from quiz.views.admin.quiz_delete import quiz_delete_view
from quiz.views.admin.admin_portal import (
    admin_login_view,
    admin_logout_view,
    admin_dashboard_view,
)

# Auth views
from quiz.views.auth.email_login import email_login_view
from quiz.views.auth.verify_registration import verify_registration_view

# User views
from quiz.views.user.quiz_home import quiz_home_view
from quiz.views.user.quiz_instructions import quiz_instructions_view
from quiz.views.user.quiz_attempt import quiz_attempt_view
from quiz.views.user.quiz_submit import quiz_submit_view
from quiz.views.user.quiz_result import quiz_result_view

# API views
from quiz.views.api.save_answer import save_answer_view
from quiz.views.api.mark_review import mark_review_view
from quiz.views.api.warn_violation import warn_violation_view
from quiz.views.api.auto_submit import auto_submit_view

app_name = "quiz"

urlpatterns = [
    # --------------------
    # AUTH
    # --------------------
    path("login/", email_login_view, name="email_login"),
    path("verify/", verify_registration_view, name="verify_registration"),

    # --------------------
    # USER
    # --------------------
    path("", quiz_home_view, name="quiz_home"),
    path("quiz/<str:quiz_id>/", quiz_instructions_view, name="quiz_instructions"),
    path("quiz/<str:quiz_id>/attempt/", quiz_attempt_view, name="quiz_attempt"),
    path("quiz/submit/", quiz_submit_view, name="quiz_submit"),
    path("quiz/result/<str:attempt_id>/", quiz_result_view, name="quiz_result"),

    # --------------------
    # ADMIN
    # --------------------
    path("quiz-admin/login/", admin_login_view, name="admin_login"),
    path("quiz-admin/logout/", admin_logout_view, name="admin_logout"),
    path("quiz-admin/", admin_dashboard_view, name="admin_dashboard"),

    path("admin/quiz/create/", unified_quiz_create_view, name="quiz_create"),
    path("admin/quiz/create-old/", quiz_create_view, name="quiz_create_old"),  # Keep old for reference
    path("admin/quiz/<str:quiz_id>/edit/", quiz_edit_view, name="quiz_edit"),
    path("admin/quiz/<str:quiz_id>/csv/", quiz_csv_upload_view, name="quiz_csv_upload"),
    path("admin/quiz/<str:quiz_id>/results/", quiz_results_view, name="quiz_results"),
    path(
        "admin/quiz/<str:quiz_id>/certificates/",
        certificate_review_view,
        name="certificate_review",
    ),
    path(
        "admin/quiz/<str:quiz_id>/delete/",
        quiz_delete_view,
        name="quiz_delete",
    ),

    # --------------------
    # API (AJAX)
    # --------------------
    path("api/save-answer/", save_answer_view, name="save_answer"),
    path("api/mark-review/", mark_review_view, name="mark_review"),
    path("api/warn-violation/", warn_violation_view, name="warn_violation"),
    path("api/auto-submit/", auto_submit_view, name="auto_submit"),
]
