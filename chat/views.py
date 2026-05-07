from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from chat.serializer import roomSerializer
from chat.models import Room,Messages
from django.contrib.auth.decorators import login_required
from account.models import User

class roomCreate(generics.CreateAPIView):
    room=Room.objects.all()
    serializer_class=roomSerializer

    def perform_create(self, serializer):
        room_name=self.kwargs.get('room_name')
        serializer.save(uuid=room_name)


@login_required
def admin(request):
    room=Room.objects.all()
    users=User.objects.filter(is_staff=True)
    return render(request,'chat/admin.html',{
        'room':room,
        'users':users
    })




@login_required
def room(request,uuid):
    room=Room.objects.get(uuid=uuid)
    if room.status==room.WAITING:
        room.status=room.ACTIVE
        room.agent=request.user
        room.save()
    return render(request,'chat/room.html',{
        'room':room,

    })
