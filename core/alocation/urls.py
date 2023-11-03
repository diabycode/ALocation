
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import *
from . import settings


urlpatterns = [
    path('', app, name='app'),
    path('a-administration/', admin.site.urls),
    
    path('login/', AppLoginView.as_view(), name='login'),
    path('logout-user/', logout_user, name='logout-user'),
    path('make-payment/', make_payment, name='make_payment'),
    path('not-staff-user/', not_staff_user, name='not-staff-user'),
    
    path('export/renters/', export_renters, name='export_renters'),
    path('export/locals/', export_locals, name='export_locals'),

    path('renters/', include('renter.urls')),
    path('locals/', include('local.urls')),

] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
