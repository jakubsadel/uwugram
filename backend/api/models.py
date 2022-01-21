from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


def upload_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    return "/".join(
        [
            "avatars",
            str(instance.whoseProfile.id)
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


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email is must")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Profile(models.Model):
    username = models.CharField(max_length=20)
    whoseProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="whoseProfile", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.username


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
