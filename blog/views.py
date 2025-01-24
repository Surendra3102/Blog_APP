from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Blog

def view_all_blogs(request):
    blogs = Blog.objects.all()  # Get all blogs
    return render(request, 'subscriber/view_all_blogs.html', {'blogs': blogs})

def home(request):
    search_query = request.GET.get('search', '')
    if search_query:
        blogs = Blog.objects.filter(title__icontains=search_query)
    else:
        blogs = Blog.objects.all()  # Fetch all blogs if no search query
    return render(request, 'blog/home.html', {'blogs': blogs})

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image=request.FILES.get('image')
        Blog.objects.create(title=title, content=content, author=request.user, image=image)
        return redirect('home')
    return render(request, 'blog/create_blog.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # Redirect to home after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)  # Fetch the blog by ID
    comments = blog.comments.all()  # Get all comments related to the blog
    likes_count = blog.likes.count()  # Get the count of likes

    if request.method == 'POST':
        # Handle comment submission
        content = request.POST.get('content')
        if content:
            Comment.objects.create(blog=blog, author=request.user, content=content)
            return redirect('blog_detail', id=blog.id)  # Redirect to the same blog detail page

    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'likes_count': likes_count,
    })


def like_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.user.is_authenticated:
        if request.user in blog.likes.all():
            blog.likes.remove(request.user)  # Unlike
        else:
            blog.likes.add(request.user)  # Like
    return redirect('blog_detail', id=blog.id)

@login_required
def edit_blog(request, id):
    blog = get_object_or_404(Blog, id=id)  # Ensure the user is the author
    if request.user !=blog.author and not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit this blog.")
        return redirect('blog_detail', id=blog.id)
    
    if request.method == 'POST':
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        blog.save()
        return redirect('blog_detail', id=blog.id)  # Redirect to the list of all blogs
    return render(request, 'blog/edit_blog.html', {'blog': blog})

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.user != blog.author and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this blog.")
        return redirect('blog_detail', id=blog.id)

    blog.delete()
    messages.success(request, "Blog deleted successfully.")
    return redirect('home')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate the form data
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'blog/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'blog/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'blog/register.html')

        # Create the user
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'blog/register.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Access restricted to administrators.")
        return redirect('home')

    users = User.objects.all()
    blogs = Blog.objects.all()
    comments = Comment.objects.all()
    return render(request, 'admin/dashboard.html', {
        'users': users,
        'blogs': blogs,
        'comments': comments,
    })

from django.contrib.auth.models import User

@login_required
def view_all_users(request):
    users = User.objects.all()  # Get all users
    return render(request, 'subscriber/view_all_users.html', {'users': users})

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete users.")
        return redirect('home')

    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, "Cannot delete another superuser.")
    else:
        user.delete()
        messages.success(request, "User deleted successfully.")

    return redirect('admin_dashboard')
