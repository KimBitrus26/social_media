
from django.urls import path

from pictures_controller.views import AddFriendRequestView, CommentView, LikeView, PictureDetailDestroyView, UploadPhotosView

urlpatterns = [
  
    path("upload-pictures/", UploadPhotosView.as_view(), name="upload-pictures"),
    path("<slug:picture_slug>/picture/", PictureDetailDestroyView.as_view(), name="update-quantity"),
    path("<slug:picture_slug>/comment/", CommentView.as_view(), name="comment"),
    path("<slug:picture_slug>/like/", LikeView.as_view(), name="like"),
    path("<int:user_id>/friend-reques/", AddFriendRequestView.as_view(), name="friend-request"),
    
]