from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import BlogPost
from datetime import datetime
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.template.loader import get_template, TemplateDoesNotExist
from django.views import View
from django.http import Http404
# Create your views here.


@method_decorator(login_required, name='dispatch')
class login_req(View):

    ''' A common Class For all Views that use login_redquired ! '''
    pass

class common_methods():

    ''' A common Class For all Views '''

    context = {}

    def get(self, request, blog_id=None):
        ''' Simple GET method to keep code DRY '''
        self.blog_id = blog_id  # Just to satisfy BlogId View
        self.request = request  # Just to satisfy Profile View
        try:
            get_template(self.template_name)

        except TemplateDoesNotExist:
            # MSG Shown only when not in production.
            raise Http404('404 - TemplateDoesNotExist')

        except Exception as e:
            return HttpResponse('<h1>500 - Internal Server Error.</h1>', status=500)

        else:
            print(self.context, type(self.context))
            return render(request, template_name=self.template_name, context=self.context)

    def http_method_not_allowed(self, request):
        return HttpResponse('<h1>403 - Forbidden</h1>')

##

class About(common_methods, View):

    template_name = 'about.html'


class Profile(login_req, common_methods, View):

    template_name = 'profile.html'

    @property
    def get_user_blogs(self):
        b = BlogPost.objects.filter(user=self.request.user).values_list(
            'id', 'title', 'created_time')

        return {'blogs_by_user': b}

    context = get_user_blogs


@ require_http_methods(["GET", "POST"])
@ login_required
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

    template_name = 'blog.html'

    @property
    def get_blog_content(self):
        blog_post = get_object_or_404(BlogPost, id=self.blog_id)
        blog_content = {'markdown_text': blog_post.text_mark,
                        'blog_id': blog_post.id, 'blog_author': blog_post.user}
        return blog_content

    context = get_blog_content


class Homepage(common_methods, View):

    template_name = 'homepage.html'

    @property
    def get_all_blog_list(self):
        blog_posts = BlogPost.objects.all().order_by(
            '-created_time')  # -created_time  descending order
        return {'dict_blogs': blog_posts}

    context = get_all_blog_list


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
