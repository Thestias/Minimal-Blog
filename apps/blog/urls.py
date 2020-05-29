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
    path('', views.homepage, name='homepage'),
    path('new_blog', views.new_blog, name='new_blog'),
    path('write_blog', views.write_blog, name='write_blog'),
    path('<int:blog_id>', views.blog_id, name='blog_id'),
    path('edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about')
]
