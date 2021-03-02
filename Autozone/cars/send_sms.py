from django.conf import settings
from django.http import HttpResponse
from twilio.rest import Client


def send_sms(request,recipient_number, user):
    message_to_broadcast = (f'{user.full_name} has shown interest in your car. you can contact them on {user.phone_number}')
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(to=recipient_number,
                           from_=settings.TWILIO_NUMBER,
                           body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)