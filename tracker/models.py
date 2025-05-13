from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # each habit belongs to a user
    name = models.CharField(max_length=100)
    target = models.IntegerField()  # number of days to complete
    days_completed = models.IntegerField(default=0)
    logs = models.JSONField(default=list, blank=True)  # stores completed dates as list of strings

    def __str__(self):
        return f"{self.name} ({self.user.username})"