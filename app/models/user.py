from django.db import models
from django.utils import timezone

from .manager import UserManager

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from autoslug import AutoSlugField

GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Others", "Others"),
    ("NONE", "NONE"),
)

BLOOD_GROUP = (
    ("1", "A+"),
    ("2", "A-"),
    ("3", "B+"),
    ("4", "B-"),
    ("5", "O+"),
    ("6", "O-"),
    ("NONE", "NONE"),
)

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=225,blank=True, default='', unique=True)
    email = models.EmailField(blank=True, default='', unique=True)
    first_name = models.CharField(max_length=225, blank=True, default='')
    last_name = models.CharField(max_length=225, blank=True, default='')
    user_type = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=0, blank=True)
    delete = models.BooleanField(default=False)
    # phone_slug=AutoSlugField(populate_from='email',
    #                      unique_with=['first_name', 'last_name'],null=True,default=None)
    
    user_id = models.CharField(max_length=225,blank=True, default='', primary_key=True)
    age = models.IntegerField(default = 1)
    gender = models.CharField(max_length = 20,choices = GENDER,default = 'NONE')
    blood_group = models.CharField(max_length = 20,choices = BLOOD_GROUP,default = 'NONE')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UserManager()
    

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.first_name
    
    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]
    
    
    def __str__(self):
        return str(self.user_id)

    
    
