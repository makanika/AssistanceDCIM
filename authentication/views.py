# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

def register_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created and logged in successfully!")
            return redirect('dashboard:index') # Redirect to dashboard after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("request: {}".format(request.POST))

            if request.POST.get('next') and request.POST.get('next') != '':
                return redirect(request.POST.get('next'))
            else:
                messages.success(request, "Logged in successfully!")
                return redirect('dashboard:index') # Redirect to dashboard after successful login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    """
    Handles user logout.
    """
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Logged out successfully.")
        return redirect('authentication:auth_login') # Redirect to login page after logout
    return redirect('dashboard') # If not POST, just redirect to dashboard or login
