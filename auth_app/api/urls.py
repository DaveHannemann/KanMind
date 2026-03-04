from django.urls import path
from .views import RegisterView, LogoutView, LoginView, EmailCheckView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'login', LoginView, basename='login')

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]