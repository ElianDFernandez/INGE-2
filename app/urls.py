from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('test/', views.test),

    path('', views.bienvenida, name='landing'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
]