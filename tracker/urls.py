from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_habit, name='add_habit'),
    path('complete/', views.mark_complete, name='mark_complete'),
    path('habits/', views.habits, name='habits'),
    path('add_scheduled/', views.add_scheduled_habit, name='add_scheduled_habit'),
    path('mark_done/<int:habit_id>/', views.mark_scheduled_habit_done, name='mark_scheduled_habit_done'),
    path('delete_scheduled/<int:habit_id>/', views.delete_scheduled_habit, name='delete_scheduled_habit'),
    path('note/add/', views.add_note, name='add_note'),
    path('note/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('todolist/add/', views.add_todolist, name='add_todolist'),
    path('todolist/<int:list_id>/edit/', views.edit_todolist, name='edit_todolist'),
    path('todolist/<int:list_id>/delete/', views.delete_todolist, name='delete_todolist'),

]