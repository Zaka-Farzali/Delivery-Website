from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.utils.translation import gettext_lazy
# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_superuser(self, Email, Name, Surname, Password = None, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        return self.create_user(Email, Name = Name, Surname = Surname, Password = Password, **other_fields)


    def create_user(self, Email, Name, Surname, Password = None, **other_fields):
        
        if not Email:
            raise ValueError(gettext_lazy('You must provide email address'))

        email = self.normalize_email(Email)
        user = self.model(email, Name, Surname, **other_fields)
        user.set_password(Password)
        user.save(using=self._db)
       
        return user

class Customer(AbstractBaseUser, PermissionsMixin):
    Email = models.EmailField(gettext_lazy('email address'), max_length=256, unique=True)
    Name = models.CharField(max_length=64)
    Surname = models.CharField(max_length=64, null=True)
    Birthday = models.DateField(auto_now=False, null=False,blank=True)
    PhoneNumber = models.CharField(max_length=16, unique=True)
    Address = models.CharField(max_length=128)
    RegistrationDate  = models.DateTimeField(default=timezone.now, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserAccountManager()
    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['Name', 'Surname']

    def __str__(self):
        return self.Name + " " + self.Surname

    def has_perm(self, perm, obj = None):
        return self.is_superuser