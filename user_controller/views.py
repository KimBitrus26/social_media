from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserDetailsSerializer, UpdateProfileSerializer

from user_controller.models import CustomUser, UserProfile


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter

class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter


class CustomUserView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CustomUserDetailsSerializer(queryset, many=True)
        return Response(serializer.data)



class UpdateProfileView(UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ("patch",)
