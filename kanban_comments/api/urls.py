from django.urls import path
from .views import CommentView

urlpatterns = [
    path("tasks/<int:task_id>/comments/", CommentView.as_view(), name="task-comments"),
    path("tasks/<int:task_id>/comments/<int:comment_id>/", CommentView.as_view(), name="single-comment"),
]