from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user, Recording.objects.filter(text=instance).values('id')[0]['id'])


class Recording(models.Model):
    text = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    rec_date = models.DateTimeField('date recorded')
    voice_record = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    uuid = models.CharField(max_length=36)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.uuid = str(uuid.uuid4())
    instance.profile.save()
