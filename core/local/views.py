from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Local
from alocation.settings import NOW_DATE_STR


class LocalsListView(ListView, LoginRequiredMixin):
    queryset = Local.objects.order_by("-added_at")
    template_name = "local/locals-list.html"
    context_object_name = "locals_list"
    search_query = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get("search-query"):
            self.search_query = request.GET.get("search-query")

            self.queryset = (
                self.queryset.filter(tag_name__icontains=self.search_query) |\
                self.queryset.filter(current_tenant__last_name__icontains=self.search_query) |\
                self.queryset.filter(current_tenant__first_name__icontains=self.search_query) |\
                self.queryset.filter(address__icontains=self.search_query) 
            ).distinct()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["now_date"] = NOW_DATE_STR
        context["search_query"] = self.search_query
        return context

    

