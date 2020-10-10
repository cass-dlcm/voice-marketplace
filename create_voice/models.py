from django.db import models
from django.conf import settings


# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user_value, Recording.objects.filter(text=instance).values('id')[0]['id'])


class Recording(models.Model):
    text = models.CharField(max_length=200)
    user_value = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rec_date = models.DateTimeField('date recorded')
    voice_record = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return self.text
