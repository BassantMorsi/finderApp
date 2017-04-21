from rest_framework.serializers import ModelSerializer

from users.models import User


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'userName',
            'password',
            'email',
            'mobile',
        ]


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'userName',
            'password',
            'email',
            'mobile',
        ]


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'userName',
            'email',
            'mobile',
        ]