from django import forms


class ParticipantConfirmationForm(forms.Form):
    """
    Confirm full team details before quiz:
    - Team lead roll
    - Up to 4 teammates (name, roll)
    - For each participant: same/different college as team lead, and custom college name if different.
    """

    # Team lead (always exists)
    team_lead_roll = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Team Lead Roll Number"
        }),
        label="Team Lead Roll Number",
    )

    # Teammate names & rolls (optional, up to 4)
    teammate1_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 1 Name",
        }),
        label="Teammate 1 Name",
    )
    teammate1_roll = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 1 Roll Number",
        }),
        label="Teammate 1 Roll Number",
    )

    teammate2_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 2 Name",
        }),
        label="Teammate 2 Name",
    )
    teammate2_roll = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 2 Roll Number",
        }),
        label="Teammate 2 Roll Number",
    )

    teammate3_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 3 Name",
        }),
        label="Teammate 3 Name",
    )
    teammate3_roll = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 3 Roll Number",
        }),
        label="Teammate 3 Roll Number",
    )

    teammate4_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 4 Name",
        }),
        label="Teammate 4 Name",
    )
    teammate4_roll = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 4 Roll Number",
        }),
        label="Teammate 4 Roll Number",
    )

    # Per-participant college flags
    team_lead_same_college = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "mr-2"}),
        label="Same college as registration",
    )

    teammate1_same_college = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "mr-2"}),
        label="Same college as team lead",
    )
    teammate1_college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 1 College Name",
        }),
        label="Teammate 1 College Name (if different)",
    )

    teammate2_same_college = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "mr-2"}),
        label="Same college as team lead",
    )
    teammate2_college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 2 College Name",
        }),
        label="Teammate 2 College Name (if different)",
    )

    teammate3_same_college = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "mr-2"}),
        label="Same college as team lead",
    )
    teammate3_college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 3 College Name",
        }),
        label="Teammate 3 College Name (if different)",
    )

    teammate4_same_college = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "mr-2"}),
        label="Same college as team lead",
    )
    teammate4_college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border rounded",
            "placeholder": "Teammate 4 College Name",
        }),
        label="Teammate 4 College Name (if different)",
    )

    def clean(self):
        cleaned_data = super().clean()

        # For each teammate: if a roll is given, a name must be provided (and vice versa)
        for idx in range(1, 5):
            name_key = f"teammate{idx}_name"
            roll_key = f"teammate{idx}_roll"
            name = cleaned_data.get(name_key, "").strip()
            roll = cleaned_data.get(roll_key, "").strip()

            if name and not roll:
                self.add_error(
                    roll_key,
                    "Please enter roll number for this teammate.",
                )
            if roll and not name:
                self.add_error(
                    name_key,
                    "Please enter name for this teammate.",
                )

        # Per-teammate college name required if not same_college
        for idx in range(1, 5):
            same_key = f"teammate{idx}_same_college"
            college_key = f"teammate{idx}_college_name"
            name_key = f"teammate{idx}_name"

            same = cleaned_data.get(same_key)
            college_name = cleaned_data.get(college_key, "").strip()
            has_member = bool(cleaned_data.get(name_key, "").strip())

            if has_member and not same and not college_name:
                self.add_error(
                    college_key,
                    "Please enter college name if different from team lead.",
                )

        return cleaned_data
