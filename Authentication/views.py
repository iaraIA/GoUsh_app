from django.shortcuts import render, redirect
from .forms import FormularioCargarUsuario
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def registerPage(request):
    form = FormularioCargarUsuario
    if request.method == 'POST':
        form = FormularioCargarUsuario(data=request.POST)
        if form.is_valid():
            form.save()

            return redirect("Login")
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            
    context = {'form': form}
    return render(request, "Authentication/register.html", context)

def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.info(request, 'Nombre de usuario o contraseña incorrectos')

    context = {}
    return render(request, "Authentication/login.html", context)

def logoutUser(request):

    logout(request)
    return redirect('Login')