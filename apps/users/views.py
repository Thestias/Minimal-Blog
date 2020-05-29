from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.views.decorators.http import require_http_methods
# Create your views here.


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
            return redirect('login')
    else:
        register_form = RegisterForm()
        return render(request, template_name='register.html', context={'register_form': register_form})
