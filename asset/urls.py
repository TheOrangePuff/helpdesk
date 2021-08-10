from django.urls import path
from . import views

urlpatterns = [
    path('tree', views.tree_diagram),
    path('add/<slug:db_object>', views.add, name='add'),
    path('view/<slug:db_object>', views.view, name='view'),
    path('create', views.create, name='create'),
    path('edit/<slug:db_object>', views.edit, name='edit')
]