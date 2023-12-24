# Video app ulrs!

from django.urls import path
from video import views

urlpatterns = [
    # 127.0.0.1:8000/video_test
    path('video_test', views.video, name='video_test'),
    path('send_status', views.send_status, name='send_status'),
]