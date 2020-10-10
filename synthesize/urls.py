from django.urls import path
from . import views

app_name = 'synthesize'
urlpatterns = [
    path('new', views.get_text, name='new'),
    path('output', views.OutputView.as_view(), name='output'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/delete', views.delete_synthesized_speech, name='delete'),
]
