from django import template
from django.dispatch.dispatcher import receiver
from chat.models import FriendList, FriendRequest

register = template.Library()


@register.filter(name='get_count_requests')
def get_count_requests(user):
    all_request = FriendRequest.objects.filter(receiver=user,status='requested')
    return all_request.count()

@register.filter(name='get_count_friends')
def get_count_friends(user):
    all_friend = FriendList.objects.get(user=user).friends
    return all_friend.count()

@register.simple_tag
def get_status_of_friend(user,friend):
    friends_list = FriendList.objects.get(user=friend)
    my_request = FriendRequest.objects.filter(sender=user,receiver=friend,status='requested')
    them_request = FriendRequest.objects.filter(sender=friend,receiver=user,status='requested')
    status = None
    if friends_list.is_friend(user):
        status = 'friend'
    elif my_request.exists():
        status = 'my_request'
    elif them_request.exists():
        status = 'them_request'
    elif user == friend:
        status = 'myself'
    else:
        status = 'not_friend'
    return status