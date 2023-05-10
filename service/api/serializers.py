from rest_framework import serializers
from .models import User, FriendRequest
from django.conf import settings
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from rest_framework import filters, status
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    date_birth = serializers.DateField(required=False,
                                       format=settings.DATE_INPUT_FORMATS[0], input_formats=[f'{settings.DATE_INPUT_FORMATS[0]}', 'iso-8601'])

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'date_birth', 'hometown', 'email')
        model = User


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    repeat_password = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ('email', 'password', 'repeat_password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    repeat_password = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ('old_password', 'password', 'repeat_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


