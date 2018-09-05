from django.urls import path

from . import views

urlpatterns = [
    path('create', views.manage_create, name='create'),
    path('list', views.manage_list, name='list'),
    path('list/<int:page>/', views.manage_list, name='list'),
    path('update', views.manage_update, name='update'),
    path('update/<str:name>/', views.manage_update, name='update'),
    path('get', views.manage_get, name='get'),
    path('get/<str:name>/', views.manage_get, name='get'),
    path('delete', views.manage_delete, name='delete'),
    path('delete/<str:name>/', views.manage_delete, name='delete'),
    path('single', views.single, name='manage'),
    path('upload', views.upload, name='Upload pulses'),
    path('download', views.download, name='Download pulses'),
    path('', views.index, name='index')
]
