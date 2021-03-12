from django.urls import path
from . import views

urlpatterns = [
    path('tree', views.tree_diagram),
    path('add/<slug:object>', views.add)
]