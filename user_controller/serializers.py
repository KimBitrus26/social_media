from django.db import models
import requests
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.core.exceptions import ValidationError as DjangoValidationError
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django.utils.translation import gettext as _
from dj_rest_auth.serializers import UserDetailsSerializer


from django.utils.encoding import force_str
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CustomUser, UserProfile


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ("email",)

class CustomRegisterSerializer(RegisterSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        self.fields.pop('password1')
        self.fields.pop('password2')
        self.fields.pop('username')
        super().__init__(*args, **kwargs)

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):

        return {
            # NOTE: using 'password1' because allauth uses it
            'password1': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

class CustomLoginSerializer(LoginSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')


class UpdateProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_user(self, obj):
        return UserDetailsSerializer(obj.user, many=False).data
