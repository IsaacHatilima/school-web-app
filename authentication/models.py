from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
import uuid
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, username, role, password):
        user = self.model(username=username, email=self.normalize_email(email),
                          role=role)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, role, password):
        user = self.model(username=username, email=self.normalize_email(email),
                          role=role)
        user.set_password(password)
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('System Admin', 'System Admin'),
        ('School Admin', 'School Admin'),
        ('Head Teacher', 'Head Teacher'),
        ('Deputy Head Teacher', 'Deputy Head Teacher'),
        ('Careers and Counseling', 'Careers and Counseling'),
        ('Class Teacher', 'Class Teacher'),
        ('Subject Teacher', 'Subject Teacher'),
        ('Accounts', 'Accounts'),
        ('Parent', 'Parent'),
    ]
    public_key = models.UUIDField(default=uuid.uuid4, editable=False,
                                  null=False, unique=True)
    email = models.EmailField(max_length=90, unique=True, null=False)
    username = models.CharField(max_length=90, unique=True, null=False)
    is_verified = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=False)
    login_attemps = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    two_fa = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    objects = UserManager()

    def __str__(self):
        return self.email + ' ('+self.is_active+')'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        db_table = "users"
