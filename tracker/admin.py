from django.contrib import admin
from .models import Habit, ScheduledHabit, StickyNote, ToDoList

admin.site.register(Habit)
admin.site.register(ScheduledHabit)
admin.site.register(StickyNote)
admin.site.register(ToDoList)

# Register your models here.

