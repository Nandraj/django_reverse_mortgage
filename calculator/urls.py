from django.urls import path
from .views import mortgage_calculator


urlpatterns = [
    path("", mortgage_calculator, name="mortgage_calculator"),
]
