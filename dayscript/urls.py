from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (Login/Logout)
    path('login/', auth_views.LoginView.as_view(template_name='diary/login.html'), name='login'),
    # Allow GET logout for convenience and redirect home
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Diary app
    path('', include('diary.urls')),
]