from django.urls import path
from django.views import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('itemView/', views.item, name='item-view'),
    path('updateView/', views.updateView, name='update-view'),
    path('addView/', views.addView, name='add-view'),

    path('addItem/', views.addItem),
    path('updateItem/', views.updateItem),
    path('deleteItem/', views.deleteItem, name='delete-item'),
]