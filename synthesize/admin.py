from django.contrib import admin
from .models import VoiceModel, SynthesizedSpeech


# Register your models here.
admin.site.register(VoiceModel)
admin.site.register(SynthesizedSpeech)
