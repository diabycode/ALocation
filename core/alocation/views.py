
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.core.serializers import serialize

from .forms import CustomAuthenticationForm
from renter.models import Payment
from alocation.settings import NOW_DATE
from renter.models import Renter
from local.models import Local
from .utils import export
from renter.forms import RenterFilterForm
from renter.views import RenterListView
from local.views import LocalsListView
from local.forms import LocalFilterForm


def admin_panel(request):
    return render(request, "alocation/administration.html")


class AppLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "alocation/login.html"
    redirect_authenticated_user = True
    
    def get_redirect_url(self) -> str:
        return reverse("renter:renters-list")


@user_passes_test(lambda u: u.is_authenticated and u.is_staff, redirect_field_name="not-staff-user")
@login_required(redirect_field_name="login")
def app(request):
    return redirect("renter:renters-list")


@user_passes_test(lambda u: u.is_authenticated and not u.is_staff, redirect_field_name="not-staff-user")
@login_required()
def not_staff_user(request):
    return render(request, "alocation/not-staff-user.html")


@user_passes_test(lambda u: u.is_authenticated and u.is_staff, redirect_field_name="not-staff-user")
@login_required(redirect_field_name="login")
def make_payment(request):
    if request.method != "POST":
        raise Http404

    pk = request.POST.get("payment", None)
    print("payment selected", request.POST.get("payment", None))
    pk = request.POST.get("payment", None)
    payment = get_object_or_404(Payment, pk=pk)
    payment.paid = True
    payment.paid_at = NOW_DATE
    payment.save()

    return render(request, "alocation/payment_done.html", {"payment_id": pk, "renter_id": payment.renter.pk})
    

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")


@user_passes_test(lambda u: u.is_authenticated and u.is_staff, redirect_field_name="not-staff-user")
@login_required(redirect_field_name="login")
def export_renters(request):

    filter_form = RenterFilterForm
    hidden_filter_form = RenterFilterForm
    
    queryset = Renter.objects.all().order_by("last_name", "first_name")

    # filter statement
    if request.GET.get("filter", None) is not None:
        filter_form = filter_form(request.GET)
        hidden_filter_form = hidden_filter_form(request.GET)

        if filter_form.is_valid():
            queryset = RenterListView.apply_filters(queryset, filter_form)

    # export statement
    if request.GET.get("export_format", None) is not None:
        export_format = request.GET.get("export_format", None)

        # serialize Renter objects
        serialized_data = serialize("json", queryset)
        response = None

        response = export(
            serialized_data=serialized_data,
            export_type=export_format,
            sheet_title="Locataires",
            filename="locataires",
        )

        return response

    
    context = {
        "objects": queryset,
        "filter_form": filter_form,
        "hidden_filter_form": hidden_filter_form,
    }
    return render(request, "alocation/export_renters.html", context)


@user_passes_test(lambda u: u.is_authenticated and u.is_staff, redirect_field_name="not-staff-user")
@login_required(redirect_field_name="login")
def export_locals(request):

    queryset = Local.objects.all().order_by("tag_name")
    filter_form = LocalFilterForm
    hidden_filter_form = LocalFilterForm

    if request.GET.get("filter", None) is not None:
        filter_form = filter_form(request.GET)
        hidden_filter_form = hidden_filter_form(request.GET)

        if filter_form.is_valid():
            queryset = LocalsListView.apply_filters(queryset, filter_form)

    if request.GET.get("export_format", None) is not None:
        export_format = request.GET.get("export_format", None)

        # serialize Renter objects
        serialized_data = serialize("json", queryset)
        response = None

        response = export(
            serialized_data=serialized_data,
            export_type=export_format,
            sheet_title="Locaux",
            filename="Locaux",
        )
        return response    

    
    context = {
        "objects": queryset,
        "filter_form": filter_form,
        "hidden_filter_form": hidden_filter_form,
    }
    return render(request, "alocation/export_locals.html", context)




