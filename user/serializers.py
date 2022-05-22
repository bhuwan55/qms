from rest_framework import serializers
from django.contrib.auth import authenticate, login, password_validation
from django.core.exceptions import ValidationError
# from phonenumber_field.serializerfields import PhoneNumberField
from .models import User


class RegisterSerializer(serializers.Serializer):
    ROLE_CHOICES = (
        (1, 'admin'),
        (2, 'user'),
    )

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
    )

    def validate(self,data):
        if User.objects.filter(email=data.get('email')).exists():
            raise ValidationError('email already registered')
        # try:
        #     password_validation.validate_password(data["password"])
        # except ValidationError as e:
        #     raise serializers.ValidationError(str(e))
        if len(data['password']) < 8:
            raise ValidationError('password must be greater the 8 characters')
        return data


# class UserEditSerializer(serializers.Serializer):
#     name = serializers.CharField(required=False)
#     address = serializers.CharField(required=False)
#     image = serializers.ImageField(required=False)
#     phone_number = PhoneNumberField(required=False)

#     def validate(self, data):
#         if 'phone_number' in data:
#             if User.objects.filter(phone_number=data['phone_number']).exists():
#                 user = User.objects.get(phone_number=data['phone_number'])
#                 if user.id != self.instance.id:
#                     raise ValidationError('phone number already registered to another user')
#         return data


class UserSerializer(serializers.ModelSerializer):
    # category = serializers.SerializerMethodField()
    # image =serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email', 'role','uuid']

# class UserViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','name', 'location','image', 'uid']


# class UserListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','uid','name','email','phone_number','location','image','is_active','disable']


# class UserCustomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','name']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
    )


# class ChangePasswordSerializer(serializers.Serializer):
#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

#     def validate(self,data):
#         try:
#             password_validation.validate_password(data["new_password"])
#         except ValidationError as e:
#             raise serializers.ValidationError(str(e))
#         return data