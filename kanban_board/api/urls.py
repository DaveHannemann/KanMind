from django.urls import path
from .views import BoardView, SingleBoardView


urlpatterns = [
    path("boards/", BoardView.as_view(), name="board"),
    path("boards/<int:board_id>/", SingleBoardView.as_view(), name="single-board"),
]