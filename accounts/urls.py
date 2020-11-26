from django.urls import path
from .views import RegistrationAPI, GetStudentInfo

urlpatterns = [
    path('student/<email>/', GetStudentInfo.as_view()),
    path('admin/access/', RegistrationAPI.as_view()),
]