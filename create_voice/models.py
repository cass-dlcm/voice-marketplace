from django.db import models


# Create your models here.
class Recording(models.Model):
    voice_record = models.FileField()
    text = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    rec_date = models.DateTimeField('date recorded')

    def __str__(self):
        return self.text
