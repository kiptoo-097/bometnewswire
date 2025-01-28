from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^(07|01)\d{8}$',
                message="Phone number must start with '07' or '01' and be exactly 10 digits.",
            ),
            MinLengthValidator(10)
        ]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('Politics', 'Politics'),
        ('National', 'National'),
        ('Business', 'Business'),
        ('Sports', 'Sports'),
        ('Lifestyle', 'Lifestyle'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    caption = models.CharField(max_length=255, null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    trending = models.BooleanField(default=False)
    published_by = models.ForeignKey(Publisher, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class AdditionalImage(models.Model):
    article = models.ForeignKey(NewsArticle, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/')
    caption = models.CharField(max_length=255, null=True, blank=True)
    placeholder = models.CharField(max_length=100, default='placeholder_1')  # Default value added

    def __str__(self):
        return f"Image for {self.article.title} at {self.placeholder}"


class Epaper(models.Model):
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='epapers/', default='epapers/News_Wire.pdf')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title