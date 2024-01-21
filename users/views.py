from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.messages import constants
from django.contrib import messages

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)

    if not user:
        messages.add_message(request, constants.ERROR, "Username or password incorrect")
        return redirect('/users/login')

    auth.login(request, user)
    messages.add_message(request, constants.SUCCESS, "Logged!")
    return redirect('/flashcard/new_flashcard')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, "PASSWORDS MISMATCH")
        return redirect('/users/register')

    user = User.objects.filter(username=username)

    if user.exists():
        messages.add_message(request, constants.ERROR, "USER already exists")
        return redirect('/users/login')

    try:
        User.objects.create_user(
            username=username,
            password=password
        )
        return redirect('/users/login')
    except:
        messages.add_message(request, constants.ERROR, "INTERNAL SERVER ERROR")
        return redirect('/users/register')