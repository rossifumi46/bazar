import json

from channels import Group

from .models import Request


def request_saved(message):
    request = Request.objects.latest('id')
    data = []
    data.append(request.real_id)
    print(data)
    Group('dashboard').send({
        'text': json.dumps(data)
    })


def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group('dashboard').add(message.reply_channel)
    print("hello")


def ws_disconnect(message):
    Group('dashboard').discard(message.reply_channel)
