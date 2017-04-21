from django.http import HttpResponse
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView
    )


from users.models import User
from .pagination import UserLimitOffsetPagination, UserPageNumberPaginaton

from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserCreateSerializer
    )


def detail(request, userName,password,email,mobile):
    num_results = User.objects.filter(userName=userName).count()
    if num_results == 0:
        user = User()
        user.userName = str(userName)
        user.password = str(password)
        user.email = str(email)
        user.mobile = str(mobile)
        user.save()
    else:
        return HttpResponse("<h1> already exists </h1>")






class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = UserPageNumberPaginaton

    #PageNumberPagination

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'userName'




