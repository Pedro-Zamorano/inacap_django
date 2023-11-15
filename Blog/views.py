from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post
from .forms import PostForm

def user_not_authenticated(user):
    return not user.is_authenticated

def home_view(request):
    posts = Post.objects.all()
    context = {'posts': posts, 'title': 'Home'}
    return render(request, 'Blog/home.html', context)

@user_passes_test(user_not_authenticated, login_url='home')
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            login(request, new_user)
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form, 'title': 'Register'}
    return render(request, 'Blog/register.html', context)

@user_passes_test(user_not_authenticated, login_url='home')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    context = {'form': form, 'title': 'Login'}
    return render(request, 'Blog/login.html', context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    context = {'title': 'Logout'}
    return render(request, 'Blog/logout.html', context)

@login_required(login_url='login')
def create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {'form': form, 'title': 'Create'}
    return render(request, 'Blog/create.html', context)