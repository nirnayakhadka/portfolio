from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about_view, name='about'),  # Remove duplicate
    path('contact/', views.contact_view, name='contact'),
    path('projects/', views.projects_view, name='projects'),
    path('contact/', views.contact_view, name='contact'),
    path('projects/<slug:slug>/', views.project_detail_view, name='project_detail'),
    path('api/projects/', views.projects_api, name='projects_api'),

    
]