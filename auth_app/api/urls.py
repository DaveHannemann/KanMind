from django.urls import path
from .views import RegisterView, LoginView, EmailCheckView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'login', LoginView, basename='login')

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path('registration', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('email-check', EmailCheckView.as_view(), name='email-check'),
]