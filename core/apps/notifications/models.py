from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.contrib.sites.models import Site


class NotificationManager(models.Manager):
    def unviewed_(self):
        return self.filter(viewed=False).count()


class Notification(models.Model):
    key = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='notifications')
    viewed = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType)
    date_created = models.DateField(auto_now_add=True)
    object_id = models.PositiveIntegerField()
    instance = GenericForeignKey('content_type', 'object_id')

    objects = NotificationManager()

    def get_absolute_url(self):
        if settings.ENABLE_HTTPS:
            scheme = 'https://{}{}'
        else:
            scheme = 'http://{}{}'
        return scheme.format(Site.objects.get_current().domain, self.instance.get_absolute_url())

    def when(self):
        return timezone.localtime(self.date_posted).strftime("%I:%M %p")

    def __unicode__(self):
        return u'%s for %s' % (self.key, self.user.username)


@receiver(post_save, sender=Notification)
def queue_notification_task(sender, instance, created, **kwargs):
    if created:
        from notifications.tasks import dispatch_notification
        dispatch_notification.delay(instance.id, instance.key, instance.object_id)
