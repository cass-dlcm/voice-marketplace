from django import forms


class RecordingForm(forms.Form):
    audio_data = forms.FileField()
    text = forms.CharField(max_length=200)
