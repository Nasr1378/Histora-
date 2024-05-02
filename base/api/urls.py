from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('rooms/', views.getPosts),
    path('rooms/<str:pk>/', views.getPost),
]