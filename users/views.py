from django.shortcuts import render

from rest_framework import generics

from . import models
from users.serializers import UserSerializer

from .models import CustomUser

import jwt
import uuid
import warnings

from django.contrib.auth import get_user_model

from calendar import timegm
from datetime import datetime

from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings

from django.http.response import HttpResponse


# def drf_login(request):
#     return HttpResponse("my login")


class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer

def jwt_payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)

    payload = {
        'user_id': user.pk,
        'username': username,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    if hasattr(user, 'role'):
        payload['role'] = user.role
    if hasattr(user, 'default_dashboard'):
        payload['default_dashboard'] = user.default_dashboard
    # if hasattr(user, 'dashboards'):
    #     payload['dashboards'] = user.dashboards

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload




from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_jwt.settings import api_settings
from rest_auth.serializers import LoginSerializer, TokenSerializer


class LoginView(APIView):
    '''
    Post call for user login.
    '''
    def get(self):
        return HttpResponse("get my login called")

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            # Check if user has valid credentials and return user instance else None
            user = serializer.authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])

            if user is not None:

                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                return Response({'msg':'Login successful', 'token': token, 'is_login_success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Credentials are not valid!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_auth.views import LoginView

from django.contrib.auth import login

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions

class LoginView1(LoginView):
    def get_response(self):
        orginal_response = super().get_response()
        mydata = {"message": "some message", "status": "success"}
        orginal_response.data.update(mydata)
        return orginal_response

# jwt_payload_handler = jwt_payload_handler
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from rest_framework import serializers
class CustomTokenSerializer(serializers.Serializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = TokenModel
        fields = ('key',)


class LoginView2(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    # permission_classes = (permissions.AllowAny,)

    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        serializer = LoginSerializer(data=request.data)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "key": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()


            # response = jwt_encode_handler(jwt_payload_handler(user))
            return Response(serializer.data)
            # return Response(response)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



