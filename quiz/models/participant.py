from djongo import models


class Participant(models.Model):
    """
    Participant model matching API response format.
    This is used for data structure reference only.
    Actual data is fetched from external API.
    """
    id = models.IntegerField(primary_key=True)
    event = models.CharField(max_length=255)
    team_code = models.CharField(max_length=50)
    team_name = models.CharField(max_length=255)
    team_lead_name = models.CharField(max_length=255)
    college_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField()  # team_lead_email in API
    teammate1_name = models.CharField(max_length=255, blank=True)
    teammate2_name = models.CharField(max_length=255, blank=True)
    teammate3_name = models.CharField(max_length=255, blank=True)
    teammate4_name = models.CharField(max_length=255, blank=True)
    registration_date = models.DateTimeField(null=True, blank=True)
    idea_description = models.TextField(blank=True)  # For IdeaArena
    idea_file_url = models.URLField(blank=True)  # For IdeaArena

    class Meta:
        managed = False  # Data comes from external API
        db_table = "participants"  # Not actually used since managed=False

    @property
    def team_lead_email(self):
        """Alias for email field to maintain compatibility."""
        return self.email
