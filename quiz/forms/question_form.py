from django import forms
from quiz.models.question import QuizQuestion


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = [
            "question_text",
            "question_type",
            "explanation_correct",
            "explanation_wrong",
        ]

        widgets = {
            "question_text": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded",
                "rows": 3,
                "placeholder": "Enter the question"
            }),
            "question_type": forms.Select(attrs={
                "class": "w-full p-2 border rounded"
            }),
            "explanation_correct": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded",
                "rows": 2,
                "placeholder": "Explanation for correct answer (optional)"
            }),
            "explanation_wrong": forms.Textarea(attrs={
                "class": "w-full p-2 border rounded",
                "rows": 2,
                "placeholder": "Explanation for wrong answer (optional)"
            }),
        }

    def clean_question_text(self):
        text = self.cleaned_data.get("question_text")
        if not text:
            raise forms.ValidationError("Question text cannot be empty.")
        return text
