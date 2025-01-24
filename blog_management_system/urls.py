"""
URL configuration for blog_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('create/', views.create_blog, name='create_blog'),  # Create new blog
    path('blogs/<int:id>/', views.blog_detail, name='blog_detail'), # Blog detail page
    path('login/', views.user_login, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('blogs/<int:id>/like/', views.like_blog, name='like_blog'),
    path('register/', views.register, name='register'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('blogs/edit/<int:id>/', views.edit_blog, name='edit_blog'),  # Edit a blog
    path('blogs/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),  # Delete a blog
    path('users/', views.view_all_users, name='view_all_users'),  # View all users
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
