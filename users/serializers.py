from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Commercial


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'code', 'email', 'first_name',
            'last_name', 'position', 'is_active',
            'groups', 'user_permissions', 'password'
        )
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

class CommercialSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    manager = serializers.SerializerMethodField()
    user_email = serializers.EmailField(write_only=True)
    manager_email = serializers.EmailField(
        write_only=True, required=False, allow_blank=True,
        allow_null=True
    )

    class Meta:
        model = Commercial
        fields = ('user', 'manager', 'goal_type', 'goal', 'user_email', 'manager_email')
        extra_kwargs = {
            'goal_type': {'required': True},
            'goal': {'required': True}
        }

    def get_manager(self, obj):
        return obj.manager.email if obj.manager else None

    def create(self, validated_data):
        user_email = validated_data.pop('user_email')
        manager_email = validated_data.pop('manager_email', None)
        if user_email == manager_email:
            raise serializers.ValidationError(
                {'manager_email': 'Manager email must be different from user email'}
            )

        user = User.objects.filter(email=user_email)
        if not user.exists():
            raise serializers.ValidationError({'user_email': 'User with this email does not exist'})

        commercial = Commercial(user=user.first(), **validated_data)
        if manager_email:
            manager = User.objects.filter(email=manager_email)
            if not manager.exists():
                raise serializers.ValidationError({'manager_email': 'Manager with this email does not exist'})
            commercial.manager = manager.first()

        commercial.save()
        return commercial
