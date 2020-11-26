from django.urls import path
from .views import RegistrationAPI, GetUserInfo, ForgotPasswordAPI

urlpatterns = [
    # student can access his information using this URL
    path('student/<email>/', GetUserInfo.as_view()),

    # admin can create and get all users, teacher can create student and get all students using this URL
    path('access/', RegistrationAPI.as_view()),

    # url for forgot password
    path('forgot_pass/', ForgotPasswordAPI.as_view())
]