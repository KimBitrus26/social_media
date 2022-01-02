from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer

from .models import Comment, Picture, Like


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = "__all__"


class PictureSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(read_only=True)
    like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Picture
        fields = "__all__"
        read_only_fields = ("id", "slug")
    
    def get_user(self, obj):
        return UserDetailsSerializer(obj.user, many=False).data

    def get_like(self, obj):
        return obj.like.count()

