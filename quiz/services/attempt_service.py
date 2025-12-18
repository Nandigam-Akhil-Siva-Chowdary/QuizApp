from django.utils import timezone

from quiz.models.attempt import QuizAttempt
from quiz.models.quiz import Quiz


class AttemptService:
    @staticmethod
    def get_active_attempt(quiz_id, team_code):
        try:
            return QuizAttempt.objects.get(
                quiz_id=quiz_id,
                team_code=team_code,
                status=QuizAttempt.STATUS_ACTIVE
            )
        except QuizAttempt.DoesNotExist:
            return None

    @staticmethod
    def record_violation(attempt: QuizAttempt, quiz: Quiz, violation_type: str):
        """
        Record a violation and take action if limit exceeded.
        """

        if violation_type == "fullscreen_exit":
            attempt.fullscreen_violations += 1

        elif violation_type == "devtools_detected":
            attempt.devtools_violations += 1

        else:
            # copy, tab switch, shortcuts, etc.
            attempt.warnings_used += 1

        attempt.save()

        # Enforce limits
        # Fullscreen: after 2 warnings (warnings_allowed=2), 3rd violation exits
        # So fullscreen_violations > warnings_allowed means >= 3 violations
        if (
            attempt.warnings_used > quiz.warnings_allowed
            or attempt.fullscreen_violations > quiz.warnings_allowed  # 3rd violation when warnings_allowed=2
            or attempt.devtools_violations >= 2
        ):
            AttemptService.disqualify_attempt(attempt)

    @staticmethod
    def disqualify_attempt(attempt: QuizAttempt):
        attempt.status = QuizAttempt.STATUS_DISQUALIFIED
        attempt.ended_at = timezone.now()
        attempt.save()

    @staticmethod
    def submit_attempt(attempt: QuizAttempt, auto=False):
        if attempt.status != QuizAttempt.STATUS_ACTIVE:
            return

        attempt.status = (
            QuizAttempt.STATUS_AUTO_SUBMITTED
            if auto
            else QuizAttempt.STATUS_SUBMITTED
        )
        attempt.ended_at = timezone.now()
        attempt.save()

    @staticmethod
    def check_time_expiry(attempt: QuizAttempt, quiz: Quiz):
        if attempt.is_time_up(quiz):
            AttemptService.submit_attempt(attempt, auto=True)
            return True
        return False
