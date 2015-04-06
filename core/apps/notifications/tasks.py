from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from notifications.models import Notification
from notifications.templatetags.notifications import render_notification
from listings.models import UserProfile, FBGroup
from utils.tasks import fb_graph
import logging
import re

logger = logging.getLogger('process')


@shared_task(ignore_result=True)
def dispatch_notification(notification_id, notification_key, object_id):
    try:
        notification = Notification.objects.get(pk=notification_id)
    except Notification.DoesNotExist:
        notification = False
    else:
        if not notification.viewed:
            if notification.user.email:
                if notification.user.profile.email_frequency == 'immediately':
                    notify_email.delay(notification.id)
            else:
                notify_comment_fb.delay(notification.id)


@shared_task(ignore_result=True)
def notify_email(notification_id):  # should be chained with send_email
    try:
        notification = Notification.objects.get(pk=notification_id)
    except Notification.DoesNotExist:
        notification = False
    else:
        context = Context({'notification': notification})
        html = get_template('email/email_notification.html').render(context)
        plaintext = get_template('email/email_notification.txt').render(context)
        subject = render_notification(notification, 'email', 'subject', mark_unread=True)
        from_email, to = 'apollo@rocketlistings.com', notification.user.email
        msg = EmailMultiAlternatives(subject, plaintext, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()


@shared_task(ignore_result=True)
def notify_comment_fb(notification_id):
    try:
        notification = Notification.objects.get(pk=notification_id)
    except Notification.DoesNotExist:
        notification = False
    else:
        if notification.content_type.model == 'comment':
            comment = notification.instance
            comments = comment.listing.comments.order_by('date_posted').exclude(scrapeid__isnull=False)

            if comments[0] == comment:  # If the notification is for the first listing comment
                if comment.private:
                    message = render_notification(notification, 'facebook-private', 'message', mark_unread=True)
                else:
                    message = render_notification(notification, 'facebook-public', 'message', mark_unread=True)
                logger.info("Facebook notification for listing {}".format(comment.listing.scrapeid))
                group_id = re.match(r'^[^_]+(?=_)', comment.listing.scrapeid).group(0)
                fbgroup = FBGroup.objects.get(graph_id=group_id)
                fb_graph.delay(str(comment.listing.scrapeid) + '/comments', fbgroup.scrape_user.id, message=message, method='post')


@shared_task(ignore_result=True)
def send_daily_digest(user_id):
    user = User.objects.get(pk=user_id)
    notifications = user.notifications.filter(viewed=False).all()
    if notifications:
        context = Context({'notifications': notifications})
        html = get_template('email/daily_digest.html').render(context)
        plaintext = get_template('email/daily_digest.txt').render(context)
        subject = 'Rocket daily digest: {} notifications!'.format(notifications.count())
        from_email, to = 'apollo@rocketlistings.com', user.email
        msg = EmailMultiAlternatives(subject, plaintext, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()


@shared_task(ignore_result=True)
def daily_digests():
    digesters = UserProfile.objects.filter(email_frequency='daily', user__notifications__viewed=False).distinct()
    logger.info("Send {} daily digests ".format(digesters.count()))
    for digester in digesters:
        send_daily_digest.delay(digester.user.id)
