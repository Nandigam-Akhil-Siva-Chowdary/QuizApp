from django.db import models
from djongo import models as djongo_models

from quiz.models.attempt import QuizAttempt
from quiz.models.question import QuizQuestion


class QuizAnswer(models.Model):
    # Relations to attempt and question
    attempt = djongo_models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question = djongo_models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)

    # For single choice → list with 1 item
    # For multiple choice → list with many items
    selected_option_ids = models.JSONField(default=list)

    is_marked_for_review = models.BooleanField(default=False)

    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "quiz_answers"
        indexes = [
            models.Index(fields=["attempt", "question"]),
        ]

    def __str__(self):
        return f"Answer for {self.question_id}"
