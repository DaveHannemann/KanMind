from django.urls import path
from .views import TaskView


urlpatterns = [
    path("tasks/", TaskView.as_view(), name="board"),
    path("tasks/<int:task_id>/", TaskView.as_view(), name="single-task"),
    path("tasks/assigned-to-me/", TaskView.as_view(), name="assigned-to-me-tasks"),
    path("tasks/reviewing/", TaskView.as_view(), name="reviewing-tasks"),
]