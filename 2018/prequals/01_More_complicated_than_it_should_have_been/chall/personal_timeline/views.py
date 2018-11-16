from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from personal_timeline.auth import login, logout
from personal_timeline.forms import UserRegistrationForm
from personal_timeline.models import Event


def index(request):
    return render(request, 'index.html')


@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    return render(request, 'admin.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            resp = redirect('index')
            login(request, user, resp)
            return resp
    return render(request, 'register.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            resp = redirect('index')
            login(request, form.get_user(), resp)
            return resp
    return render(request, 'login.html')


def logout_user(request):
    resp = redirect('index')
    logout(request, resp)
    return resp


@login_required
def wall(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST' and 'message' in request.POST and username == request.user.username:
        Event.objects.create(author=request.user, message=request.POST['message'])
        return redirect('wall', request.user.username)

    return render(request, 'wall.html',
                  {'timeline_username': user.username, 'events': Event.objects.filter(author=user).order_by('posted')})
