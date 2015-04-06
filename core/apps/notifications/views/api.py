from rest_framework import generics
from rest_framework import permissions
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from listings.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from django.http import HttpResponse


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a notification instance.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


@api_view(['DELETE'])
def bulk_remove_notifications(request):
    notifications = request.user.notifications.all().exclude(key="feed.saved_search")
    for notification in notifications:
        notification.delete()
    return HttpResponse(status=200)


@api_view(['DELETE'])
def bulk_remove_matches(request):
    notifications = request.user.notifications.filter(key="feed.saved_search")
    notifications.delete()
    return HttpResponse(status=200)

@api_view(['POST'])
def mark_viewed(request):
    notifications = request.user.notifications.filter(viewed=False)
    for n in notifications:
        n.viewed = True
        n.save()
    return HttpResponse(status=200)