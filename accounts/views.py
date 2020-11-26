from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import CreateUserSerializer, GetUserSerializer
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework import status
from .models import OtpGenerator
import random

# getting user model
User = get_user_model()

# for admin users - get all users, post user
class RegistrationAPI(APIView):
    # post method to create user
    def post(self, request, format=None):
        entry_email = self.request.user

        # if admin user is making request
        if 'admin' in list(Group.objects.filter(user__email__iexact=str(entry_email)).values_list('name', flat=True)):
            serializer = CreateUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({"user created": request.data['email']}, status=status.HTTP_201_CREATED)

        # if teacher is making request
        elif 'teacher' in list(Group.objects.filter(user__email__iexact=str(entry_email)).values_list('name', flat=True)):
            if request.data['groups'] == ['student']:
                serializer = CreateUserSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                return Response({"Student created": request.data['email']}, status=status.HTTP_201_CREATED)
            else:
                return Response({"Access Denied": "You can only create student"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Access Denied': "You don't have access" }, status=status.HTTP_401_UNAUTHORIZED)

    # get method to get all users
    def get(self, request, format=None):
        entry_email = self.request.user
        if 'admin' in list(Group.objects.filter(user__email__iexact=str(entry_email)).values_list('name', flat=True)):
            queryset = User.objects.all()
            serializer = GetUserSerializer(queryset, many=True)
            return Response({"All Users": serializer.data}, status=status.HTTP_200_OK)
        elif 'teacher' in list(Group.objects.filter(user__email__iexact=str(entry_email)).values_list('name', flat=True)):
            queryset = User.objects.filter(groups__name='student')
            serializer = GetUserSerializer(queryset, many=True)
            return Response({"All Students": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'Access Denied': "You don't have access"}, status=status.HTTP_401_UNAUTHORIZED)


# for student - get his own information only, teacher and admin can also view their info
class GetUserInfo(APIView):
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
            return Response({'your_info': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'Access denied': 'You can view only your information'}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordAPI(APIView):
    # permission of this endpoint should be AllowAny forgot password does not requires authentication
    permission_classes = (permissions.AllowAny, )

    # get OTP for password change
    def get(self, request, format=None):
        email = request.data['email']
    
        # 6 letter OTP
        otp = random.randint(100000, 999999)

        # generate OTP instance to later check for authenticity, we can mail this OTP to email
        try:
            OtpGenerator.objects.get(email__iexact=email).delete()
        except OtpGenerator.DoesNotExist:
            obj = OtpGenerator.objects.create(email=email, otp=otp)
        # return OTP
        return Response({'OTP': obj.otp}, status=status.HTTP_200_OK)
        
    # post OTP with email and new password
    def post(self, request, format=None):
        email = request.data['email']
        otp = request.data['otp']
        password1 = request.data['password1']
        password2 = request.data['password2']

        # check if passwords are same
        if password1 == password2:
            user = User.objects.get(email=email)
            if user is not None:
                user.set_password(password1)
                user.save()
                # delete OTP instance
                OtpGenerator.objects.filter(email__iexact=email).delete()

                return Response({"Success": "Password changed"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"Error": "User not registered"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        

