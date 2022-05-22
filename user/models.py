from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from phonenumber_field.modelfields import PhoneNumberField
import uuid
# from lib.utils import get_upload_path_notification, get_upload_path_user
import datetime


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Create a user"""
        if not email:
            raise ValueError('Users must have a valid email.')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Method to handle: manage.py superuser"""
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.role = 1
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        (1, 'admin'),
        (2, 'user'),
    )
    uuid = models.UUIDField(
         unique = True,
         default = uuid.uuid4,
         editable = False)

    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=2)
    disable = models.BooleanField(default=False)
    
    #django default fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['role',]

    def __str__(self):
        return self.name


# class UserProfile(models.Model):
#     name = models.CharField(max_length=100,null=True,blank=True)
#     image = models.ImageField(max_length=255, null=True, blank=True,upload_to=get_upload_path_user)
#     phone_number = PhoneNumberField(unique=True,null=True,blank=True)
#     address = models.CharField(max_length=150,null=True,blank=True)
#     # category = models.ManyToManyField('product.Category')
