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

    try:
        template = get_template(config)
    except TemplateDoesNotExist:
        template = Template(config)
    
    return template.render(Context({
        'instance': notif.instance,
        'key': notif.key,
        
    }))
