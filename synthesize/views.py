import requests
import yaml
from django.core.files import File
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
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
            synthesized_speech.user = request.user
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
            synthesized_speech.save()
            if response.status_code == 200:
                with open("static/out.wav", 'wb') as audio:
                    audio.write(response.content)
                    print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
                synthesized_speech.audio.save('synthesized/user_{0}/{1}.wav'.format(synthesized_speech.user, synthesized_speech.id), File(open('static/out.wav', 'rb')))
                synthesized_speech.save()
            else:
                print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            # redirect to a new URL:
            return HttpResponseRedirect('output')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SpeechForm(user=request.user.username)

    return render(request, 'synthesize/new.html', {'form': form})


class OutputView(LoginRequiredMixin, generic.ListView):
    template_name = 'synthesize/output.html'
    context_object_name = 'synthesized_speech'

    def get_queryset(self):
        return SynthesizedSpeech.objects.filter(user=self.request.user)[0]


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'synthesize/index.html'
    context_object_name = 'list_of_synthesized_speech'

    def get_queryset(self):
        return SynthesizedSpeech.objects.filter(user=self.request.user)


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = SynthesizedSpeech
    template_name = 'synthesize/detail.html'
    context_object_name = 'synthesized_speech'

    def get_queryset(self):
        return SynthesizedSpeech.objects.filter(user=self.request.user)


@login_required
def delete_synthesized_speech(request, pk=None):
    object = SynthesizedSpeech.objects.get(id=pk)
    object.delete()
    return render(request, 'synthesize/index.html')
