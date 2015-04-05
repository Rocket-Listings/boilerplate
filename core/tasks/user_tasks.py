from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

@shared_task(ignore_result=True)
def signup_email(user_id):  # should be chained with send_email
    user = User.objects.get(pk=user_id)
    from_email, to = 'apollo@rocketlistings.com', user.email
    subject = "Thanks for joining Hidden Talent!"
    body = "You're going to have an an amazing time."
    msg = EmailMultiAlternatives(subject, body, from_email, [to])
    msg.send()