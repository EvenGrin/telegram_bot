from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_user/', views.add_user, name='add_user'),
    path('users_list/', views.users_list, name='users_list'),
    path('send_message/', views.send_message, name='send_message'),
]
