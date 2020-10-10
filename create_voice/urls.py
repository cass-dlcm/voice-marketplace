from django.urls import path
from . import views

app_name = 'create_voice'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/delete', views.delete_recording, name='delete'),
    path('record/', views.RecordView.as_view(), name='record'),
    path('prompt/', views.PromptView.as_view(), name='prompt'),
    path('upload/', views.RecieveRecordingView.as_view(), name='upload')
]
