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
    )

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
   # url(r'^create/$', UserCreateAPIView.as_view(), name='create'),
   #url(r'^$', UserListAPIView.as_view(), name='list'),
   # url(r'^(?P<userName>[\w-]+)/$', UserDetailAPIView.as_view(), name='details'),
   #url(r'^(?P<userName>[\w-]+)/edit/$', UserUpdateAPIView.as_view(), name='update'),
   # url(r'^(?P<userName>[\w-]+)/delete/$', UserDeleteAPIView.as_view(), name='delete'),
    url(r'^(?P<username>[\w-]+)/(?P<password>.*)/(?P<email>[\w.@+-]+)/(?P<mobile>[0-9]+)/$', detail, name='signup1'),

]
