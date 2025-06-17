from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, ScheduledHabit, StickyNote, ToDoList
from django.contrib.auth.decorators import login_required
from datetime import date
from django.utils import timezone
from django.contrib import messages

@login_required
def home(request):
    habits = Habit.objects.filter(user=request.user, completed=False)
    scheduled_habits = ScheduledHabit.objects.filter(user=request.user)

    sticky_notes = StickyNote.objects.filter(user=request.user)
    todolists    = ToDoList.objects.filter(user=request.user)

    # Add progress percent to each habit
    for habit in habits:
        if habit.target > 0:
            habit.progress = int((habit.days_completed / habit.target) * 100)
        else:
            habit.progress = 0

    # Show scheduled habits due today in the TODAY section
    due_today = [
        h for h in ScheduledHabit.objects.filter(user=request.user) if h.is_due_today()
    ]


    return render(request, 'home.html', {
        'habits': habits,
        'scheduled_habits': scheduled_habits,
        'today_habits': due_today,
        'today': timezone.localdate().isoformat(),
        'today_str': timezone.localdate().strftime("%a %B %d %Y"),
        'sticky_notes': sticky_notes,
        'todolists': todolists,
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
            # Check if the habit is being completed
            if habit.days_completed >= habit.target:
                habit.completed = True # Mark the habit as completed
            habit.save()

        return redirect('home')

#habits view
def habits(request):
    # Get all habits for the logged-in user
    active = Habit.objects.filter(user=request.user, completed=False)
    completed = Habit.objects.filter(user=request.user, completed=True)
    scheduled = ScheduledHabit.objects.filter(user=request.user)
    return render(request, 'habits.html', {
        'active_habits': active,
        'completed_habits': completed,
        'scheduled_habits': scheduled,
        })

@login_required
def add_scheduled_habit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        frequency = request.POST.get('frequency')
        day_of_week = request.POST.get('day_of_week') or None  # convert empty string to None

        if day_of_week is not None:
            day_of_week = int(day_of_week)

        ScheduledHabit.objects.create(
            user=request.user,
            name=name,
            frequency=frequency,
            day_of_week=day_of_week
        )
        return redirect('home')

@login_required
def mark_scheduled_habit_done(request, habit_id):
    habit = get_object_or_404(ScheduledHabit, id=habit_id, user=request.user)
    today_str = date.today().isoformat()

    if today_str not in habit.completions:
        habit.completions.append(today_str)
        habit.save()

    return redirect('home')

#delete scheduled habit
@login_required
def delete_scheduled_habit(request, habit_id):
    habit = get_object_or_404(ScheduledHabit, id=habit_id, user=request.user)
    habit.delete()
    return redirect('habits')

@login_required
def add_note(request):
    if request.method == "POST":
        if StickyNote.objects.filter(user=request.user).count() >= 5:
            messages.warning(request, "Maximum 5 sticky notes.")
        else:
            StickyNote.objects.create(
                user=request.user,
                text=request.POST.get("text"),
                color=request.POST.get("color", "yellow")
            )
    return redirect('home')

@login_required
def edit_note(request, note_id):
    if request.method == "POST":
        note = get_object_or_404(StickyNote, id=note_id, user=request.user)
        note.text  = request.POST.get("text")
        note.color = request.POST.get("color", note.color)
        note.save()
    return redirect('home')

@login_required
def delete_note(request, note_id):
    StickyNote.objects.filter(id=note_id, user=request.user).delete()
    return redirect('home')

@login_required
def add_todolist(request):
    if request.method == "POST":
        if ToDoList.objects.filter(user=request.user).count() >= 3:
            messages.warning(request, "Maximum 3 to-do lists.")
        else:
            ToDoList.objects.create(
                user=request.user,
                title=request.POST.get("title")
            )
    return redirect('home')

@login_required
def edit_todolist(request, list_id):
    tdl = get_object_or_404(ToDoList, id=list_id, user=request.user)
    if request.method == "POST":
        tdl.title = request.POST.get("title")
        tdl.save()
    return redirect('home')

@login_required
def delete_todolist(request, list_id):
    ToDoList.objects.filter(id=list_id, user=request.user).delete()
    return redirect('home')