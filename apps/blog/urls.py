"""personal_blog_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('new_blog', views.NewBlog.as_view(), name='new_blog'),
    path('write_blog', views.WriteBlog.as_view(), name='write_blog'),
    path('<int:blog_id>', views.BlogId.as_view(), name='blog_id'),
    path('edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('about/', views.About.as_view(), name='about')
]
