from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views import generic
from .models import Recording, Profile
import random
from .forms import RecordingForm
import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError


# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'create_voice/index.html'
    context_object_name = 'list_of_recordings'

    def get_queryset(self):
        return Recording.objects.filter(
            rec_date__lte=timezone.now()
        ).filter(user=self.request.user.username).order_by('-rec_date')


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Recording
    template_name = 'create_voice/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Recording.objects.filter(rec_date__lte=timezone.now()).filter(user=self.request.user.username)


class RecordView(LoginRequiredMixin, generic.ListView):
    model = Recording
    text = random.choice(open('clips.csv').read().splitlines())
    template_name = 'create_voice/record.html'
    context_object_name = 'text'

    def get_queryset(self):
        return self.text


class PromptView(generic.ListView):
    template_name = 'create_voice/prompt.html'
    context_object_name = 'text'

    def get_queryset(self):
        return random.choice(open('clips.csv').read().splitlines())


class RecieveRecordingView(generic.ListView):
    model = Recording

    def post(self, request):
        form = RecordingForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            recording = Recording()
            recording.text = form.cleaned_data['text']
            recording.rec_date = timezone.now()
            recording.voice_record = form.files['audio_data']
            recording.user = request.user.username
            recording.save()
            if (not os.path.exists('media/' + recording.user)):
                os.mkdir('media/' + recording.user)
            os.rename(recording.voice_record.path, os.path.join(Path(__file__).resolve().parent.parent, 'media') + '\\' + recording.user + '\\' + str(recording.id) + '.wav')
            recording.voice_record = os.path.join(Path(__file__).resolve().parent.parent, 'media') + '\\' + recording.user + '\\' + str(recording.id) + '.wav'
            recording.save()
            connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)
            container_name = recording.user + Profile.objects.filter(user=request.user)[0].uuid
            container_client = blob_service_client.get_container_client(container_name)
            try:
                container_client.create_container()
            except ResourceExistsError:
                pass
            upload_file_path = os.path.join(Path(__file__).resolve().parent.parent, 'media') + '\\' + recording.user + '\\' + str(recording.id) + '.wav'
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=recording.voice_record.name)
            with open(upload_file_path, "rb") as data:
                blob_client.upload_blob(data)
            return HttpResponse('Ok')
        else:
            return HttpResponseBadRequest('')
