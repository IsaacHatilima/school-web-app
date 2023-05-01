from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
import uuid
# from django.urls import reverse
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
    is_two_fa = models.BooleanField(default=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def get_staff_names(self):
        profile = StaffProfile.objects.get(user=self.id)
        return profile.firstname+' '+profile.lastname

    def get_staff_id(self):
        profile = StaffProfile.objects.get(user=self.id)
        return profile

    class Meta:
        db_table = "users"


class StaffProfile (models.Model):
    public_key = models.UUIDField(default=uuid.uuid4, editable=False,
                                  null=False, unique=True)
    user = models.ForeignKey(User, null=False, editable=False,
                             on_delete=models.PROTECT)
    department_of = models.ForeignKey('administration.Department', null=False,
                                      editable=False, on_delete=models.PROTECT)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    cell = models.CharField(max_length=50, null=False)
    marital_status = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'staff_profiles'
        ordering = ['-id']

    # def get_absolute_url(self):
    #     return reverse('url', args=[args])

    def __str__(self):
        return self.firstname+' '+self.lastname
