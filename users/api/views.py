import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    UserSerializer,
    )


@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        # serializer = UserSerializer(data=json.loads(request.body.decode('utf-8')))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    msg = {
        'status': 'error'
    }
    try:
        data = request.data
        username = data.get('userName', None)
        password = data.get('password', None)
        user = User.objects.get(userName=username, password=password)
    except User.DoesNotExist:
        return Response(msg,status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# serializer = UserLoginSerializer(data=request.data)
# serializer = UserSerializer(data=json.loads(request.body.decode('utf-8')))
""" queryset = User.objects.all()
    data = request.data
    usename = data.get('userName', None)
    password = data.get('password', None)
    if queryset.filter(userName=usename,password=password).exist():
            return Response()
"""

#post bas ma3mola be get we7sha ya3ny first version
def detail(request, userName,password,email,mobile):
    num_results = User.objects.filter(userName=userName).count()
    if num_results == 0:
        user = User()
        user.userName = str(userName)
        user.password = str(password)
        user.email = str(email)
        user.mobile = str(mobile)
        user.save()
        return HttpResponse("{'userName':'"+str(userName)+"','password':'"+str(password)+"','email':'"+str(email)+"','mobile':'"+str(mobile)+"'}")

    else:
        return HttpResponse("{'status':'already exists'}")


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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




