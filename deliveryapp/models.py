from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.hashers import make_password
# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password = None, **other_fields):
        
        if not email:
            raise ValueError(gettext_lazy('You must provide email address'))

        email = self.normalize_email(email)
        user = self.model(email=email , **other_fields)
        user.password  = make_password(password)
        user.save(using=self._db)
       
        return user

    def create_superuser(self, email, password = None, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        return self.create_user(email=email, password = password, **other_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy('email address'), max_length=256, unique=True)
    name = models.CharField(max_length=64, null=True)
    surname = models.CharField(max_length=64, null=True)
    birthday = models.DateField(auto_now=False, null=True,blank=True)
    phone_number = models.CharField(max_length=16, unique=True, null=True, blank=True)
    address = models.CharField(max_length=128, blank=True)
    registration_date  = models.DateTimeField(default=timezone.now, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj = None):
        return self.is_superuser


class FAQ(models.Model):
    Question = models.TextField(max_length=512)
    Answer = models.TextField()
    Date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.Question

class Partner(models.Model):
    Name = models.CharField(max_length=64)
    Logo = models.ImageField()
    Url = models.URLField()
    Description = models.TextField(max_length=256)
    Date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.Name

class Order(models.Model):

    STATUS_CHOICES =[
        ('PR', 'In Progress'),
        ('OR','Ordered'),
        ('DL','Delivered'),
        ('FN','Finished'),
    ]
    Url = models.URLField()
    Color = models.CharField(max_length=32)
    Size = models.CharField(max_length=16)
    Amount = models.IntegerField()
    OtherInfo = models.TextField(max_length=256)
    Status  = models.CharField(max_length=2, choices=STATUS_CHOICES,default='PR', editable=True)
    OrderDate = models.DateTimeField(default=timezone.now, editable=False)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.Url 

class Storage(models.Model):
    Country = models.CharField(max_length=32)
    City = models.CharField(max_length=32)
    Address = models.CharField(max_length=128)
    Date = models.DateTimeField(default=timezone.now, editable=False)
    Partner = models.ManyToManyField(Partner)

    def __str__(self):
        return self.City + " " + self.Address
