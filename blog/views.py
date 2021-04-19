from django.shortcuts import render, redirect
from .forms import CustomUserCreation
from .models import Blog
import markdown
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import Truncator

# Create your views here.


def homepage(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'homepage.html', {'page_obj': page_obj})


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

        synopsis = Truncator(file_data).chars(75).strip('#')
        blog_post = Blog(author=request.user, title=title,
                         body=md.convert(file_data), synopsis=synopsis)

        try:
            blog_post.full_clean()
        except ValidationError:
            pass
        else:
            messages.success(request, 'Blog uploaded')
            blog_post.save()

    return render(request, 'upload_blog.html')
