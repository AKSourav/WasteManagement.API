from django.contrib.auth.base_user import BaseUserManager
from django.apps import apps  # Import the apps module to get the User model dynamically
import random

def unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        User = apps.get_model('app', 'User')  # Get the User model dynamically

        try:
            n=User.objects.get(user_id=uq)
        except:
            return uq
        
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, phone=None,email=None, password=None, **extra_fields):
        if not phone and not email:
            raise ValueError("You have not provided a valid USER PHONE NUMBER or EMAIL")
        user_id=unique_number("superuser")
        print("email",email,"sdfsdfs")
        email = self.normalize_email(email)
        print("email",email,"sdfsdfs")
        user = self.model(phone=phone,email=email,user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)
    
    def create_superuser(self, phone=None,email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(phone,email, password, **extra_fields)
    