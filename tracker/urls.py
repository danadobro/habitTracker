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

]