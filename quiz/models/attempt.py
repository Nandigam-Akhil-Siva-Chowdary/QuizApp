from django.db import models
from django.utils import timezone
from djongo import models as djongo_models


class QuizAttempt(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_SUBMITTED = "submitted"
    STATUS_AUTO_SUBMITTED = "auto_submitted"
    STATUS_DISQUALIFIED = "disqualified"

    STATUS_CHOICES = (
        (STATUS_ACTIVE, "Active"),
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_AUTO_SUBMITTED, "Auto Submitted"),
        (STATUS_DISQUALIFIED, "Disqualified"),
    )

    # MongoDB quiz reference
    quiz_id = djongo_models.ObjectIdField()
    team_code = models.CharField(max_length=50)
    team_lead_email = models.EmailField()
    roll_number = models.CharField(max_length=100, blank=True)
    college_name = models.CharField(max_length=255, blank=True)
    extra_member_name = models.CharField(max_length=255, blank=True)
    same_college = models.BooleanField(default=True)

    attempt_number = models.PositiveIntegerField(default=1)

    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )

    # Anti-cheat tracking
    warnings_used = models.PositiveIntegerField(default=0)
    fullscreen_violations = models.PositiveIntegerField(default=0)
    devtools_violations = models.PositiveIntegerField(default=0)

    # Order persistence (critical for fairness)
    question_order = models.JSONField(default=list)
    option_order_map = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quiz_attempts"
        indexes = [
            models.Index(fields=["quiz_id", "team_code"]),
        ]

    def __str__(self):
        return f"{self.team_code} - Attempt {self.attempt_number}"

    def time_remaining_seconds(self, quiz):
        """
        Calculate remaining time based on quiz limit.
        """
        elapsed = (timezone.now() - self.started_at).total_seconds()
        return max(0, (quiz.time_limit_minutes * 60) - elapsed)

    def is_time_up(self, quiz):
        return self.time_remaining_seconds(quiz) <= 0
