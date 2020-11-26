from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import CreateUserSerializer, GetUserSerializer
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.response import Response
from django.contrib.auth.models import Group

# getting user model
User = get_user_model()

# for admin users - get all users, post user
class RegistrationAPI(APIView):
    # post method to create user
    def post(self, request, format=None):
        entry_email = self.request.user
        if 'admin' in list(Group.objects.filter(user__email__iexact=str(entry_email)).values_list('name', flat=True)):
            serializer = CreateUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({"user created": request.data['email']})
        else:
            return Response({'Access Denied': "You don't have access" })

    # get method to get all users
    def get(self, request, format=None):
        entry_email = self.request.user
        if 'admin' in list(Group.objects.filter(user__email__iexact=str(entry_email)).values_list('name', flat=True)):
            queryset = User.objects.all()
            serializer = GetUserSerializer(queryset, many=True)
            return Response({"All Users": serializer.data})
        else:
            return Response({'Access Denied': "You don't have access" })

# for student - get his own information only
class GetStudentInfo(APIView):
    serializer_class = GetUserSerializer

    # for getting email from URL
    def get_object(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404
    # get method to view students own information
    def get(self, request, email, format=None):
        entry_email = self.request.user
        if str(entry_email) == str(email):
            user = self.get_object(email)
            serializer = GetUserSerializer(user)
            return Response({'your_info': serializer.data})
        else:
            return Response({'Access denied': 'You can view only your information'})




