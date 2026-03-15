from django.urls import path
from .views import TaskView, AssignedTasksView, ReviewerTasksView


urlpatterns = [
    path("tasks/", TaskView.as_view(), name="board"),
    path("tasks/<int:task_id>/", TaskView.as_view(), name="single-task"),
    path("tasks/assigned-to-me/", AssignedTasksView.as_view(), name="assigned-to-me"),
    path("tasks/reviewing/", ReviewerTasksView.as_view(), name="reviewing"),
]