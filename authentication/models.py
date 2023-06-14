from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
import uuid
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class Profile (models.Model):
    public_key = models.UUIDField(default=uuid.uuid4, editable=False,
                                  null=False, unique=True)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    cell = models.CharField(max_length=50, null=False)
    marital_status = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'profiles'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse("admin_staff_update", kwargs={"public_key": self.public_key})

    def __str__(self):
        return self.firstname+' '+self.lastname


class UserManager(BaseUserManager):
    def create_user(self, email, username, role, profile, password):
        user = self.model(username=username, email=self.normalize_email(email),
                          role=role, profile=profile)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, role, profile, password):
        user = self.model(username=username, email=self.normalize_email(email),
                          role=role, profile=profile)
        user.set_password(password)
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('System Admin', 'System Admin'),
        ('Clerk', 'Clerk'),
        ('Dispatch', 'Dispatch'),
        ('Stakeholder', 'Stakeholder'),
    ]
    public_key = models.UUIDField(default=uuid.uuid4, editable=False,
                                  null=False, unique=True)
    email = models.EmailField(max_length=90, unique=True, null=False)
    username = models.CharField(max_length=90, unique=True, null=False)
    profile = models.ForeignKey(Profile, null=True, editable=False,
                                on_delete=models.PROTECT)
    is_verified = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=False)
    login_attemps = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    two_fa = models.CharField(max_length=10, null=True)
    is_two_fa = models.BooleanField(default=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role', 'profile']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token)
        }

    def get_staff_names(self):
        profile = Profile.objects.get(user=self.id)
        return profile.firstname+' '+profile.lastname

    class Meta:
        db_table = "users"
