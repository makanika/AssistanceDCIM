from django.urls import path
from . import views
app_name = 'visitors'  # Namespace for the visitors app
urlpatterns = [
    path('', views.visitor_log_list, name='visitor_log_list'),
    path('add/', views.add_visitor_log, name='add_visitor_log'),
    path('edit/<int:pk>/', views.edit_visitor_log, name='edit_visitor_log'),
    path('delete/<int:pk>/', views.delete_visitor_log, name='delete_visitor_log'),
]
