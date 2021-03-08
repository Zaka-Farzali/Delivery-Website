from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
# Create your models here.

class Customer(models.Model):
    Name = models.CharField(max_length=64)
    Surname = models.CharField(max_length=64, null=True)
    Birthday = models.DateField(auto_now=False, null=False,blank=False)
    Email = models.EmailField(max_length=256)
    Password = models.CharField(max_length=32)
    PhoneNumber = models.CharField(max_length=16)
    Address = models.CharField(max_length=128)
    RegistrationDate  = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.Name + " " + self.Surname

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
# Create your models here.
