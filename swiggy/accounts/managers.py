from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import accounts.constants as user_const

class UserManger(BaseUserManager):
     def save_user(self, userid, password, **extra_fields):
        if not userid:
            raise ValueError(_("The Userid must be set"))
        
        user = self.model(userid=userid, **extra_fields)
        user.set_password(password)
        user.save()
        return user

     def create_user(self, userid, password, **extra_fields):
        if self.filter(phone_no = extra_fields.get('phone_no'), user_type=user_const.USER).exists():
            raise ValueError(_("This Phone Number already exist"))

        return self.save_user(userid, password, **extra_fields)

    
     def create_superuser(self, userid, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", user_const.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("user_type") is not user_const.ADMIN:
            raise ValueError(_(f"Superuser must have user_type={user_const.ADMIN}."))
        
        if self.filter(phone_no = extra_fields.get('phone_no'), user_type=user_const.ADMIN).exists():
            raise ValueError(_("This Phone Number already exist"))

        return self.save_user(userid, password, **extra_fields)

     def create_restaurant_owner(self, userid, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", user_const.RESTAURANT)

        if extra_fields.get("user_type") is not user_const.RESTAURANT:
            raise ValueError(_(f"Superuser must have user_type={user_const.RESTAURANT}."))
        
        if self.filter(phone_no = extra_fields.get('phone_no'), user_type=user_const.RESTAURANT).exists():
            raise ValueError(_("This Phone Number already exist"))

        return self.save_user(userid, password, **extra_fields)

     def create_delivery_boy(self, userid, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", user_const.DELIVERY)

        if extra_fields.get("user_type") is not user_const.DELIVERY:
            raise ValueError(_(f"Superuser must have user_type={user_const.DELIVERY}."))
        
        if self.filter(phone_no = extra_fields.get('phone_no'), user_type=user_const.DELIVERY).exists():
            raise ValueError(_("This Phone Number already exist"))

        return self.save_user(userid, password, **extra_fields)