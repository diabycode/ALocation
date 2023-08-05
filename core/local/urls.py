
from django.contrib import admin
from django.urls import path, include

from .views import LocalsListView

app_name = "local"

urlpatterns = [
    path('', LocalsListView.as_view(), name="locals-list"),

]
