from django import forms


class QuizCSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload Quiz CSV",
        help_text="Upload a CSV file containing quiz questions",
        widget=forms.ClearableFileInput(attrs={
            "class": "w-full p-2 border rounded",
            "accept": ".csv"
        })
    )

    def clean_csv_file(self):
        file = self.cleaned_data.get("csv_file")

        if not file:
            raise forms.ValidationError("No file uploaded.")

        if not file.name.endswith(".csv"):
            raise forms.ValidationError("Only CSV files are allowed.")

        # Optional: size limit (e.g., 5MB)
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("CSV file size should not exceed 5MB.")

        return file
