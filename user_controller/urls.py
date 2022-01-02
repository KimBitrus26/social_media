from user_controller.views import FacebookConnect, GoogleConnect, CustomUserView, FacebookLogin, GoogleLogin, UpdateProfileView
from django.urls import path, include
from dj_rest_auth.registration.views import VerifyEmailView
from . import views

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("facebook/connect/", FacebookConnect.as_view(), name="fb_connect"),
    path("google/connect/", GoogleConnect.as_view(), name="google_connect"),
    path("facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("users/", CustomUserView.as_view(), name="users"),
    path('registration/verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('registration/verify-email/<slug:key>/', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('<pk>/user-profile/', UpdateProfileView.as_view(), name='user-profile'),
]
