from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    # Add other URLs as needed later
     path('about/', views.about, name='about'),
]
