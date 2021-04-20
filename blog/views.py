from django.shortcuts import render, redirect
from .forms import CustomUserCreation
from .models import Blog, Category
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import Truncator
from django.db.models import Q


# Create your views here.


def homepage(request):
    blogs = Blog.objects.all().prefetch_related(
        'categories').order_by("id").reverse()
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


def profile(request, user_id):

    if request.method == 'POST' and user_id == request.user.id:
        blog_to_delete = int(request.POST.get('delete'))
        Blog.objects.get(id=blog_to_delete).delete()
        messages.success(request, 'Blog deleted')

    blogs = Blog.objects.filter(author=user_id).order_by("id").reverse()
    paginator = Paginator(blogs, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page_obj': page_obj, 'requested_user': User.objects.get(id=user_id)})


def upload_blog(request):
    available_categories = Category.objects.all()

    if request.method == 'POST':
        md = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()])

        '''
        This section reads the file, the read() method returns a raw string that next its converted
        to UTF-8 encoding
        '''
        uploaded_file = request.FILES['file']
        file_data = request.FILES['file'].read().decode('utf-8')

        '''
        Creating some variables for the Blog record creation and creating the blog
        '''
        title = uploaded_file.name.replace('.md', '')
        synopsis = Truncator(file_data).chars(100).strip('#')
        blog_post = Blog(author=request.user, title=title, body=md.convert(file_data), synopsis=synopsis)

        '''
        This section loops trough the categories in the request.POST and if they dont exist it saves them,
        then wheter they exist or have been just created it saves the id of them in categories_to_add.
        '''
        categories_to_add = []
        for category in request.POST.getlist('category'):
            category = category.capitalize()
            check_category = Category.objects.filter(name=category).exists()
            if check_category:
                categories_to_add.append(Category.objects.get(name=category).id)
            else:
                if len(category) != 0:
                    Category(name=category).save()
                    categories_to_add.append(Category.objects.get(name=category).id)

        try:
            blog_post.full_clean()
        except ValidationError:
            pass
        else:
            blog_post.save()
            # Adding the categories to the post
            blog_post.categories.add(*categories_to_add)
            messages.success(request, 'Blog uploaded')

    return render(request, 'upload_blog.html', {'categories': available_categories})


def blog(request, blog_id):
    blog_data = Blog.objects.get(id=blog_id)
    return render(request, 'blog.html', {'blog': blog_data})


def search(request):
    query_data = request.POST.getlist('search')

    for query in query_data:
        lookup = Q(title__icontains=query)

    '''
    In order, this part does this:
    1- Filters all blogs for the lookup
    2- Discards the repeated
    3- Prefetchs the related categories
    4- Orders the blog's by ID
    5- It reverses the order
    '''
    results = Blog.objects.filter(lookup).distinct().prefetch_related(
        'categories').order_by("id").reverse()

    paginator = Paginator(results, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'homepage.html', {'page_obj': page_obj, 'header': 'Search results.'})
