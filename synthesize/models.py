from django.db import models
from django.conf import settings


# Create your models here.
class VoiceModel(models.Model):
    endpoint = models.URLField()
    name = models.CharField(max_length=200)
    creator = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='creator')

    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    return 'synthesized/user_{0}/{1}.wav'.format(instance.user, SynthesizedSpeech.objects.filter(text=instance).values('id')[0]['id'])


class SynthesizedSpeech(models.Model):
    audio = models.FileField(upload_to=user_directory_path)
    text = models.CharField(max_length=200)
    voice_model = models.ForeignKey(VoiceModel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
