from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    """
    TokenSerializer
    """
    @classmethod
    def get_token(cls, user):
        token = super(ObtainTokenPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for registering the user
    """
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    """
    CustomUser Serializer
    """
    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'last_name')