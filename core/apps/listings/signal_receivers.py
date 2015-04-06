
def send_welcome_email(sender, instance, created, **kwargs):
	if created:
		from listings import tasks
		print "send signup email receiver"
		tasks.signup_email.delay(instance.id)