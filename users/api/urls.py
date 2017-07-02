from django.conf.urls import url

from users.api import views
from .views import (
    UserListAPIView,
    UserDetailAPIView,
    UserDeleteAPIView,
    UserUpdateAPIView,
    UserCreateAPIView,
    signup,
    login,
    detail,
    find_request,
    miss_request,
    recognize,
    user_requests,
    request_status,
    )

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
    url(r'^find_request/$', find_request, name='find_request'),
    url(r'^miss_request/$', miss_request, name='miss_request'),
    url(r'^login/(?P<username>[\w-]+)/$', user_requests, name='user_requests'),
   # url(r'^create/$', UserCreateAPIView.as_view(), name='create'),
   #url(r'^$', UserListAPIView.as_view(), name='list'),
   # url(r'^(?P<userName>[\w-]+)/$', UserDetailAPIView.as_view(), name='details'),
   #url(r'^(?P<userName>[\w-]+)/edit/$', UserUpdateAPIView.as_view(), name='update'),
   # url(r'^(?P<userName>[\w-]+)/delete/$', UserDeleteAPIView.as_view(), name='delete'),
   url(r'^(?P<username>[\w-]+)/(?P<password>.*)/(?P<email>[\w.@+-]+)/(?P<mobile>[0-9]+)/$', detail, name='signup1'),
   url(r'^recognize/$', recognize, name='recognize'),
   url(r'^request_status/$', request_status, name='request_status'),
]
