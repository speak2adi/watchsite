from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, TokenAuthentication
from .backends import CustomModelBackend
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger(__name__)


# AUTH VIEWS


# login with facebook
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


# login with github
class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter


# login with google
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
    client_class = OAuth2Client


# login with twitter
class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


# register user
class UserRegistration(CreateAPIView):
    serializer_class = UserSerializer


# Logout View
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = CustomUser.objects.get(email=email)

        if user is None:
            raise AuthenticationFailed('USER DOES NOT EXIST')
        if not user.check_passoword(password):
            raise AuthenticationFailed("Incorrect Password")

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        return Response({
            "access_token": access_token,
            "refresh_token": refresh_token,
        })


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response("Logout Successful", status=status.HTTP_200_OK)
        except TokenError:
            raise AuthenticationFailed("Invalid Token")

