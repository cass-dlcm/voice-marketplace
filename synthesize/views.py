import os
import requests
import yaml
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import SynthesizedSpeech
from .forms import SpeechForm


@login_required
def get_text(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SpeechForm(request.POST, user=request.user.username)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            synthesized_speech = SynthesizedSpeech()
            synthesized_speech.text = form.cleaned_data['speech_text']
            synthesized_speech.voice_model = form.cleaned_data['voice_model']

            headers = {
                'Ocp-Apim-Subscription-Key': yaml.load(open('/code/secrets.yaml', 'r'), Loader=yaml.FullLoader)['Ocp_Apim_Subscription_Key'],
            }
            access_token = str(requests.post('https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken', headers=headers).text)
            constructed_url = "https://eastus.voice.speech.microsoft.com/cognitiveservices/v1?deploymentId=0982d199-b2b3-4480-96c8-d11372f35c54"
            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
                'User-Agent': 'speech_marketplace'
            }
            data = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US"><voice name="' + str(synthesized_speech.voice_model.name) + '">' + str(synthesized_speech.text) + '</voice></speak>'
            response = requests.post(constructed_url, headers=headers, data=data)
            if response.status_code == 200:
                if os.path.exists('static/output.wav'):
                    os.remove('static/output.wav')
                with open('static/output.wav', 'wb') as audio:
                    audio.write(response.content)
                    synthesized_speech.save()
                    print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
                    synthesized_speech.audio = audio
                    synthesized_speech.save()
            else:
                print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            # redirect to a new URL:
            return HttpResponseRedirect('output.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SpeechForm(user=request.user.username)

    return render(request, 'synthesize/new.html', {'form': form})


@login_required
def output(request):
    return render(request, 'synthesize/output.html')
