from django.urls import path
from core import views

urlpatterns = [
    path('requests/', views.request_list),
    path('requests/<int:pk>/', views.request_detail),
    path('sellers/', views.seller_list),
    path('sellers/<int:pk>/', views.seller_detail),
    path('feedbacks/', views.rate),
    path('users/', views.user)
]