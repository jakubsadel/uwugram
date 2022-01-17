from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


def upload_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    return "/".join(
        [
            "avatars",
            str(instance.id)
            + str(instance.username)
            + str(".")
            + str(ext),
        ]
    )


def upload_post_path(instance, filename):
    ext = filename.split(".")[-1]
    return "/".join(
        [
            "posts",
            str(instance.whosePost.id) + str(instance.title) + str(".") + str(ext),
        ]
    )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"),
                              unique=True,
                              error_messages={
                                  "unique": _("A user with that email address already exists."), },
                              )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class Post(models.Model):
    title = models.CharField(max_length=100)
    whosePost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="whosePost", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked", blank=True
    )

    def __str__(self):
        return self.title



class Comment(models.Model):
    text = models.CharField(max_length=100)
    whoseComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="whoseComment", on_delete=models.CASCADE
    )
    whichPost = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
