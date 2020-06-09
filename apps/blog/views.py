from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import BlogPost
from datetime import datetime
from django.contrib import messages
from django.utils.decorators import method_decorator

from django.views import View

# Create your views here.


@method_decorator(login_required, name='dispatch')
class login_req(View):

    ''' A common Class For all Views that use login_redquired ! '''
    pass

class common_methods():

    ''' A common Class For all Views '''

    def get(self, request):
        ''' Simple GET method to keep code DRY '''
        return render(request, template_name=self.template_name)

    def http_method_not_allowed(self, request):
        return HttpResponse('<h1>403 - Forbidden</h1>')

##

class About(common_methods, View):

    template_name = 'about.html'


class Profile(login_req, common_methods, View):

    def get(self, request):
        b = BlogPost.objects.filter(user=request.user).values_list(
            'id', 'title', 'created_time')
        return render(request, template_name='profile.html', context={'blogs_by_user': b})


@require_http_methods(["GET", "POST"])
@login_required
def edit_blog(request, blog_id):
    #  WAY Easier to let this one be.
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


class BlogId(common_methods, View):

    def get(self, request, blog_id):
        blog_post = get_object_or_404(BlogPost, id=blog_id)
        context = {'markdown_text': blog_post.text_mark,
                   'blog_id': blog_post.id, 'blog_author': blog_post.user}
        return render(request, template_name='blog.html', context=context)


class Homepage(common_methods, View):

    def get(self, request):
        '''
        Lists all Blogs!
        '''
        dict_blogs = {}
        blog_posts = BlogPost.objects.all().order_by(
            '-created_time')  # -created_time  descending order
        for blogObject in blog_posts:
            dict_blogs[blogObject.id] = blogObject.title

        return render(request, 'homepage.html', context={'dict_blogs': blog_posts})


class NewBlog(common_methods, login_req, View):

    template_name = 'new_blog.html'

    def post(self, request):
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


class WriteBlog(common_methods, login_req, View):

    template_name = 'write_blog.html'

    def post(self, request):
        data = request.POST
        dt_string = get_timestamp()
        b = BlogPost(title=data['title'],
                     text_mark=data['markdownText'], created_time=dt_string, user=request.user)
        b.save()
        messages.success(request, 'Blog Created!')
        return redirect('homepage')


def get_timestamp():
    ''' Used to add a timestamp when creating a blog'''

    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M")

    return dt_string
