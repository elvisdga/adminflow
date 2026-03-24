from django.urls import path
from . import views

urlpatterns = [
    
    #usando FBV Funcion Basado en Vista
    #path("clients/", views.client_list, name="client_list"),
    #usando CBV Clases Basado en Vista
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/new/", views.ClientCreateView.as_view(),name="client_create"),
    path("clients/<int:pk>/edit/", views.ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", views.ClientDeleteView.as_view(), name="client_delete")
]