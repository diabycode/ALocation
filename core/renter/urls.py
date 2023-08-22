
from django.urls import path

from .views import RenterListView, RenterDetailView, RenterDeleteView, RenterCreateView, RenterEditView

app_name = "renter"

urlpatterns = [
    path('', RenterListView.as_view(), name='renters-list'),
    path('add/', RenterCreateView.as_view(), name='add'),
    path('<str:pk>/edit/', RenterEditView.as_view(), name='edit'),
    path('<str:pk>/delete/', RenterDeleteView.as_view(), name='delete'),
    path('<str:pk>/details/', RenterDetailView.as_view(), name='renter-details'),
]



