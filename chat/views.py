from django.http.response import HttpResponse
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from chat.models import ChatRoomPrivate, ChatRoomPublic, FriendList, FriendRequest, MessagePrivate,Profile,User,get_chat_private_room
from .forms import ProfileForm,UserForm
from django.contrib import messages
from django.db.models import Q



def is_there_request(sender,receiver):
    try:
        request_sender = FriendRequest.objects.get(sender=sender,receiver=receiver,status='requested')
    except FriendRequest.DoesNotExist:
        return False
    return True

# Views
@login_required
def index(request):
    return render(request,'chat/index.html')


@login_required
def room_public(request,room_name):
    ''' Public Room '''
    room = get_object_or_404(ChatRoomPublic,name=room_name)
    return render(request,'chat/room.html',{'room_name':room_name})


def profile_view(request):
    ''' Profile all users also i and other users '''

    user = request.user
    profile = None

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)

    profile_form = ProfileForm(instance=profile)
    user_form = UserForm(instance=user)

    if request.POST:
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        user_form = UserForm(request.POST,instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.instance.user = user
            profile_form.save()
            user_form.save()
            messages.success(request,'Information successfully saved.')
            return redirect(request.path_info)
        else:
            profile_form = ProfileForm(request.POST,instance=profile)
            user_form = UserForm(request.POST,instance=user)

    context = {
        'profile':profile,
        'profile_form':profile_form,
        'user_form':user_form,
    }
    return render(request,'account/profile.html',context)


def room_private(request,user):
    ''' Generate the chat room for two user > Private '''
    pass


@login_required
def friends_list(request):
    ''' Display friends list '''
    user = request.user
    qs = FriendList.objects.get(user=user) 
    context = {'friends':qs.friends.all()}
    return render(request,'chat/friends_list.html',context)


def friend_requests(request):
    ''' Display all Request for this user '''
    user = request.user
    my_requests = FriendRequest.objects.filter(sender=user,status='requested')
    they_requests = FriendRequest.objects.filter(receiver=user,status='requested')
    context = {
        'my_requests':my_requests,
        'they_requests':they_requests
    }
    return render(request,'chat/friend_request.html',context)


@require_GET
def search(request):
    ''' Searching about users '''
    query = request.GET.get('q')
    if len(query) >= 2:
        if request.user.is_authenticated:
            qs = Profile.objects.filter(
                Q(user__username__icontains=query)|
                Q(user__email__icontains=query)|
                Q(nickname__icontains=query)
            ).exclude(user=request.user)
        else:
            qs = Profile.objects.filter(
                Q(user__username__icontains=query)|
                Q(user__email__icontains=query)|
                Q(nickname__icontains=query)
            )
    else:
        qs = None
    context = {
        'users':qs
    }
    return render(request,'chat/search_user.html',context)


@login_required
def user_profile(request,username):
    user = request.user
    profile = get_object_or_404(Profile,user__username=username)
    have_request = False
    has_request = False
    is_request = False
    is_friend = False
    is_self = False

    # am i his friend
    friends = FriendList.objects.get(user=profile.user)
    if friends.is_friend(user):
        is_friend = True
    # does this user has any request to that user
    request_friend = FriendRequest.objects.filter(sender=user,receiver=profile.user,status='requested')
    if request_friend:
        have_request = True
    # does that user has any request to this user
    his_request_friend = FriendRequest.objects.filter(sender=profile.user,receiver=user,status='requested')
    if his_request_friend:
        has_request = True
    # is there any request
    if has_request or have_request:
        is_request = True
    # its you?
    if profile.user == user:
        is_self = True
    
    context = {
        'profile':profile,
        'have_request':have_request,
        'request_friend':request_friend.first(),
        'his_request_friend':his_request_friend.first(),
        'has_request':has_request,
        'is_request':is_request,
        'is_self':is_self,
        'is_friend':is_friend
    }
    return render(request,'chat/user_profile.html',context)


@login_required
def user_friends(request,username):
    has_friend = True
    if request.user.username == username:
        return redirect('friends')
    qs = get_object_or_404(FriendList,user__username=username)
    if qs.friends.all().count() == 0:
        has_friend = False
    context = {
        'friends':qs.friends.all(),
        'has_friend':has_friend,
        'username':username
    }
    return render(request,'chat/user_friends.html',context)



@login_required
def chat_private(request,username):
    user = get_object_or_404(User,username=username)
    private_chat_room = get_chat_private_room(user,request.user)
    print(private_chat_room)
    messages = MessagePrivate.objects.filter(room=private_chat_room)
    friends = FriendList.objects.get(user=request.user)
    if not private_chat_room:
        return HttpResponse("this is not your friend")
    
    context = {
        'friend':user,
        'friends':friends.friends.all(),
        'messages':messages,
    }
    return render(request,'chat/chat_private.html',context) 
