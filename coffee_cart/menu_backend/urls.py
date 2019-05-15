from django.urls import path
from django.views import static

from . import views

urlpatterns = [
    path('', views.index),
    path('itemView/', views.item, name='item-view'),
    path('updateView/', views.updateView, name='update-view'),
    path('addView/', views.addView, name='add-view'),

    path('addItem/', views.addItem),
    path('updateItem/', views.updateItem),
    path('deleteItem/<str:itemName>/', views.deleteItem),
    path('getItem/<str:itemName>/', views.getItem),
    path('getAllItems/', views.getAllItems),
]