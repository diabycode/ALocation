
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import AppLoginView, make_payment, app, logout_user
from . import settings


urlpatterns = [
    path('', app, name='app'),
    path('admin/', admin.site.urls),
    
    path('login/', AppLoginView.as_view(), name='login'),
    path('logout-user/', logout_user, name='logout-user'),
    path('make-payment/', make_payment, name='make_payment'),
    
    path('renters/', include('renter.urls')),
    path('locals/', include('local.urls')),

] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
