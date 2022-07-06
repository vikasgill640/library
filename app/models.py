from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    type=models.CharField(max_length=99,choices=(('Librarian','Librarian'),('Member','Member')))
    gender=models.CharField(max_length=24,choices=(('male','male'),('female','female'),('other','other')))
    mobile_no=models.CharField(max_length=12)
    address=models.TextField(max_length=500)
    def __str__(self):
        return str(self.username)

class Book(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=449)
    status=models.CharField(max_length=39,default='Available',choices=(('Borrowed','Borrowed'),('Available','Available')))
    def __str__(self):
        return str(self.name)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user.username)