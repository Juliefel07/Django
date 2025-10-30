from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Custom user manager
class StudentManager(BaseUserManager):
    def create_user(self, email, school_id, password=None, **extra_fields):
        """Create and save a regular student user"""
        if not email:
            raise ValueError('Students must have an email address')
        if not school_id:
            raise ValueError('Students must have a school ID')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, school_id=school_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, school_id, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, school_id, password, **extra_fields)


class Student(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    school_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['school_id']

    def __str__(self):
        return self.full_name if self.full_name else self.email
# Lost Item model
class Item(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100)
    description = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True)  # optional override
    item_type = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='items/', blank=True, null=True)

    # Status fields
    found = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    # Optional additional info for both lost & found
    additional_info = models.TextField(blank=True)

    # Extra item details
    color = models.CharField(max_length=100, blank=True)
    material = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    proof_of_ownership = models.CharField(max_length=200, blank=True)
    identifying_elements = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    @property
    def owner_contact(self):
        # returns the contact number exactly like "09755066673"
        return self.owner.contact_number or "Unknown"

# Comment model
class Comment(models.Model):
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.commenter} on {self.item}'

# Claim model
class Claim(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    claimer = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    claimed_at = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=False)
    # inside Student model
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default-avatar.png', blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', default='cover_photos/default-cover.jpg', blank=True)

    def __str__(self):
        return f'{self.claimer} claims {self.item}'
class LostItem(models.Model):
    student_id = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True)
    grade_section = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Lost info
    place = models.CharField(max_length=100, blank=True)
    last_seen_date = models.DateField(blank=True, null=True)
    last_seen_time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True)

    # Found info
    found = models.BooleanField(default=False)
    found_date = models.DateField(blank=True, null=True)
    finder_name = models.CharField(max_length=100, blank=True)
    finder_contact = models.CharField(max_length=20, blank=True)
    place_found = models.CharField(max_length=100, blank=True)
    found_description = models.TextField(blank=True)



class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # <-- THIS FIXES THE ERROR
        on_delete=models.CASCADE
    )
    avatar = models.CharField(max_length=50, default='avatar1.png')



class Feedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)  # manual name
    feedbacks = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        display_name = self.name or (self.user.username if self.user else "Anonymous")
        return f"{display_name} - {self.feedbacks[:30]}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()  # the content of the notification
    is_read = models.BooleanField(default=False)  # whether the user has seen the notification
    created_at = models.DateTimeField(auto_now_add=True)  # automatically set when the notification is created

    def __str__(self):
        return self.message


