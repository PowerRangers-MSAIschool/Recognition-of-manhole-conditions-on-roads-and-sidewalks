# Home app ulrs!

from django.urls import path
from home import views

urlpatterns = [
    path('', views.home_main, name='main'),
    path('video_detect1', views.move_page1, name='move_test1'),
    path('video_detect2', views.move_page2, name='move_test2'),
    path('video_detect3', views.move_page3, name='move_test3'),
    path('video_detect4', views.move_page4, name='move_test4'),

]