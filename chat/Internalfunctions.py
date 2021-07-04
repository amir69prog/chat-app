from chat import models

def create_request(receiver,sender):
    request = models.FriendRequest(
        receiver=receiver,
        sender=sender
    )
    request.save()
    return request


def accept_request(receiver,sender):
    try:
        request = models.FriendRequest.objects.get(
            receiver=receiver,
            sender=sender,
            status='requested'
        )
        request.status = 'accepted'
        request.save()
    except models.FriendRequest.DoesNotExist:
        return False
    return request

def cancel_request(receiver,sender):
    try:
        request = models.FriendRequest.objects.get(
            receiver=receiver,
            sender=sender,
            status='requested'
        )
        request.status = 'canceled'
        request.save()
    except models.FriendRequest.DoesNotExist:
        return False
    return request

def decline_request(receiver,sender):
    try:
        request = models.FriendRequest.objects.get(
            receiver=receiver,
            sender=sender,
            status='requested'
        )
        request.status = 'declined'
        request.save()
    except models.FriendRequest.DoesNotExist:
        return False
    return request