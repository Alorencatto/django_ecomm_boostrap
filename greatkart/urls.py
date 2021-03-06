from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views
from .settings import MEDIA_ROOT

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name="home"),
                  path('store/', include('store.urls')),
                  path('cart/', include('carts.urls')),
                  path('crudapp/', include('crudapp.urls')),

              ] + static(settings.MEDIA_URL, document_root=MEDIA_ROOT)
