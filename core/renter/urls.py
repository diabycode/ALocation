
from django.urls import path

from .views import RenterListView, RenterDetailView, RenterDeleteView

app_name = "renter"

urlpatterns = [
    path('', RenterListView.as_view(), name='renters-list'),
    path('<str:pk>/details/', RenterDetailView.as_view(), name='renter-details'),
    path('<str:pk>/delete/', RenterDeleteView.as_view(), name='delete'),
]



