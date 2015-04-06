from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template import Context

@shared_task(ignore_result=True)
def signup_email(user_id):  
    user = User.objects.get(pk=user_id)
    context = Context({'user': user})
    html = get_template('email/email_notification.html').render(context)
    plaintext = get_template('email/email_notification.txt').render(context)
    subject = render_notification(notification, 'email', 'subject', mark_unread=True)
    from_email, to = 'apollo@rocketlistings.com', notification.user.email
    msg = EmailMultiAlternatives(subject, plaintext, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()