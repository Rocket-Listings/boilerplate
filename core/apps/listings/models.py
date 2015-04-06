from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete

# Create your models here.

from signal_receivers import *  # noqa
receiver(post_save, sender=User)(send_welcome_email)