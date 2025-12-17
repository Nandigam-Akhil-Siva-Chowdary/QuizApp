from quiz.services.attempt_service import AttemptService
from quiz.models.quiz import Quiz
from quiz.models.attempt import QuizAttempt


class AntiCheatService:
    """
    Central place to handle all anti-cheat signals
    coming from the frontend.
    """

    # Allowed violation types sent from frontend JS
    ALLOWED_VIOLATIONS = {
        "fullscreen_exit",
        "devtools_detected",
        "copy_attempt",
        "cut_attempt",
        "right_click",
        "keyboard_shortcut",
        "tab_switch",
    }

    @staticmethod
    def handle_violation(
        *,
        attempt: QuizAttempt,
        quiz: Quiz,
        violation_type: str
    ):
        """
        Validate and record a violation.
        """

        if violation_type not in AntiCheatService.ALLOWED_VIOLATIONS:
            # Ignore unknown / tampered inputs
            return

        # Delegate enforcement to AttemptService
        AttemptService.record_violation(
            attempt=attempt,
            quiz=quiz,
            violation_type=violation_type
        )
