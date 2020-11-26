from django.urls import path
from .views import RegistrationAPI, GetUserInfo

urlpatterns = [
    path('student/<email>/', GetUserInfo.as_view()),
    path('register/access/', RegistrationAPI.as_view()),
]