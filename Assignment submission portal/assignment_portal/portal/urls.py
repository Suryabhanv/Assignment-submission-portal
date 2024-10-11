# portal/urls.py
from django.urls import path
from .views import get_assignment
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('upload/', views.upload_assignment, name='upload_assignment'),
    path('admins/', views.list_admins, name='list_admins'),
    path('assignments/<int:admin_id>/', views.view_assignments, name='view_assignments'),
    path('api/assignments/<int:assignment_id>/', get_assignment, name='get_assignment'),
    path('assignments/<int:assignment_id>/accept/', views.accept_assignment, name='accept_assignment'),
    path('assignments/<int:assignment_id>/reject/', views.reject_assignment, name='reject_assignment'),
    path('upload_form/', views.upload_assignment_form, name='upload_assignment_form'),
    path('api/upload/', views.upload_assignment, name='upload_assignment'),  # Your API endpoint
]
