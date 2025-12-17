from django import forms


class ParticipantConfirmationForm(forms.Form):
    roll_number = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Enter your roll number"
        })
    )

    add_team_member = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "mr-2"
        })
    )

    extra_member_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Extra team member name"
        })
    )

    same_college = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            "class": "mr-2"
        })
    )

    college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Enter college name"
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        add_member = cleaned_data.get("add_team_member")
        extra_member_name = cleaned_data.get("extra_member_name")

        same_college = cleaned_data.get("same_college")
        college_name = cleaned_data.get("college_name")

        if add_member and not extra_member_name:
            self.add_error(
                "extra_member_name",
                "Please enter the extra team member name."
            )

        if not same_college and not college_name:
            self.add_error(
                "college_name",
                "Please enter your college name."
            )

        return cleaned_data
