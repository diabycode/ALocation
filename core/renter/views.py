from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from .models import Renter
from local.models import Local
from alocation.settings import NOW_DATE_STR
from .forms import RenterForm, RenterFilterForm



class RenterListView(ListView, LoginRequiredMixin):
    queryset = Renter.objects.order_by("-added_at")
    context_object_name = "renters"
    template_name = "renter/renter-list.html"
    search_query = None
    paginate_by = 7
    filter_form = RenterFilterForm()

    queryset_is_filtered = False

    filter_items = (
        {"name": 'currently_tenant', 'label': 'locataires actuel', 'checked': False},
        {"name": 'not_currently_tenant', 'label': 'anciens locataires', 'checked': False},
        {"name": 'has_a_debt', 'label': 'endettés', 'checked': False},
        {"name": 'has_no_debt', 'label': 'non endettés', 'checked': False},
    )

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
    
        if not request.user.is_staff:
            return redirect("not-staff-user")
        return super().dispatch(request, *args, **kwargs)

    @classmethod
    def apply_filters(cls, queryset, filter_form):

        filters = filter_form.cleaned_data

        if_currently_tenant_queryset = queryset.none() # local__isnull=False | local__isnull=True
        if_debt_queryset = queryset.none() # payment__paid=False | payment__paid=True exlude payment__paid=False

        if filters["currently_tenant"]:
            if_currently_tenant_queryset = if_currently_tenant_queryset | queryset.filter(local__isnull=False)
        
        if filters["not_currently_tenant"]:
            if_currently_tenant_queryset = if_currently_tenant_queryset | queryset.filter(local__isnull=True)
        
        if filters["has_a_debt"]:
            if_debt_queryset = if_debt_queryset | queryset.filter(payment__paid=False)
        
        if filters["has_no_debt"]:
            if_debt_queryset = if_debt_queryset | queryset.filter(payment__paid=True).exclude(payment__paid=False) | \
                                queryset.filter(payment__isnull=True)
        

        if if_currently_tenant_queryset.exists() and if_debt_queryset.exists():
            return (queryset & (if_currently_tenant_queryset & if_debt_queryset)).distinct()

        elif if_currently_tenant_queryset.exists():
            return (queryset & if_currently_tenant_queryset).distinct()
        
        elif if_debt_queryset.exists():
            return (queryset & if_debt_queryset).distinct()
        
        return queryset
            
    def apply_search(self, query, queryset):
        return (
                queryset.filter(first_name__icontains=query) | \
                queryset.filter(last_name__icontains=query) | \
                queryset.filter(local__tag_name__icontains=query) 
            ).distinct()

    def get(self, request, *args, **kwargs):

        # reset filters on queryset
        self.queryset = Renter.objects.all()

        self.search_query = request.GET.get("search-query", None)
        if self.search_query:
            self.queryset = self.apply_search(self.search_query, self.queryset)

        
        if request.GET.get("filter", None) is not None:

            self.filter_form = RenterFilterForm(request.GET)
            if self.filter_form.is_valid():
                self.queryset = self.apply_filters(self.queryset, self.filter_form)
                self.queryset_is_filtered = True
        else:
            self.queryset_is_filtered = False
            

        # # treat filters
        # for filter_item in self.filter_items:
        #     if request.GET.get(filter_item['name']):
        #         filter_item['checked'] = True 
        #     else:
        #         filter_item['checked'] = False

        # # apply filters if any filter is checked
        # if any([f["checked"] for f in self.filter_items]):
        #     self.queryset = self.apply_filters(self.queryset)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now_date"] = NOW_DATE_STR
        if self.search_query:
            context["search_query"] = self.search_query.strip()

        context["filter_form"] = self.filter_form

        context["filter_items"] = self.filter_items
        context["queryset_is_filtered"] = self.queryset_is_filtered
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
