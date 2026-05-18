from django.contrib import admin

# Register your models here.

from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "reservation_date",
        "reservation_time",
        "guests",
        "status",
    )

    list_filter = ("status", "reservation_date")
    search_fields = ("full_name", "email", "phone")