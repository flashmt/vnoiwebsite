from django import template
from forum.models import Topic

register = template.Library()

@register.filter(name="lastest_thread")
def lastest_thread(topic):
    try:
        topic = Topic.objects.get(topic=topic)
    except Topic.DoesNotExist:
        #TODO: Handle this exception
        pass
    #TODO change this stupid query method
    return topic