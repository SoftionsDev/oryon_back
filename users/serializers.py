from rest_framework import serializers

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
