from django.urls import path
from django.views import static

from . import views

urlpatterns = [
    path('', views.index),
    path('howdy/', views.howdy),
    path('addItem/', views.addItem),
    path('deleteItem/<str:itemName>', views.deleteItem),
    path('updateItem/', views.updateItem),
    path('getItem/<str:itemName>', views.getItem),
    path('getAllItems/', views.getAllItems),
]