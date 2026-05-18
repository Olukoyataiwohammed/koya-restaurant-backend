from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Reservation
from .serializer import ReservationSerializer


@api_view(["POST"])
def create_reservation(request):
    serializer = ReservationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "message": "Reservation created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )

@api_view(["GET", "POST"])
def reservations(request):

    if request.method == "GET":
        reservations = Reservation.objects.all().order_by("-created_at")
        serializer = ReservationSerializer(reservations, many=True)

        return Response(serializer.data)

    if request.method == "POST":
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    




@api_view(["GET", "PUT", "DELETE"])
def reservation_detail(request, pk):

    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == "GET":
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ReservationSerializer(
            reservation,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        reservation.delete()

        return Response(
            {"message": "Reservation deleted"},
            status=204,
        )