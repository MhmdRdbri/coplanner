from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import random
import asyncio
import http.client
import json

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(unique=True, max_length=15)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    # email = models.EmailField(unique=True, default='a@gmail.com')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    has_special_access = models.BooleanField(default=False)
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True) 

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    def __str__(self):
        return self.full_name()
        



class PasswordResetToken(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def create_code(cls, user):
        token = ''.join(random.choices('0123456789', k=6))
        expiration_time = timezone.now() + timezone.timedelta(minutes=2)
        return cls.objects.create(user=user, token=token)

    @classmethod
    def delete_code(cls, token):
        cls.objects.filter(token=token).delete()

    def is_expired(self):
        return self.expiration_time <= timezone.now()

class PendingRegistration(models.Model):
    phone_number = models.CharField(unique=True, max_length=15)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.last_name
        conn = http.client.HTTPSConnection("api2.ippanel.com")
                payload = json.dumps({"code": "vdphprz0qk3wgm7","sender": "+983000505","recipient": self.phone_number,"variable":{"full_name": f"{self.first_name}",}})headers = {
                    'apikey': ' SZtX_MYwI2E0jWqdkrSoDV3-02u0yF-l2c1LXgZVZpw= ',
                    'Content-Type': 'application/json'
                }
                conn.request("POST", "/api/v1/sms/pattern/normal/send", payload, headers)
                res = conn.getresponse()
                result = res.read().decode("utf-8")
                if res.status == 200:
                    status = 'sent'
                else:
                    status = 'error'
            except Exception as e:
                result = str(e)
                status = 'error'

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    work_position = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.phone_number:
            self.phone_number = self.user.phone_number

        if self.phone_number != self.user.phone_number:
            self.user.phone_number = self.phone_number
            self.user.save()
            
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f'پروفایل {self.name} {self.last_name} '