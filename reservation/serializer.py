from rest_framework import serializers
from datetime import date, datetime, time

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = "__all__"

    # Prevent past dates
    def validate_reservation_date(self, value):

        if value < date.today():
            raise serializers.ValidationError(
                "Reservation date cannot be in the past."
            )

        return value

    # Example restaurant opening hours validation
    def validate_reservation_time(self, value):

        opening_time = time(9, 0)   # 9:00 AM
        closing_time = time(22, 0) # 10:00 PM

        if value < opening_time or value > closing_time:
            raise serializers.ValidationError(
                "Reservations are only available between 9AM and 10PM."
            )

        return value

    # Validate guest count
    def validate_guests(self, value):

        if value < 1:
            raise serializers.ValidationError(
                "Guests must be at least 1."
            )

        if value > 20:
            raise serializers.ValidationError(
                "Maximum reservation is 20 guests."
            )

        return value