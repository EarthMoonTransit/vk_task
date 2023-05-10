from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django import forms


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    date_birth = models.DateField(null=True)
    hometown = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=255, unique=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_friend_status(self, other_user):
        if self == other_user:
            return "same user"
        if other_user in self.friends.all():
            return "friends"
        if FriendRequest.objects.filter(from_user=self, to_user=other_user).exists():
            return "friend request sent"
        if FriendRequest.objects.filter(from_user=other_user, to_user=self).exists():
            return "friend request received"
        return "no connection"

class StatusChoices(models.TextChoices):
    Pending = 'pending'
    Accepted = 'accepted'
    Rejected = 'rejected'

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.Pending, max_length=50)

    class Meta:
        unique_together = ('from_user', 'to_user')




