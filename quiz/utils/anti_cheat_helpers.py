# =========================
# ANTI-CHEAT CONSTANTS
# =========================

VIOLATION_FULLSCREEN_EXIT = "fullscreen_exit"
VIOLATION_TAB_SWITCH = "tab_switch"
VIOLATION_COPY = "copy_attempt"
VIOLATION_DEVTOOLS = "devtools_open"

ALL_VIOLATIONS = {
    VIOLATION_FULLSCREEN_EXIT,
    VIOLATION_TAB_SWITCH,
    VIOLATION_COPY,
    VIOLATION_DEVTOOLS,
}

# Violations that count towards warnings
WARNING_VIOLATIONS = {
    VIOLATION_FULLSCREEN_EXIT,
    VIOLATION_TAB_SWITCH,
    VIOLATION_COPY,
    VIOLATION_DEVTOOLS,
}


# =========================
# HELPER FUNCTIONS
# =========================

def is_valid_violation(violation_type: str) -> bool:
    """
    Check if violation type is known.
    """
    return violation_type in ALL_VIOLATIONS


def is_warning_violation(violation_type: str) -> bool:
    """
    Check if violation should increment warnings.
    """
    return violation_type in WARNING_VIOLATIONS


def get_violation_counter_field(violation_type: str) -> str | None:
    """
    Map violation type to QuizAttempt counter field.
    """
    mapping = {
        VIOLATION_FULLSCREEN_EXIT: "fullscreen_violations",
        VIOLATION_TAB_SWITCH: "tab_switch_violations",
        VIOLATION_COPY: "copy_violations",
        VIOLATION_DEVTOOLS: "devtools_violations",
    }
    return mapping.get(violation_type)
