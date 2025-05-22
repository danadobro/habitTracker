from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def home(request):
    habits = Habit.objects.filter(user=request.user)

    # Add progress percent to each habit
    for habit in habits:
        if habit.target > 0:
            habit.progress = int((habit.days_completed / habit.target) * 100)
        else:
            habit.progress = 0

    return render(request, 'home.html', {
        'habits': habits,
        'today': date.today().isoformat(),
        'today_str': date.today().strftime("%a %B %d %Y"),
        })

@login_required
def add_habit(request):
    if request.method == 'POST':
        name = request.POST.get("habit_name")
        target = request.POST.get("target")
        Habit.objects.create(user=request.user, name=name, target=target)
        return redirect('home')

def mark_complete(request):
    if request.method == 'POST':
        habit_id = request.POST.get("habit_id")
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)

        today_str = request.POST.get("date") or date.today().isoformat()

        if today_str not in habit.logs:
            habit.logs.append(today_str)
            habit.days_completed += 1
            habit.save()

        return redirect('home')


        

