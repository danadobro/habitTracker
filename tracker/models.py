from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # each habit belongs to a user
    name = models.CharField(max_length=100)
    target = models.IntegerField()  # number of days to complete
    days_completed = models.IntegerField(default=0)
    logs = models.JSONField(default=list, blank=True)  # stores completed dates as list of strings
    completed = models.BooleanField(default=False)  # whether the habit is completed

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    

DAY_NAMES = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    
class ScheduledHabit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    frequency = models.CharField(max_length=10, choices=[('daily', 'Daily'), ('weekly', 'Weekly')])
    day_of_week = models.IntegerField(null=True, blank=True)  # 0=Monday ... 6=Sunday (for weekly habits)
    start_date = models.DateField(auto_now_add=True)
    completions = models.JSONField(default=list, blank=True)  # list of dates it was completed

    def is_due_today(self):
        from datetime import date
        today = date.today()

        if self.frequency == 'daily':
            return True
        elif self.frequency == 'weekly':
            return today.weekday() == self.day_of_week
        return False
    
    #get the text representation of the schedule
    def get_schedule_text(self):
        if self.frequency == "daily":
            return "Daily"
        # weekly
        return DAY_NAMES[self.day_of_week]
    
    def get_streak(self):
        today = date.today()
        logs_set = set(self.completions)
        streak = 0

        if self.frequency == 'daily':
            for i in range(0, len(logs_set)):
                check_day = today - timedelta(days=i)
                if check_day.isoformat() in logs_set:
                    streak += 1
                else:
                    break

        elif self.frequency == 'weekly':
            for i in range(0, 52):
                check_day = today - timedelta(weeks=i)
                while check_day.weekday() != self.day_of_week:
                    check_day -= timedelta(days=1)
                if check_day.isoformat() in logs_set:
                    streak += 1
                else:
                    break

        return streak
    
    # convenience so templates stay clean
    def streak_emoji(self):
        s = self.get_streak()
        return f"{s} 🔥" if s >= 3 else ""

    def __str__(self):
        return f"{self.name} ({self.frequency})"
    


class StickyNote(models.Model):
    COLOR_CHOICES = [
        ("yellow", "Yellow"), ("pink", "Pink"),
        ("blue", "Blue"), ("green", "Green"),
    ]
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    text  = models.CharField(max_length=255)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="yellow")

    def __str__(self):
        return f"Note({self.user.username}): {self.text}"
    

class ToDoList(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"List({self.user.username}): {self.title}"