from djongo import models


class Participant(models.Model):
    _id = models.ObjectIdField(primary_key=True)

    team_code = models.CharField(max_length=50)
    team_name = models.CharField(max_length=255)

    team_lead_name = models.CharField(max_length=255)
    team_lead_email = models.EmailField()

    college_name = models.CharField(max_length=255)
    event = models.CharField(max_length=255)

    class Meta:
        managed = False   # VERY IMPORTANT
        db_table = "events_participant"
