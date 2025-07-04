

# Create your views here.
#create views LOG 6

from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo, Category , BlogPost
from .forms import PhotoForm

def home(request):
    category_id = request.GET.get('category')
    photos = Photo.objects.all()
    if category_id:
        photos = photos.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'denver_gallery/home.html', {'photos': photos, 'categories': categories})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'denver_gallery/photo_detail.html', {'photo': photo})

def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'denver_gallery/upload.html', {'form': form})

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'denver_blog/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'denver_blog/blog_detail.html', {'post': post})



