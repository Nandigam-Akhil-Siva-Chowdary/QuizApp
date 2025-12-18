import random
from django.utils import timezone

from quiz.models.quiz import Quiz
from quiz.models.question import QuizQuestion
from quiz.models.attempt import QuizAttempt


class QuizService:
    @staticmethod
    def get_quiz_or_404(quiz_id):
        """
        Helper to fetch an active quiz by integer primary key.
        """
        try:
            return Quiz.objects.get(pk=quiz_id, is_active=True)
        except Quiz.DoesNotExist:
            return None

    @staticmethod
    def is_quiz_live(quiz: Quiz) -> bool:
        now = timezone.now()
        return quiz.start_time <= now <= quiz.end_time and quiz.is_active

    @staticmethod
    def can_attempt_quiz(quiz: Quiz, team_code: str) -> bool:
        """
        Allow a new attempt only if completed attempts are below max_attempts.
        Active attempts are handled separately (resume logic), so we only count
        finished or disqualified attempts here.
        """
        used_attempts = QuizAttempt.objects.filter(
            quiz_id=quiz.id,
            team_code=team_code,
            status__in=[
                QuizAttempt.STATUS_SUBMITTED,
                QuizAttempt.STATUS_AUTO_SUBMITTED,
                QuizAttempt.STATUS_DISQUALIFIED,
            ]
        ).count()

        return used_attempts < quiz.max_attempts

    @staticmethod
    def create_attempt(
        quiz: Quiz,
        team_code: str,
        team_lead_email: str,
        roll_number: str = "",
        college_name: str = "",
        extra_member_name: str | None = None,
        same_college: bool = True,
    ):
        """
        Create a new quiz attempt with shuffled order (if enabled)
        """
        attempt_number = (
            QuizAttempt.objects.filter(
                quiz_id=quiz.id,
                team_code=team_code
            ).count() + 1
        )

        questions = list(
            QuizQuestion.objects.filter(quiz_id=quiz.id)
        )

        question_ids = [str(q.id) for q in questions]

        # Shuffle questions if enabled
        if quiz.shuffle_questions:
            random.shuffle(question_ids)

        option_order_map = {}

        for q in questions:
            # options are stored as list of dicts, not model instances
            option_ids = [opt.get("text") for opt in q.options if opt.get("text")]

            if quiz.shuffle_options:
                random.shuffle(option_ids)

            option_order_map[str(q.id)] = option_ids

        attempt = QuizAttempt.objects.create(
            quiz_id=quiz.id,
            team_code=team_code,
            team_lead_email=team_lead_email,
            roll_number=roll_number or "",
            college_name=college_name or "",
            extra_member_name=extra_member_name or "",
            same_college=same_college,
            attempt_number=attempt_number,
            question_order=question_ids,
            option_order_map=option_order_map,
        )

        return attempt

    @staticmethod
    def get_questions_for_attempt(attempt: QuizAttempt):
        """
        Return questions in the same order as stored in attempt
        """
        questions = QuizQuestion.objects.filter(
            quiz_id=attempt.quiz_id
        )

        question_map = {str(q.id): q for q in questions}

        ordered_questions = []
        for qid in attempt.question_order:
            q = question_map.get(qid)
            if not q:
                continue

            # Apply stored option order
            ordered_options = []
            option_map = {}
            for opt in q.options:
                key = opt.get("text") or str(opt.get("id"))
                if key:
                    option_map[key] = opt
            for oid in attempt.option_order_map.get(qid, []):
                opt = option_map.get(oid)
                if opt:
                    if "id" not in opt:
                        opt["id"] = oid
                    ordered_options.append(opt)

            q.options = ordered_options
            ordered_questions.append(q)

        return ordered_questions
