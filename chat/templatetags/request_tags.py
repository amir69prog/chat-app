from django import template
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