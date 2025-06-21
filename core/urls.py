from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView # For redirecting root to dashboard
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')), # Include URLs from the dashboard app
    path('auth/', include('authentication.urls')), # Include URLs from the authentication app
    path('visitors/', include('visitors.urls')), # Include URLs from the visitors app
    path('', RedirectView.as_view(url='/dashboard/', permanent=True)), # Redirect root to dashboard
]
