# =========================
# QUIZ STATUS CONSTANTS
# =========================

QUIZ_STATUS_ACTIVE = "active"
QUIZ_STATUS_INACTIVE = "inactive"


# =========================
# ATTEMPT STATUS CONSTANTS
# =========================

ATTEMPT_STATUS_ACTIVE = "active"
ATTEMPT_STATUS_SUBMITTED = "submitted"
ATTEMPT_STATUS_AUTO_SUBMITTED = "auto_submitted"
ATTEMPT_STATUS_DISQUALIFIED = "disqualified"


# =========================
# QUESTION TYPES
# =========================

QUESTION_TYPE_SINGLE = "single"
QUESTION_TYPE_MULTIPLE = "multiple"

QUESTION_TYPES = (
    QUESTION_TYPE_SINGLE,
    QUESTION_TYPE_MULTIPLE,
)


# =========================
# SESSION KEYS
# =========================

SESSION_QUIZ_USER = "quiz_user"
SESSION_ACTIVE_ATTEMPT = "active_attempt"


# =========================
# CSV CONSTANTS
# =========================

CSV_REQUIRED_COLUMNS = [
    "question_text",
    "question_type",
    "option_1",
    "option_2",
    "correct_options",
]
