
from django.urls import path

from pictures_controller.views import CommentView, PictureDetailDestroyView, UploadPhotosView

urlpatterns = [
  
    path("upload-pictures/", UploadPhotosView.as_view(), name="upload-pictures"),
    path("<slug:picture_slug>/picture/", PictureDetailDestroyView.as_view(), name="update-quantity"),
    path("comment/", CommentView.as_view(), name="upload-pictures"),
    
]