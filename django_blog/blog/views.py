from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout

# Create your views here.

@login_required
def profile(request):
    return render(request, 'blog/profile.html', {'user': request.user})
# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Redirect to user profile
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})
