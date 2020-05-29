from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import BlogPost
from datetime import datetime
from django.contrib import messages

# Create your views here.


@require_http_methods(['GET'])
def about(request):
    return render(request, template_name='about.html')


@require_http_methods(['GET', 'POST'])
@login_required
def profile(request):
    b = BlogPost.objects.filter(user=request.user).values_list(
        'id', 'title', 'created_time')
    return render(request, template_name='profile.html', context={'blogs_by_user': b})


@require_http_methods(["GET", "POST"])
@login_required
def edit_blog(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    if request.method == 'POST':
        data = request.POST
        blog_post.title = data.get('title')
        blog_post.text_mark = data.get('markdownText')
        blog_post.save()
        messages.success(request, 'Blog Edited!')
        return redirect('homepage')
    else:
        context = {'markdown_text': blog_post.text_mark,
                   'blog_title': blog_post.title}
        return render(request, template_name='write_blog.html', context=context)


@require_http_methods(['GET'])
def blog_id(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    context = {'markdown_text': blog_post.text_mark,
               'blog_id': blog_post.id, 'blog_author': blog_post.user}
    return render(request, template_name='blog.html', context=context)


@require_http_methods(['GET'])
def homepage(request):
    dict_blogs = {}
    blog_posts = BlogPost.objects.all()
    for blogObject in blog_posts:
        dict_blogs[blogObject.id] = blogObject.title

    return render(request, 'homepage.html', context={'dict_blogs': blog_posts})


@require_http_methods(['GET', 'POST'])
@login_required
def new_blog(request):
    if request.method == 'POST':
        f = (request.FILES['file'])
        post_title = request.POST['title']
        file_read = f.read()
        dt_string = get_timestamp()
        file_read_String = file_read.decode('utf-8')
        b = BlogPost(title=post_title, text_mark=file_read_String,
                     created_time=dt_string, user=request.user)
        b.save()
        messages.success(request, 'Blog Uploaded!')
        return redirect('homepage')
    return render(request, template_name='new_blog.html')


@require_http_methods(['GET', 'POST'])
@login_required
def write_blog(request):
    if request.method == 'POST':
        data = request.POST
        dt_string = get_timestamp()
        b = BlogPost(title=data['title'],
                     text_mark=data['markdownText'], created_time=dt_string, user=request.user)
        b.save()
        messages.success(request, 'Blog Created!')
        return redirect('homepage')
    return render(request, template_name='write_blog.html')


def get_timestamp():
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M")

    return dt_string
