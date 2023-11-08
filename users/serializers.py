from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        groups = validated_data.pop('groups')
        permissions = validated_data.pop('user_permissions')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # add groups
        user.groups.set(groups)

        # add permissions
        user.user_permissions.set(permissions)
        return user

class TokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['position'] = user.position
        token['is_active'] = user.is_active
        token['groups'] = list(user.groups.values_list('id', flat=True))

        return token
