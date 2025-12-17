import csv
import io


class CSVImportService:
    """
    Handles parsing and validation of quiz question CSV files.
    Does NOT save anything to DB.
    """

    REQUIRED_FIELDS = [
        "question_text",
        "question_type",
        "option1",
        "option2",
        "option3",
        "option4",
        "correct_options",
    ]

    OPTIONAL_FIELDS = [
        "explanation_correct",
        "explanation_wrong",
    ]

    QUESTION_TYPES = {"single", "multiple"}

    @staticmethod
    def parse_csv(file):
        """
        Parse CSV file and return:
        - valid_rows
        - errors
        """

        decoded_file = file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded_file))

        valid_rows = []
        errors = []

        # Validate headers
        missing_headers = [
            field for field in CSVImportService.REQUIRED_FIELDS
            if field not in reader.fieldnames
        ]

        if missing_headers:
            return [], [{
                "row": "header",
                "error": f"Missing required columns: {', '.join(missing_headers)}"
            }]

        for idx, row in enumerate(reader, start=1):
            row_errors = []

            # Required fields check
            for field in CSVImportService.REQUIRED_FIELDS:
                if not row.get(field):
                    row_errors.append(f"{field} is empty")

            # Question type validation
            q_type = row.get("question_type", "").lower()
            if q_type not in CSVImportService.QUESTION_TYPES:
                row_errors.append(
                    "question_type must be 'single' or 'multiple'"
                )

            # Correct options validation
            correct_opts = row.get("correct_options", "")
            correct_list = [
                opt.strip() for opt in correct_opts.split(",") if opt.strip()
            ]

            if not correct_list:
                row_errors.append("correct_options cannot be empty")

            if q_type == "single" and len(correct_list) != 1:
                row_errors.append(
                    "Single answer questions must have exactly one correct option"
                )

            if row_errors:
                errors.append({
                    "row": idx,
                    "errors": row_errors
                })
            else:
                valid_rows.append({
                    "question_text": row["question_text"],
                    "question_type": q_type,
                    "options": [
                        row["option1"],
                        row["option2"],
                        row["option3"],
                        row["option4"],
                    ],
                    "correct_options": correct_list,
                    "explanation_correct": row.get("explanation_correct", ""),
                    "explanation_wrong": row.get("explanation_wrong", ""),
                })

        return valid_rows, errors
