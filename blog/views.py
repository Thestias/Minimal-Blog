from django.shortcuts import render, redirect
from .forms import CustomUserCreation
from .models import Blog
import markdown
from django.core.exceptions import ValidationError
from django.contrib import messages

# Create your views here.


def homepage(request):
    return render(request, 'homepage.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('Profile')

    if request.method == 'POST':
        register_form = CustomUserCreation(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
            return redirect('Login')
    else:
        register_form = CustomUserCreation()
    return render(request, 'login_register.html', context={'form': register_form, 'action': 'Register'})


def profile(request):
    return render(request, 'profile.html')


def upload_blog(request):
    if request.method == 'POST':
        md = markdown.Markdown()

        uploaded_file = request.FILES['file']
        title = uploaded_file.name.replace('.md', '')
        file_data = request.FILES['file'].read().decode(
            'utf-8')  # read() returns a raw string

        blog_post = Blog(author=request.user, title=title,
                         body=md.convert(file_data))

        try:
            blog_post.full_clean()
        except ValidationError:
            pass
        else:
            messages.success(request, 'Blog uploaded')
            blog_post.save()

    return render(request, 'upload_blog.html')
