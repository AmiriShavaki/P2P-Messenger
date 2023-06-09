from django.contrib import admin
from django.urls import path
from chat.views import GetMessages, SendMessage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messages/', GetMessages.as_view()),
    path('send/', SendMessage.as_view())
]