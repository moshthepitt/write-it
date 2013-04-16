from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from popit.models import ApiInstance
from contactos.models import Contact


class MessageManager(models.Manager):
    def create(self, **kwargs):
        if 'contacts' in kwargs:
            contacts = kwargs['contacts']
            del kwargs['contacts']
        else:
            raise TypeError('A message needs contacts to be sent')
        message = super(MessageManager, self).create(**kwargs)
        for contact in contacts:
            outbound_message = OutboundMessage.objects.create(contact=contact, message=message)
        return message

class Message(models.Model):
    """Message: Class that contain the info for a model, despite of the input and the output channels. Subject and content are mandatory fields"""
    subject = models.CharField(max_length=512)
    content = models.TextField()
    instance = models.ForeignKey('Instance')

    objects = MessageManager()

		
class Instance(models.Model):
    """Instance: Entity that groups messages and people for usability purposes. E.g. 'Candidates running for president'"""
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    api_instance = models.ForeignKey(ApiInstance)

    @models.permalink
    def get_absolute_url(self):
        return ('instance.views.details', self.slug)

class OutboundMessage(models.Model):
    """docstring for OutboundMessage: This class is the message delivery unit. The OutboundMessage is the one that will be tracked in order 
    to know the actual status of the message"""
    contact = models.ForeignKey(Contact)
    message = models.ForeignKey(Message)
		
