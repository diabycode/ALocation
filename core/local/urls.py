
from django.urls import path

from .views import (
    LocalsListView,
    LocalDetailsView,
    LocalDeleteView,
    LocalEditView,
    LocalAddView,
    assign_local_to_renter,
    change_renter,
)

app_name = "local"

urlpatterns = [
    path('', LocalsListView.as_view(), name="locals-list"),
    path('<str:pk>/details', LocalDetailsView.as_view(), name="local-details"),
    path('<str:pk>/delete/', LocalDeleteView.as_view(), name="delete"),
    path('<str:pk>/edit/', LocalEditView.as_view(), name="edit"),
    path('add/', LocalAddView.as_view(), name="add"),

    path('assign-local-to-renter/', assign_local_to_renter, name="assign-local-to-renter"), # type: ignore
    path('change-renter/', change_renter, name="change_renter"), # type: ignore
]
