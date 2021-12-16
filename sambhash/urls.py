from django.urls import path

from . import views

app_name = "sambhash"
urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat_view, name='chat'),
    path("logout", views.logout_view, name="logout"),
    path("chatroom/<str:room_name>/", views.room_view, name="room")
]
