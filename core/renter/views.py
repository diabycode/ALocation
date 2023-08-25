from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from .models import Renter
from local.models import Local
from alocation.settings import NOW_DATE_STR
from .forms import RenterForm 



class RenterListView(ListView, LoginRequiredMixin):
    queryset = Renter.objects.order_by("-added_at")
    context_object_name = "renters"
    template_name = "renter/renter-list.html"
    search_query = None
    paginate_by = 7

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
    
        if not request.user.is_staff:
            return redirect("not-staff-user")
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
        
        if not request.user.is_staff:
            return redirect("not-staff-user")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["renter_locals"] = (self.get_object()).local_set.all()
        context_data["locals_list"] = [l for l in Local.objects.all() if not l.is_currently_rented]
        context_data["renter_payments"] = (self.get_object()).payment_set.all()
        context_data["now_date"] = NOW_DATE_STR
        return context_data


class RenterDeleteView(DeleteView):
    model = Renter
    template_name = "renter/renter__confirm_delete.html"
    context_object_name = "renter"
    extra_context = {'now_date': NOW_DATE_STR}
    
    def get_success_url(self) -> str:
        return reverse("renter:renters-list")
    

class RenterCreateView(CreateView):
    model = Renter
    template_name = "renter/renter-add.html"
    form_class = RenterForm
    success_url = reverse_lazy("renter:renters-list")
    extra_context = {'now_date': NOW_DATE_STR}


class RenterEditView(UpdateView):
    model = Renter
    form_class = RenterForm
    template_name = "renter/renter-edit.html"
    extra_context = {'now_date': NOW_DATE_STR}

    def get_success_url(self) -> str:
        success_url = reverse("renter:renter-details", kwargs={'pk': (self.get_object()).pk}) 
        return success_url
