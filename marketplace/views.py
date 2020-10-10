from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Voice


# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'marketplace/index.html'
    context_object_name = 'list_of_voices'

    def get_queryset(self):
        return Voice.objects.filter()
