from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('', views.index, name='index'),  # Serve the HTML template
]
