from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('success')
            return HttpResponseRedirect(reverse("sambhash:chat"))
        else:
            return render(request, "sambhash/index.html", {
                'message': 'Invalid Credentials.'
            })
    else:
        return render(request, "sambhash/index.html")

def chat_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sambhash:index"))
    return render(request, "sambhash/chat.html")

def logout_view(request):
    logout(request)
    return render(request, "sambhash/logout.html")

def room_view(request, room_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sambhash:index"))
    return render(request, "sambhash/room.html", {
        'room_name': room_name
    })
