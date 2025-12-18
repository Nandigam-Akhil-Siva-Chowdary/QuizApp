from django.db import models
from djongo import models as djongo_models


class QuizOption(djongo_models.Model):
    text = djongo_models.CharField(max_length=255)
    is_correct = djongo_models.BooleanField(default=False)

    class Meta:
        abstract = True


class QuizQuestion(models.Model):
    SINGLE = "single"
    MULTIPLE = "multiple"

    QUESTION_TYPE_CHOICES = (
        (SINGLE, "Single Answer"),
        (MULTIPLE, "Multiple Answer"),
    )

    # Django will auto-create 'id' field which Djongo maps to MongoDB's '_id'
    # We don't need to explicitly define it
    
    # Reference to quiz (this is just a foreign reference, NOT the primary key)
    quiz_id = djongo_models.ObjectIdField()
    question_text = models.TextField()

    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPE_CHOICES,
        default=SINGLE
    )

    # Embedded options (MongoDB-friendly) as an array of embedded documents
    options = djongo_models.ArrayField(
        model_container=QuizOption,
        null=False,
        blank=False,
    )

    # Optional explanations (used only if results are shown)
    explanation_correct = models.TextField(blank=True)
    explanation_wrong = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quiz_questions"

    def __str__(self):
        return self.question_text[:50]
