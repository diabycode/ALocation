from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Renter
from alocation.settings import NOW_DATE_STR


class RenterListView(ListView, LoginRequiredMixin):
    queryset = Renter.objects.order_by("-added_at")
    context_object_name = "renters"
    template_name = "renter/renter-list.html"
    search_query = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get("search-query"):
            self.search_query = request.GET.get("search-query")

            self.queryset = (
                self.queryset.filter(first_name__icontains=self.search_query) | \
                self.queryset.filter(last_name__icontains=self.search_query) | \
                self.queryset.filter(local__tag_name__icontains=self.search_query) 
            ).distinct()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now_date"] = NOW_DATE_STR
        if self.search_query:
            context["search_query"] = self.search_query.strip()
        return context


class RenterDetailView(DetailView, LoginRequiredMixin):
    model = Renter
    context_object_name = "renter"
    template_name = "renter/renter-details.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["renter_locals"] = (self.get_object()).local_set.all()
        context_data["renter_payments"] = (self.get_object()).payment_set.all()
        context_data["now_date"] = NOW_DATE_STR
        return context_data



    



