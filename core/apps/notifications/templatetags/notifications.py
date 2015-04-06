from django import template
from django.template import Template, Context, TemplateDoesNotExist
from django.conf import settings
from django.template.loader import get_template

register = template.Library()


@register.simple_tag
def render_notification(notif, media='default', field='message', mark_unread=False):

    try:
        config = settings.NOTIFICATIONS[notif.key][media][field]
    except KeyError:
        return ""

    if not notif.viewed and not mark_unread:
        notif.viewed = True
        notif.save()

    if mark_unread:
        notif.viewed = False
        notif.save()

    try:
        template = get_template(config)
    except TemplateDoesNotExist:
        template = Template(config)

    try:
        url = notif.get_absolute_url()
    except:
        notif.delete()
    else:
        if media == "facebook-private" or media == "facebook-public":
            notif.instance = notif.instance
            notif.instance.body = notif.instance.body.replace("'", "")
            notif.instance.body = notif.instance.body.replace('"', "")
            notif.instance.listing.user.first_name = notif.instance.listing.user.first_name.replace('"', "")
            notif.instance.listing.user.first_name = notif.instance.listing.user.first_name.replace("'", "")
            notif.save()

        return template.render(Context({
            'instance': notif.instance,
            'key': notif.key,
            'url': url,
            'date': notif.when()
        }))
