from . import views
from django.urls import path

app_name = "chatbot"

urlpatterns = [
    path('', views.chatbot_view, name='chatbot_test')
]