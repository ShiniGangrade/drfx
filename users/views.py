"""
todo - check default_dashboard is null/""
- on creating using api - it saves as null

"""
import uuid
from calendar import timegm
from datetime import datetime

from django.contrib.auth import authenticate, login
from rest_auth.serializers import LoginSerializer
from rest_framework import generics, status, permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenSerializer, CustomRegisterUserSerializer


jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


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
    if hasattr(user, 'dashboards'):
        payload['dashboards'] = list(user.dashboards.get_queryset().values_list("name", flat=True))

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



# class CustomUserViewSet(viewsets.ModelViewSet):
class CustomUserViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    # serializer_class = CustomUserSerializer

    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action in ['create']:
            return CustomRegisterUserSerializer
        # if self.action in[ 'update' ,'retrieve', 'list']:
        #     return CustomUserSerializer
        return CustomUserSerializer


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = CustomTokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "access_token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )
            })
            serializer.is_valid()

            return Response(serializer.data)
            # return Response(response)
        return Response(status=status.HTTP_401_UNAUTHORIZED)




# class RegisterUser(generics.CreateAPIView):
#     """
#     POST auth/register/
#     """
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = CustomRegisterUserSerializer
#
#     # def post(self, request, *args, **kwargs):
#     #     print("view registeruser called")
#     #     username = request.data.get("username", "")
#     #     password = request.data.get("password", "")
#     #     email = request.data.get("email", "")
#     #     role = request.data.get("role", "user")
#     #
#     #     if not username or not password or not email:
#     #         return Response(
#     #             data={
#     #                 "message": "username, password and email is required to register a user"
#     #             },
#     #             status=status.HTTP_400_BAD_REQUEST
#     #         )
#     #     new_user = CustomUser.objects.create_user(
#     #         username=username, password=password, email=email, role=role
#     #     )
#     #     return Response(status=status.HTTP_201_CREATED)
#     #
