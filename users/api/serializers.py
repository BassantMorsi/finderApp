from rest_framework.serializers import ModelSerializer

from users.models import User, MissRequest, FindRequest


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'userName',
            'password',
            'email',
            'mobile',
        )


class UserMissRequestSerializer(ModelSerializer):
    class Meta:
        model = MissRequest
        fields = (
            'date',
            'status',
            'fName',
            'gender',
            'type',
        )


class UserFindRequestSerializer(ModelSerializer):
    class Meta:
        model = FindRequest
        fields = (
            'date',
            'status',
            'fName',
            'gender',
            'type',
        )














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