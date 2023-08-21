from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from .forms import CustomAuthenticationForm
from renter.models import Payment
from alocation.settings import NOW_DATE


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


