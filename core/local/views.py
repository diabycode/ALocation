from typing import Any, Dict
from django.http import Http404
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType


from .models import Local
from renter.models import Renter
from alocation.settings import NOW_DATE_STR
from .forms import LocalForm, LocalFilterForm


class LocalsListView(ListView, LoginRequiredMixin):
    queryset = Local.objects.order_by("-added_at")
    template_name = "local/locals-list.html"
    context_object_name = "locals_list"
    search_query = None
    paginate_by = 7
    filter_form = LocalFilterForm()  

    queryset_is_filtered = False  

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not request.user.is_staff:
            return redirect("not-staff-user")
        return super().dispatch(request, *args, **kwargs)

    def apply_search(self, query, queryset):
        return (
                queryset.filter(tag_name__icontains=query) |\
                queryset.filter(current_tenant__last_name__icontains=query) |\
                queryset.filter(current_tenant__first_name__icontains=query) |\
                queryset.filter(address__icontains=query) 
            ).distinct()

    @classmethod
    def apply_filters(cls, queryset, filter_form):
        # filters name ( has_a_tenant, has_no_tenant, has_a_debt, has_no_debt )

        filters = filter_form.cleaned_data

        if_has_a_tenant_queryset = queryset.none()
        if_has_a_debt_queryset = queryset.none()

        if filters["has_a_tenant"]:
            if_has_a_tenant_queryset = if_has_a_tenant_queryset | queryset.filter(current_tenant__isnull=False)

        if filters["has_no_tenant"]:
            if_has_a_tenant_queryset = if_has_a_tenant_queryset | queryset.filter(current_tenant__isnull=True)

        if filters["has_a_debt"]:
            if_has_a_debt_queryset = if_has_a_debt_queryset | queryset.filter(payment__paid=False)

        if filters["has_no_debt"]:
            if_has_a_debt_queryset = if_has_a_debt_queryset | queryset.filter(payment__paid=True).exclude(payment__paid=False)

        if if_has_a_tenant_queryset.exists() and if_has_a_debt_queryset.exists():
            return (queryset & (if_has_a_tenant_queryset & if_has_a_debt_queryset)).distinct()
        
        if if_has_a_tenant_queryset.exists():
            return (queryset & if_has_a_tenant_queryset).distinct()
        
        if if_has_a_debt_queryset.exists():
            return (queryset & if_has_a_debt_queryset).distinct()

        return queryset

    def get(self, request, *args, **kwargs):

        # reset all filters
        self.queryset = Local.objects.order_by("-added_at")

        self.search_query = request.GET.get("search-query")
        if self.search_query:
            self.queryset = self.apply_search(self.search_query, self.queryset)

        if request.GET.get("filter", None) is not None:

            self.filter_form = LocalFilterForm(request.GET)
            if self.filter_form.is_valid():
                self.queryset = self.apply_filters(self.queryset, self.filter_form)
                self.queryset_is_filtered = True
        else:
            self.queryset_is_filtered = False

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["now_date"] = NOW_DATE_STR
        context["search_query"] = self.search_query
        context["filter_form"] = self.filter_form
        context["queryset_is_filtered"] = self.queryset_is_filtered

        return context

    
class LocalDetailsView(DetailView):
    model = Local
    template_name = "local/local-details.html"
    context_object_name = "local"
    extra_context = {'now_date': NOW_DATE_STR}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payments_list"] = (self.get_object()).payment_set.all()
        context["renters_list"] = Renter.objects.all().order_by("last_name")
        return context


class LocalDeleteView(DeleteView):
    model = Local
    template_name = "local/local__confirm_delete.html"
    context_object_name = "local"
    extra_context = {'now_date': NOW_DATE_STR}
    
    def get_success_url(self) -> str:
        return reverse("local:locals-list")

    def form_valid(self, form):
        response = super().form_valid(form)

        # Create a log entry
        LogEntry.objects.create(
            user=self.request.user,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_repr=str(self.object),
            action_flag=DELETION,
            change_message=f"Local '{self.object.tag_name}' supprimé",
        )

        return response


class LocalAddView(CreateView):
    model = Local
    template_name = "local/local-add.html"
    form_class = LocalForm
    success_url = reverse_lazy("local:locals-list")
    extra_context = {'now_date': NOW_DATE_STR}

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Create a log entry
        LogEntry.objects.create(
            user=self.request.user,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_repr=str(self.object),
            object_id=self.object.pk,
            action_flag=ADDITION,
            change_message=f"Local '{self.object.tag_name}' ajouté",
        )
        
        return response


class LocalEditView(UpdateView):
    model = Local
    form_class = LocalForm
    template_name = "local/local-edit.html"
    extra_context = {'now_date': NOW_DATE_STR}

    def get_success_url(self) -> str:
        success_url = reverse("local:local-details", kwargs={'pk': (self.get_object()).pk}) 
        return success_url

    def get_changed_fields(self, form):
        changes = {}
        for field in form.changed_data:
            changes[field]  = form.cleaned_data[field]
        
        return changes
    
    def form_valid(self, form):
        old_object = self.get_object()
    
        response = super().form_valid(form)

        changes = self.get_changed_fields(form)
        changes_str = (
            f"[{Local._meta.get_field(change_field).verbose_name}] : ('{getattr(old_object, change_field)}', '{changes[change_field]}')"
            for change_field in changes
        )

        # Create a log entry
        LogEntry.objects.create(
            user=self.request.user,
            content_type_id=ContentType.objects.get_for_model(self.object).pk,
            object_repr=str(self.object),
            object_id=self.object.pk,
            action_flag=CHANGE,
            change_message=f"Champs modifié(s) [{', '.join(changes_str)}]",
        )

        return response


def assign_local_to_renter(request):
    if request.method == "POST":
        renter = Renter.objects.get(pk=request.POST.get("renter_id"))
        locals_selected = request.POST.getlist("locals_selected")

        for id in locals_selected:
            renter.assign_local(
                local=Local.objects.get(pk=id)
            )

        return redirect("renter:renter-details", pk=renter.pk)
    return Http404()


def change_renter(request):

    if request.method == "POST":
        
        local = Local.objects.get(pk=request.POST.get("local"))

        if request.POST.get('renter') == "none":
            local.unasign_tenant()  # unassign local 
        else: 
            local.unasign_tenant()

            renter = Renter.objects.get(pk=request.POST.get("renter"))
            renter.assign_local(local=local)

        return redirect("local:local-details", pk=local.pk)
    return Http404()