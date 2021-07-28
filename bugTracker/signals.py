import requests
from django.db.models.signals import post_save
from django.dispatch import receiver

from bugTracker.models.messaging import Notification
from bugTracker.models.task import Task



@shared_task(ignore_result=True)
def create_message_notifications(message_id):
    message = get_object_or_None(Message, id=message_id)
    if not message:
        return

    notification = Notification.objects.create(...)
    requests.get('http://localhost:3000/new/{}'.format(user_id))

@receiver(post_save, sender=Task, dispatch_uid='task_post_save')
def notification_message_post_save(sender, instance=None, created=None, **kwargs):
    if not created:
        return
    Notification
    create_message_notifications.delay(instance.id)