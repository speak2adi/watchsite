from django.contrib import admin
from django.urls import path, include
from allauth.account.views import confirm_email
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("backend.urls")),
    path('', include("users.urls")),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('rest_framework.urls')),
    path('account/', include('allauth.urls')),
    path('account/confirm-email/<str:key>/', confirm_email, name='account_confirm_email'),

]
