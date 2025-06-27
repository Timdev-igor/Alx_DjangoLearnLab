from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.
def login_view(request):
    """
    Handles user login using the custom authentication backend.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            return render(request, 'vagus/login.html', {'error': 'Invalid email or password'})
    return render(request, 'vagus/login.html')
#perms
@login_required
def home_view(request):
    return render(request, 'vagus/home.html')  # This will use 'templates/home.html'

@login_required
@permission_required('vagus.can_view', raise_exception=True)
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'vagus/post_detail.html', {'post': post})

@login_required
@permission_required('vagus.can_create', raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:  # Ensure fields are not empty
            Post.objects.create(title=title, content=content)
            return redirect('post_list')  # Redirect to post list after creation

    return render(request, 'vagus/create_post.html')

@login_required
@permission_required('vagus.can_edit', raise_exception=True)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'vagus/edit_post.html', {'post': post})

@login_required
@permission_required('vagus.can_delete', raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post_list')

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'vagus/post_list.html', {'posts': posts})