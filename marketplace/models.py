from django.db import models
from django.conf import settings
from synthesize.models import VoiceModel


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_credits = models.IntegerField()

    def __str__(self):
        return self.user.username


class Voice(models.Model):
    voice_model = models.OneToOneField(VoiceModel, on_delete=models.CASCADE)
    sample_audio = models.FileField()
    cost = models.IntegerField()

    def __str__(self):
        return self.voice_model.name
