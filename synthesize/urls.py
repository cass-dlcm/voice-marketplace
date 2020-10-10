from django.urls import path
from . import views

app_name = 'synthesize'
urlpatterns = [
    path('new', views.get_text, name='new'),
    path('<int:pk>/', views.output, name='output'),
]
