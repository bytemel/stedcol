from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    objects = CustomUserManager()  # Attach the custom manager

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('graduate', 'Graduate'),
        ('mentor', 'Mentor'),
        ('instructor', 'Instructor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username


# Mentor Profile
class MentorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'mentor'})
    bio = models.TextField()
    expertise = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.expertise}"


# Instructor Profile
class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField()
    expertise = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)  # Reference to Instructor model
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title


# Modules and Lessons for a Course
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"


# Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


# Mentorship Request Model
class MentorshipRequest(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, default='Pending')  # Pending, Accepted, Rejected

    def __str__(self):
        return f"{self.student.username} requesting {self.mentor.user.username}"


# Assessments (Quizzes and Assignments)
class Assessment(models.Model):
    ASSESSMENT_TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    ]
    course = models.ForeignKey(Course, related_name='assessments', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assessment_type = models.CharField(max_length=10, choices=ASSESSMENT_TYPE_CHOICES)
    total_marks = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# Questions and Options for Quizzes
class Question(models.Model):
    assessment = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.assessment.title} - {self.question_text[:50]}"


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.question_text[:50]} - {self.option_text}"


# Submission for Assignments
class Submission(models.Model):
    assessment = models.ForeignKey(Assessment, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.assessment.title}"


# Certificates for Completed Courses
class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    certificate_url = models.URLField(blank=True, null=True)
    issued_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Certificate for {self.enrollment.student.username} - {self.enrollment.course.title}"
