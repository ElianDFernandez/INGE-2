from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Desarrollo
    path('test/', views.test),
    path('manifest.webmanifest', views.pwa_manifest, name='pwa_manifest'),
    path('sw.js', views.pwa_service_worker, name='pwa_service_worker'),

    # Autenticación
    path('', views.bienvenida, name='landing'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('registro/', views.registro, name='registro'),

    # Recuperación de contraseña (Utilizacion de auth_views que implementa Django)
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='app/password_reset_form.html',
        email_template_name='app/password_reset_email.html',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Vistas protegidas
    path('home/', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
]