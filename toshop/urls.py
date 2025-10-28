from django.urls import path
from .views import root_view

urlpatterns = [path("", root_view, name="root")]
