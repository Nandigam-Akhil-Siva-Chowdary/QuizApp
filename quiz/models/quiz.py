from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    guidelines = models.TextField(blank=True)

    # Event this quiz belongs to (matches NexusOfThings event.name)
    event_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Event name, e.g. InnovWEB, SensorShowDown, IdeaArena, Error Erase",
    )

    # Quiz rules
    time_limit_minutes = models.PositiveIntegerField(
        help_text="Time limit in minutes"
    )

    max_attempts = models.PositiveIntegerField(
        default=1,
        help_text="Maximum attempts allowed per team"
    )

    warnings_allowed = models.PositiveIntegerField(
        default=2,
        help_text="Number of warnings before auto exit"
    )

    shuffle_questions = models.BooleanField(default=True)
    shuffle_options = models.BooleanField(default=True)

    allow_immediate_results = models.BooleanField(
        default=False,
        help_text="Allow users to see results immediately after submission"
    )

    # Availability window
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quiz_quizzes"

    def __str__(self):
        return self.title

    def is_live(self, now):
        """
        Check if quiz is currently live.
        """
        return self.is_active and self.start_time <= now <= self.end_time
