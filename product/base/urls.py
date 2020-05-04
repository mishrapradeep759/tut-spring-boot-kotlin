from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('motor/', include('motor_product.urls')),
    path('admin/', admin.site.urls),
]