from django import forms
from quiz.models.quiz import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            "title",
            "description",
            "guidelines",
            "time_limit_minutes",
            "max_attempts",
            "warnings_allowed",
            "shuffle_questions",
            "shuffle_options",
            "allow_immediate_results",
            "start_time",
            "end_time",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "Quiz Title"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded",
                "rows": 3,
                "placeholder": "Quiz description"
            }),
            "guidelines": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded",
                "rows": 4,
                "placeholder": "Rules & guidelines"
            }),
            "time_limit_minutes": forms.NumberInput(attrs={
                "class": "w-full p-2 border rounded",
                "min": 1
            }),
            "max_attempts": forms.NumberInput(attrs={
                "class": "w-full p-2 border rounded",
                "min": 1
            }),
            "warnings_allowed": forms.NumberInput(attrs={
                "class": "w-full p-2 border rounded",
                "min": 0
            }),
            "shuffle_questions": forms.CheckboxInput(attrs={
                "class": "mr-2"
            }),
            "shuffle_options": forms.CheckboxInput(attrs={
                "class": "mr-2"
            }),
            "allow_immediate_results": forms.CheckboxInput(attrs={
                "class": "mr-2"
            }),
            "start_time": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "w-full p-2 border rounded"
            }),
            "end_time": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "w-full p-2 border rounded"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")

        if start and end and start >= end:
            raise forms.ValidationError(
                "End time must be after start time."
            )

        return cleaned_data
