from django.urls import path, include
from .views import FacebookLogin, TwitterLogin, GoogleLogin, GithubLogin, UserRegistration, LoginView, LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('facebook/login/', FacebookLogin.as_view(), name='fb_login'),
    path('facebook/login/', FacebookLogin.as_view(), name='fb_login'),
    path('github/login/', GithubLogin.as_view(), name='github_login'),
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path('twitter/login/', TwitterLogin.as_view(), name='twitter_login'),
    path('register/', UserRegistration.as_view(), name='register'),

]
