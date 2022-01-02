
from rest_framework import serializers
from rest_framework.generics import  CreateAPIView, ListCreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import IsAuthenticated

from .serializers import CommentSerializer, FriendsSerializer, LikeSerializer, PictureSerializer
from social_media.pagination import StandardResultsSetPagination
from .models import Comment, FriendLists, Like, Picture, PictureFile
from django.contrib.auth import get_user_model

User = get_user_model()


class UploadPhotosView(ListCreateAPIView):
   
    serializer_class = PictureSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = StandardResultsSetPagination 
    parser_class = [MultiPartParser, FormParser,]

    def get_queryset(self):
        return Picture.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        files = request.FILES.getlist("photos")
        if files:
            request.data.pop("photos")

            serializer = PictureSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)

                picture_qs = Picture.objects.get(id=serializer.data["id"])
                uploaded_pictures = []
                for file in files:
                    content = PictureFile.objects.create(user=user, photos=file)
                    uploaded_pictures.append(content)

                picture_qs.photos.add(*uploaded_pictures)
                context = serializer.data
                context["photos"] = [file.id for file in uploaded_pictures]
                return Response(context, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PictureSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                context = serializer.data
                return Response(context, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class PictureDetailDestroyView(RetrieveAPIView):
    """View to retrieve picture"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, picture_slug):
        try:
            return Picture.objects.get(slug=picture_slug)
        except Picture.DoesNotExist:
            return Response("Not found", status=status.HTTP_404_NOT_FOUND)

    def get(self, request,  picture_slug,  *args, **kwargs):
        instance = self.get_object(picture_slug) 
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
     
class CommentView(ListCreateAPIView):
   
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = StandardResultsSetPagination 

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        picture_slug = self.kwargs.get("picture_slug")
        picture = get_object_or_404(Picture, slug=picture_slug)
        data = request.data
        user = request.user
        content = data.get("content", None)

        comment = Comment.objects.create(user=user, picture=picture, content=content)

        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)
        
class LikeView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = StandardResultsSetPagination 

    def create(self, request, *args, **kwargs):
        picture_slug = self.kwargs.get("picture_slug")
        picture = get_object_or_404(Picture, slug=picture_slug)
        user = request.user
        like = Like.objects.create(user=user, picture_likes=picture)

        serializer = LikeSerializer(like, many=False)
        return Response(serializer.data)
        
class AddFriendRequestView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = StandardResultsSetPagination 

    def get_queryset(self):
        return FriendLists.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        to_user = get_object_or_404(User, pk=user_id)
        from_user = request.user
        friend_request, created = FriendLists.objects.get_or_create(user=from_user, friends=to_user)
        if created:
            return Response("Friend request sent", status=status.HTTP_201_CREATED)
        return Response("Friend request was already sent")
        
