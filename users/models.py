from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password


# USER MANAGER
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Incorrect Email, The EMail Field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # Create user with the given email and password.

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('The Email field must be set')

        user = self.create_user(email, password, **extra_fields)
        return user


# Custom User
class CustomUser(AbstractBaseUser):
    username = None
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Merchant Model
class Merchant(models.Model):
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    is_merchant = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name
