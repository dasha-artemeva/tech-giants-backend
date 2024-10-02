from django.urls import path

from applications.ui import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lk', views.lk, name='lk')
]