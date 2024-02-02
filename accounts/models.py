from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.urls import reverse 

from django.core.validators import FileExtensionValidator,MinValueValidator, MaxValueValidator,EmailValidator
from django.core.exceptions import ValidationError

from django.db.models import Avg

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    '''
    User Model .
    '''
    
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    friends = models.ManyToManyField("self")

    def __str__(self):
        return self.email
    
    objects = CustomUserManager()

    class Meta:
        verbose_name ='CustomUser'