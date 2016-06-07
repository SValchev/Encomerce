from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser

class UnpadaidUser(models.Model):
    email = models.CharField(max_length=225, unique=True)
    last_notification = models.DateTimeField(default=timezone.now)

# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225, unique=True)
    last_4_digits = models.CharField(max_length=4,blank=True,null=True)
    stripe_id = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    @classmethod
    def create(cls, name, email, last_4_digits, stripe_id, password):
        user = User(name=name, email=email, last_4_digits=last_4_digits, stripe_id=id)
        user.set_password(password)

        user.save()

        return user


    @classmethod
    def get_user_by_id(cls,user_id):
        return cls.objects.get(pk=user_id)


    def __str__(self):
        return self.email


    def __repr__(self):
        return self.__str__()
