
def send_welcome_email(sender, instance, created, **kwargs):
	if created:
		from core import tasks
		tasks.signup_email.delay(instance.id)