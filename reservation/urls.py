from django.urls import path
from .views import reservations, reservation_detail

urlpatterns = [
    path(
        "",
        reservations,
        name="reservations",
    ),

   
    path(
        "<int:pk>/",
        reservation_detail,
        name="reservation-detail",
    ),
]