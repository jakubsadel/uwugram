from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "whosePost", "created_on", "img", "liked")
        extra_kwargs = {"whosePost": {"read_only": True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "text", "whoseComment", "whichPost")
        extra_kwargs = {"whoseComment": {"read_only": True}}
