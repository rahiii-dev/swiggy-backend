from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import UserManger
import accounts.constants as user_const


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    userid = models.CharField('Userid', max_length=50, primary_key=True)
    email = models.EmailField('Email', null=True)
    phone_no = models.CharField('Phone Number', null=True, max_length = 10)
    full_name = models.CharField('Full Name', null=True, blank=True, max_length=50)
    user_type = models.PositiveSmallIntegerField(choices=user_const.USER_TYPE_CHOICES, default=user_const.USER)

    USERNAME_FIELD = "userid"
    REQUIRED_FIELDS = ['phone_no']

    objects = UserManger()

    def __str__(self):
      return self.userid
    
    @property
    def UserType(self):
      for Utype in user_const.USER_TYPE_CHOICES:
            if self.user_type in Utype:
                return Utype[1]