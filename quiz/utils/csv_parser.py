import csv
from io import TextIOWrapper


REQUIRED_COLUMNS = [
    "question_text",
    "question_type",      # single | multiple
    "option_1",
    "option_2",
    "correct_options",    # comma separated option numbers: 1,3
]


OPTION_COLUMNS = [
    "option_1",
    "option_2",
    "option_3",
    "option_4",
    "option_5",
]


def parse_quiz_csv(file):
    """
    Parse and validate quiz CSV.

    Returns:
        preview_data: list of parsed questions
        errors: list of {row, errors[]}
    """

    preview_data = []
    errors = []

    reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))

    for idx, row in enumerate(reader, start=2):  # header is row 1
        row_errors = []

        # Required fields check
        for col in REQUIRED_COLUMNS:
            if not row.get(col):
                row_errors.append(f"Missing {col}")

        question_type = row.get("question_type", "").lower()
        if question_type not in ("single", "multiple"):
            row_errors.append("question_type must be 'single' or 'multiple'")

        # Collect options
        options = []
        for col in OPTION_COLUMNS:
            if row.get(col):
                options.append(row[col].strip())

        if len(options) < 2:
            row_errors.append("At least two options are required")

        # Parse correct options
        correct_raw = row.get("correct_options", "")
        try:
            correct_indexes = [
                int(i.strip())
                for i in correct_raw.split(",")
                if i.strip()
            ]
        except ValueError:
            correct_indexes = []
            row_errors.append("correct_options must be numbers (e.g., 1,3)")

        if not correct_indexes:
            row_errors.append("At least one correct option required")

        # Validate correct option indexes
        for idx_opt in correct_indexes:
            if idx_opt < 1 or idx_opt > len(options):
                row_errors.append(
                    f"Correct option index {idx_opt} is out of range"
                )

        # Multiple vs single validation
        if question_type == "single" and len(correct_indexes) > 1:
            row_errors.append(
                "Single choice question cannot have multiple correct options"
            )

        if row_errors:
            errors.append({
                "row": idx,
                "errors": row_errors
            })
            continue

        preview_data.append({
            "question_text": row["question_text"].strip(),
            "question_type": question_type,
            "options": options,
            "correct_options": [
                options[i - 1] for i in correct_indexes
            ],
            "explanation_correct": row.get("explanation_correct", "").strip(),
            "explanation_wrong": row.get("explanation_wrong", "").strip(),
        })

    return preview_data, errors
