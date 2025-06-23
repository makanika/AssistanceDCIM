from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Import Django's built-in auth views
app_name = 'authentication'  # Namespace for the authentication app

urlpatterns = [
    path('register/', views.register_view, name='auth_register'),
    path('login/', views.login_view, name='auth_login'), # Use custom login view to show messages
    path('logout/', views.logout_view, name='auth_logout'), # Use custom logout view to show messages
    # You can also use Django's built-in views directly for password reset etc.
    # path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
]
