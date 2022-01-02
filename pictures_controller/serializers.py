from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer

from .models import Comment, FriendLists, Picture, Like

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
   
    class Meta:
        model = Comment
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.first_name

class PictureSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Picture
        fields = "__all__"
        read_only_fields = ("id", "slug")
    
    def get_user(self, obj):
        return UserDetailsSerializer(obj.user, many=False).data

    def get_like(self, obj):
        return obj.like.count()

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = "__all__"
        
class FriendsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendLists
        fields = "__all__"
        