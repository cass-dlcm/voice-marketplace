from django import forms
from .models import VoiceModel


def get_voice_models(*args, **kwargs):
    VoiceModel.objects.filter(subscribers__username__startswith=kwargs.pop('user'))


class SpeechForm(forms.Form):
    speech_text = forms.CharField(label='Text to speak', max_length=10000)
    voice_model = forms.ModelChoiceField(queryset=VoiceModel.objects)

    def __init__(self, *args, **kwargs):
        self.voice_model = forms.ModelChoiceField(queryset=VoiceModel.objects.filter(subscribers__username__startswith=kwargs.pop('user')))
        super(SpeechForm, self).__init__(*args, **kwargs)
