import re
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post
from .forms import PostForm

# VALIDA SI EL USUARIO ESTA AUTENTICADO
def user_not_authenticated(user):
    return not user.is_authenticated

# PANTALL POR DEFECTO QUE MUESTRA LOS POST
def home_view(request):
    posts = Post.objects.all()
    context = {'posts': posts, 'title': 'Home'}
    return render(request, 'Blog/home.html', context)

# CREAR UN NUEVO USUARIO
@user_passes_test(user_not_authenticated, login_url='home')
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        # expresión regular para verificar que el nombre de usuario
        # no contenga caracteres especiales
        check = re.compile("^[a-zA-Z]+$")
        
        # variables que reciben los datos ingresados en el form
        username = form.data['username']
        password = form.data['password1']
        repeatPassword = form.data['password2']
        
        # Validacion de contraseñas iguales y nombre de usuario
        print(f'data de formulario: {form.data}')
        if password !=  repeatPassword:
            messages.warning(request, "Las contraseñas no son iguales")
        elif check.match(username):
            print('username válido')
        else:
            messages.warning(request, "El nombre de usuario no es valido")
        
        # entra aqui si todo es válido
        if form.is_valid():
            print('ENTRAMOS AL FORMUALRIO VALIDO')
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(request, "Registro exitoso")
            login(request, new_user)
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form, 'title': 'Register'}
    return render(request, 'Blog/register.html', context)

# INICIAR SESION
@user_passes_test(user_not_authenticated, login_url='home')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            messages.success(request, "Inicio de sesión exitoso")
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    context = {'form': form, 'title': 'Login'}
    return render(request, 'Blog/login.html', context)

# REALIZA EL LOGOUT
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    context = {'title': 'Logout'}
    return render(request, 'Blog/logout.html', context)

# CREAR UNA NUEVO POST
@login_required(login_url='login')
def create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, "Creado exitosamente")
            return redirect('home')
    else:
        form = PostForm()
    context = {'form': form, 'title': 'Create'}
    return render(request, 'Blog/create.html', context)