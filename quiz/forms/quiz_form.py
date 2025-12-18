from django import forms
from django.conf import settings
from django.utils import timezone
import datetime

from quiz.models.quiz import Quiz
from quiz.services.events_api_service import EventsAPIService


class QuizForm(forms.ModelForm):
    """
    Admin form for creating/editing a quiz.
    Uses separate date and time pickers for start/end.
    """

    event_name = forms.ChoiceField(
        required=True,
        choices=[],
        label="Event",
        help_text="Select which event this quiz belongs to (must match participant registration event).",
        widget=forms.Select(attrs={
            "class": "w-full p-2 border rounded",
        }),
    )

    # Separate date and time fields for start/end
    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "w-full p-2 border rounded",
        }),
        label="Start date",
    )
    start_time_part = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={
            "type": "time",
            "class": "w-full p-2 border rounded",
        }),
        label="Start time",
    )
    end_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "w-full p-2 border rounded",
        }),
        label="End date",
    )
    end_time_part = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={
            "type": "time",
            "class": "w-full p-2 border rounded",
        }),
        label="End time",
    )

    class Meta:
        model = Quiz
        # NOTE: we exclude model start_time/end_time and set them manually
        fields = [
            "title",
            "event_name",
            "description",
            "guidelines",
            "time_limit_minutes",
            "max_attempts",
            "warnings_allowed",
            "shuffle_questions",
            "shuffle_options",
            "allow_immediate_results",
            "is_active",
            # start_time / end_time are set in clean() / save()
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "Quiz Title",
            }),
            "event_name": forms.Select(attrs={
                "class": "w-full p-2 border rounded",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded",
                "rows": 3,
                "placeholder": "Quiz description",
            }),
            "guidelines": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded",
                "rows": 4,
                "placeholder": "Rules & guidelines",
            }),
            "time_limit_minutes": forms.NumberInput(attrs={
                "class": "w-full p-2 border rounded",
                "min": 1,
            }),
            "max_attempts": forms.NumberInput(attrs={
                "class": "w-full p-2 border rounded",
                "min": 1,
            }),
            "warnings_allowed": forms.NumberInput(attrs={
                "class": "w-full p-2 border rounded",
                "min": 0,
            }),
            "shuffle_questions": forms.CheckboxInput(attrs={
                "class": "mr-2",
            }),
            "shuffle_options": forms.CheckboxInput(attrs={
                "class": "mr-2",
            }),
            "allow_immediate_results": forms.CheckboxInput(attrs={
                "class": "mr-2",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "mr-2",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate event choices from external API
        choices = EventsAPIService.get_event_name_choices()
        if choices:
            self.fields["event_name"].choices = choices
        else:
            # Fallback to known set if API fails
            fallback = [
                ("InnovWEB", "InnovWEB"),
                ("SensorShowDown", "SensorShowDown"),
                ("IdeaArena", "IdeaArena"),
                ("Error Erase", "Error Erase"),
            ]
            self.fields["event_name"].choices = fallback

        # If editing an existing quiz, prefill date/time parts from model fields
        if self.instance and self.instance.pk and self.instance.start_time:
            start = self.instance.start_time
            end = self.instance.end_time
            if timezone.is_aware(start):
                start = timezone.localtime(start)
            if timezone.is_aware(end):
                end = timezone.localtime(end)
            self.fields["start_date"].initial = start.date()
            self.fields["start_time_part"].initial = start.time().replace(microsecond=0)
            if end:
                self.fields["end_date"].initial = end.date()
                self.fields["end_time_part"].initial = end.time().replace(microsecond=0)

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        start_time = cleaned_data.get("start_time_part")
        end_date = cleaned_data.get("end_date")
        end_time = cleaned_data.get("end_time_part")

        if start_date and start_time and end_date and end_time:
            start_dt = datetime.datetime.combine(start_date, start_time)
            end_dt = datetime.datetime.combine(end_date, end_time)

            if getattr(settings, "USE_TZ", False):
                tz = timezone.get_current_timezone()
                start_dt = timezone.make_aware(start_dt, tz)
                end_dt = timezone.make_aware(end_dt, tz)

            if start_dt >= end_dt:
                raise forms.ValidationError("End time must be after start time.")

            # Store combined datetimes so save() can use them
            cleaned_data["start_time"] = start_dt
            cleaned_data["end_time"] = end_dt

        return cleaned_data

    def save(self, commit=True):
        """
        Ensure model.start_time / end_time are set from combined fields.
        """
        instance = super().save(commit=False)
        start_dt = self.cleaned_data.get("start_time")
        end_dt = self.cleaned_data.get("end_time")
        if start_dt:
            instance.start_time = start_dt
        if end_dt:
            instance.end_time = end_dt

        if commit:
            instance.save()
        return instance
