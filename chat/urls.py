from django.urls import path
from . import views


urlpatterns=[
    path('create-room/<str:room_name>/',views.roomCreate.as_view(),name='room-create'),
    path('chat-admin/',views.admin,name='admin'),
    path('chat-admin/<str:uuid>/',views.room,name='room'),
]
