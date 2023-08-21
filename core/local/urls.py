
from django.contrib import admin
from django.urls import path, include

from .views import *

app_name = "local"

urlpatterns = [
    path('', LocalsListView.as_view(), name="locals-list"),
    path('<str:pk>/details', LocalDetailsView.as_view(), name="local-details"),
    path('<str:pk>/delete/', LocalDeleteView.as_view(), name="delete"),
    # path('<str:pk>/delete/', local_delete_view, name="delete"),
    path('assign-local-to-renter/', assign_local_to_renter, name="assign-local-to-renter"),
]
