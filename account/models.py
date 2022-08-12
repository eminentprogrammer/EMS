from turtle import position
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from apps.modules.settings import SendMail
import random
import uuid

def Generate_OTP():
	otp = ""
	for i in range(4):
		otp += str(random.randint(2,9))
	return int(otp)

def Generate_slug():
	otp = "v-"
	for i in range(15):
		otp += str(random.randint(2,9))
	return otp


class Parent(models.Model):
    name            = models.CharField(max_length=200, blank=True, null=True)
    email           = models.EmailField(help_text="Parent Email Address",  blank=True, null=True)
    phone_number    = models.CharField(max_length=20, help_text="Parent Phone Number",  blank=True, null=True)
    relationship    = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MyAccountManager(BaseUserManager):
    def create_superuser(self, username, email, password):
        if not email:
            raise ValueError('Admin must have a valid College email address')
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            )
        user.is_active = True
        user.is_admin   = True
        user.is_staff   = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
        
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('User enter a valid email address')
        elif not username:
            raise ValueError('User must enter a unique username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            password = password,
            )
        user.is_active  = False
        user.is_student = False
        user.is_admin   = False
        user.is_staff   = False
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user

ACCOUNT_TYPE = (
    (0,'STUDENT'),
    (1,'STAFF'),
)


class Account(AbstractBaseUser):
    username                = models.CharField(max_length=250, unique=True, primary_key=True, verbose_name="User ID")

    email                   = models.EmailField(verbose_name='email', max_length=354, unique=True)
    
    lastname                = models.CharField(max_length=200, help_text="Last name", blank=True, null=True)

    firstname               = models.CharField(max_length=200, help_text="First name", blank=True, null=True)
    
    phone_number            = models.CharField(max_length=17, unique=True, blank=True, null=True)

    account_type            = models.PositiveIntegerField(choices=ACCOUNT_TYPE, null=True)
    
    email_verification_pin  = models.PositiveIntegerField(blank=True, null=True)

    is_email_verified       = models.BooleanField(default=False)

    is_active               = models.BooleanField(default=False)
    is_student              = models.BooleanField(default=False)
    is_admin                = models.BooleanField(default=False)
    is_female_porter        = models.BooleanField(default=False)
    is_male_porter          = models.BooleanField(default=False)
    is_dsa                  = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)

    slug                    = models.SlugField(blank=True, null=True, default=Generate_slug())

    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["username"]

    objects = MyAccountManager()
    
    class Meta:
        verbose_name_plural = "Account"
    
    def __str__(self):
        return "%s %s" %(self.username, self.email)
    
    def get_account_type(self):
        return self.account_type
    
    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    
    def verify_email(self):
        self.email_verification_pin = Generate_OTP()
        self.slug = Generate_slug()
        self.save()
        SendMail.Send_OPT(self.email, self.email_verification_pin)

    def save(self, *args, **kwargs):
        if self.account_type == 0:
            self.is_student     = True
        elif self.account_type  == 1:
            self.is_staff       = True
        else:
            pass
        super().save(*args, **kwargs)
        

DEPARTMENT = (
    ('Physics','Physics'),
    ('English','English'),
    ('Economics','Economics'),
    ('Chemical Sciences','Chemical Sciences'),
    ('Biological Sciences','Biological Sciences'),
    ('Mathematical Sciences','Mathematical Sciences'),
    ('Accounting and Finance','Accounting and Finance'),
    ('Business Administration','Business Administration'),
    ('Mass Communication and Media Studies',' Mass Communication and Media Studies'),
    ('Philosophy and Religious Studies','Philosophy and Religious Studies'),
    ('Political Science and International Relations','Political Science and International Relations'),
)

GENDER = (
    ('Female', 'Female'),
    ('Male', 'Male'),
)

RESIDENCE = (
    ('Assumption Hall', 'Assumption Hall'),
    ('Divine Mercy Hall', 'Divine Mercy Hall'),
)


class Student(models.Model):
    user                = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    gender              = models.CharField(max_length=500, help_text="Gender", choices=GENDER, blank=True, null=True)
    department          = models.CharField(max_length=500, help_text="Department", choices=DEPARTMENT, blank=True, null=True)
    hall_of_residence   = models.CharField(max_length=500, choices=RESIDENCE, blank=True, null=True)
    
    parent_name         = models.CharField(max_length=500, blank=True, null=True)
    parent_email        = models.EmailField(default="user@ems.com")
    parent_phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    slug                = models.SlugField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Student Profile"

    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        if self.gender == 0:
            self.hall_of_residence = 'Assumption Hall'
        else:
            self.hall_of_residence = 'Divine Mercy Hall'
        super().save(*args, **kwargs)