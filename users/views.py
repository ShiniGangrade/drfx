"""
todo - check default_dashboard is null/""
- on creating using api - it saves as null

todo - logout

"""

from django.contrib.auth import authenticate, login

from rest_auth.serializers import LoginSerializer
from rest_framework import generics, status, permissions, viewsets, mixins

from rest_framework_jwt.settings import api_settings
from django.utils.decorators import method_decorator
from .models import CustomUser, Role, Grant
from .serializers import CustomUserSerializer, CustomRegisterUserSerializer, RoleSerializer, \
    GrantSerializer #, PasswordChangeSerializer
from api.serializers import UserJWTTokenSerializer

# from rest_auth.serializers import PasswordChangeSerializer
from django.views.decorators.debug import sensitive_post_parameters

from allauth.socialaccount.providers.microsoft.views import MicrosoftGraphOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.http import HttpResponse
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.response import Response



class CustomUserViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    queryset = CustomUser.objects.all()
    # # permission_classes = (permissions.AllowAny,)  # change
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.IsAdminUser,)

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
            serializer = UserJWTTokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "access_token": api_settings.JWT_ENCODE_HANDLER(
                    api_settings.JWT_PAYLOAD_HANDLER(user)
                )
            })
            serializer.is_valid()

            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (permissions.AllowAny,)  # change


class GrantViewSet(viewsets.ModelViewSet):
    queryset = Grant.objects.all()
    serializer_class = GrantSerializer
    permission_classes = (permissions.AllowAny,)  # change


def demo(request):
    print(">>> demo route", request.user)
    return HttpResponse("demo route")



class MicrosoftLogin(SocialLoginView):
    adapter_class = MicrosoftGraphOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:8000/accounts/microsoft/callback/'

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        r = self.get_response()
        return Response({'access_token': r.data['token'], "token_type": "Bearer"})













sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

# class PasswordChangeView(GenericAPIView):
#     """
#     Calls Django Auth SetPasswordForm save method.
#
#     Accepts the following POST parameters: new_password1, new_password2
#     Returns the success/fail message.
#     """
#     serializer_class = PasswordChangeSerializer
#     # permission_classes = (permissions.IsAuthenticated,)
#     permission_classes = (permissions.AllowAny,)
#
#     @sensitive_post_parameters_m
#     def dispatch(self, *args, **kwargs):
#         return super(PasswordChangeView, self).dispatch(*args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         print("in pwd change 1")
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print("in pwd change 2")
#         return Response({"detail": _("New password has been saved.")})


