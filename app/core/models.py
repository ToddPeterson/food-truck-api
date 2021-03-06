# from django.db import models
# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     BaseUserManager,
#     PermissionsMixin
# )

# from vendor.models import Vendor


# class UserManager(BaseUserManager):

#     def create_user(self, email, password=None, **other_fileds):
#         """Create and save a new user"""
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(email=self.normalize_email(email), **other_fileds)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_superuser(self, email, password):
#         """Create and save a new superuser"""
#         user = self.create_user(email, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return user


# class User(AbstractBaseUser, PermissionsMixin):
#     """Custom user model that replaces username with email"""

#     email = models.EmailField(max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     vendor = models.OneToOneField(
#         Vendor,
#         on_delete=models.CASCADE,
#         null=True
#     )

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
