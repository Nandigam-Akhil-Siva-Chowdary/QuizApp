from quiz.utils.constants import QUESTION_TYPES


def validate_question_payload(question_text, question_type, options, correct_options):
    """
    Validate question data before saving.
    """
    errors = []

    if not question_text:
        errors.append("Question text is required")

    if question_type not in QUESTION_TYPES:
        errors.append("Invalid question type")

    if len(options) < 2:
        errors.append("At least two options are required")

    if not correct_options:
        errors.append("At least one correct option is required")

    if question_type == "single" and len(correct_options) > 1:
        errors.append("Single choice question can have only one correct option")

    for idx in correct_options:
        if idx < 0 or idx >= len(options):
            errors.append("Correct option index out of range")

    return errors


def validate_attempt_access(quiz, attempt_count):
    """
    Validate whether user can attempt quiz.
    """
    if not quiz.is_active:
        return False, "Quiz is not active"

    if attempt_count >= quiz.max_attempts:
        return False, "Maximum attempts exceeded"

    return True, None
