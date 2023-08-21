from typing import Any, Dict
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render

from .models import Local
from renter.models import Renter
from alocation.settings import NOW_DATE_STR


class LocalsListView(ListView, LoginRequiredMixin):
    queryset = Local.objects.order_by("-added_at")
    template_name = "local/locals-list.html"
    context_object_name = "locals_list"
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

    
class LocalDetailsView(DetailView):
    model = Local
    template_name = "local/local-details.html"
    context_object_name = "local"
    extra_context = {'now_date': NOW_DATE_STR}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payments_list"] = (self.get_object()).payment_set.all()
        return context


class LocalDeleteView(DeleteView):
    model = Local
    template_name = "local/local__confirm_delete.html"
    context_object_name = "local"
    extra_context = {'now_date': NOW_DATE_STR}
    success_url = "/"


"""
def local_delete_view(request, pk):
    local = Renter.objects.get(pk=pk)

    if request.method == "POST":
        print("DELETED !!")
        return redirect("/")
    
    context = {
        'local': local,
    }
    return render(request, "local/local__confirm_delete.html", context)
"""


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


