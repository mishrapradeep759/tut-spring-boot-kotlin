from django.urls import path

from . import views as upload_panel_views

urlpatterns = [
    path('upload_vehicle/', upload_panel_views.dashboard, name='dashboard'),
]