from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index),
    re_path(r"^list/(?P<detailType>[A-Za-z]+)/", views.list, name='list'),
    re_path(r"^editPerson/(?P<id>[0-9]*)", views.editPerson, name='editPerson'),
    re_path(r"^editProject/(?P<id>[0-9]*)", views.editProject, name='editProject'),
    re_path(r"^details/(?P<detailType>[A-Za-z]+)/(?P<id>[0-9]+)/$", views.details, name='details'),
    re_path(r"^delete/(?P<detailType>[A-Za-z]+)/(?P<id>[0-9]*)", views.delete, name='delete'),
]
