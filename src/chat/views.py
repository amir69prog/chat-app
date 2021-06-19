from django.shortcuts import render,get_object_or_404
# from chat.models import Room


def index(request):
    return render(request,'chat/index.html')

def room(request,room_name):
    # room = get_object_or_404(Room,name=room_name)
    return render(request,'chat/room.html',{'room_name':room_name})