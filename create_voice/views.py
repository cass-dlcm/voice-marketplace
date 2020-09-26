from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import generic
from .models import Recording
import random
from datetime import datetime


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
    recording = Recording()
    recording.text = random.choice(open('clips.csv').read().splitlines())
    recording.rec_date = timezone.now()
    template_name = 'create_voice/record.html'
    context_object_name = 'recording'

    def get_queryset(self):
        self.recording.user = self.request.user.username
        return self.recording


class PromptView(generic.ListView):
    template_name = 'create_voice/prompt.html'
    context_object_name = 'text'

    def get_queryset(self):
        return random.choice(open('clips.csv').read().splitlines())
