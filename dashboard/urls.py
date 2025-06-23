from django.urls import path
from . import views
app_name = 'dashboard'  # Namespace for the dashboard app
urlpatterns = [
    path('', views.dashboard_view, name='index'), # The main dashboard page
    path('generate_pdf/', views.generate_pdf_report, name='generate_pdf_report'),
]
