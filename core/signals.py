from django.db.models.signals import post_save
from django.dispatch import receiver

from channels import Channel

from .models import Request


@receiver(post_save, sender=Request)
def lot_save_handler(sender, **kwargs):
    Channel('request-saved').send({
        'request': sender.id
    })