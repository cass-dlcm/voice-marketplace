from django.urls import path
from . import views

app_name = 'synthesize'
urlpatterns = [
    path('', views.get_text, name='index'),
    path('<int:pk>/', views.output, name='output'),
]
