from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
import create_voice.views as cViews
import synthesize.views as sViews
import marketplace.views as mViews


"""voiceMarketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from voiceMarketplace import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_voice/', include('create_voice.urls')),
    path('create_voice/index', cViews.IndexView.as_view(), name='create_voice/index'),
    path('create_voice/record', cViews.RecordView.as_view(), name='create_voice/record'),
    path('create_voice/prompt', cViews.PromptView.as_view(), name='create_voice/prompt'),
    path('create_voice/upload', cViews.RecieveRecordingView.as_view(), name='create_voice/upload'),
    path('syntheisze/', include('synthesize.urls')),
    path('synthesize/index', sViews.IndexView.as_view(), name='synthesize/index'),
    path('synthesize/new', sViews.get_text, name='synthesize/new'),
    path('synthesize/output', sViews.OutputView.as_view(), name='synthesize/output'),
    path('marketplace/', include('marketplace.urls')),
    path('marketplace/index', mViews.IndexView.as_view(), name='marketplace/index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name='accounts/register'),
    path('duo/',  include('duo_auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
