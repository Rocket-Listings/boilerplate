from django.db import models
from django.contrib.auth.models import User
from notifications.models import Notification

def global_notifications(request):
    if request.user.is_authenticated():
        notifications = request.user.notifications.filter(viewed=False)
        return {
        'notifications': notifications
        }
    else:
        return {
        'notifications': False
        }
