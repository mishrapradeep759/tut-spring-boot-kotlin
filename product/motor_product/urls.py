from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('management/', include("motor_product.upload_panel.urls")),
]