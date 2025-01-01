from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from stedcol import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # User registration page
    path('register', views.register, name='register'),
    
    # User login page
    path('login/', views.login, name='login'),

    path('accounts/login/', LoginView.as_view(template_name='stedcol/login.html'), name='login'),

    #password reset
    path('accounts/', include('django.contrib.auth.urls')),
    
    # User profile page
    path('profile/', views.profile, name='profile'),
    
    # List of available courses
    path('courses/', views.course_list, name='course_list'),
    
    # Mentorship request page for a specific mentor
    path('mentorship_request/<int:mentor_id>/', views.mentorship_request, name='mentorship_request'),
]
