from django import forms


class SpeechForm(forms.Form):
    speech_text = forms.CharField(label='Text to speak', max_length=10000)
