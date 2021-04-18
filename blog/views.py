from django.shortcuts import render, redirect
from .forms import CustomUserCreation
from django.contrib import messages

# Create your views here.


def homepage(request):
    return render(request, 'homepage.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        register_form = CustomUserCreation(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
            return redirect('Login')
    else:
        register_form = CustomUserCreation()
    return render(request, 'login_register.html', context={'form': register_form})
