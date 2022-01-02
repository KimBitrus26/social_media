
from rest_framework import serializers
from rest_framework.generics import  ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import serializers, status

from rest_framework.permissions import IsAuthenticated

from .serializers import CommentSerializer, PictureSerializer
from social_media.pagination import StandardResultsSetPagination
from .models import Comment, Picture


class UploadPhotosView(ListCreateAPIView):
   
    serializer_class = PictureSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = StandardResultsSetPagination 

    def get_queryset(self):
        return Picture.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)