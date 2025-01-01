from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Course, MentorshipRequest, MentorProfile

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('profile')  # Redirect to the profile page
    else:
        form = UserCreationForm()
    return render(request, 'stedcol/register.html', {'form': form})

# Login view
def login_view(request):  # Avoid naming the function "login" to prevent conflicts with django.contrib.auth.login
    return render(request, 'stedcol/login.html')

# Profile view
def profile(request):
    return render(request, 'stedcol/profile.html')

# Course List view
def course_list(request):
    courses = Course.objects.all()  # Fetch all courses
    return render(request, 'stedcol/course_list.html', {'courses': courses})

# Mentorship Request view
def mentorship_request(request, mentor_id):
    mentor = get_object_or_404(MentorProfile, id=mentor_id)  # Use get_object_or_404 for error handling
    student = request.user
    if request.method == 'POST':
        message = request.POST.get('message')
        MentorshipRequest.objects.create(student=student, mentor=mentor, message=message)
        return redirect('profile')  # Redirect to the profile page after submitting the request
    return render(request, 'stedcol/mentorship_request.html', {'mentor': mentor})

# Home view
def home(request):
    return render(request, 'stedcol/home.html')

# About view
def about(request):
    return render(request, 'stedcol/about.html')

# Contact view
def contact(request):
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'stedcol/contact.html')