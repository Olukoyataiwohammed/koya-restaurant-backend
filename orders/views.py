from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
import requests
import uuid
import hashlib
import hmac
import json

from cart.models import Cart
from .models import Order, OrderItem, Payment
from .serializer import OrderSerializer, CreateOrderSerializer, PaymentSerializer


# -----------------------------------------
# CREATE ORDER (Guest + Auth)
# -----------------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    serializer = CreateOrderSerializer(
        data=request.data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    order = serializer.save()

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


# -----------------------------------------
# LIST USER ORDERS
# -----------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# -----------------------------------------
# ORDER DETAIL (SECURED)
# -----------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found"}, status=404)

    serializer = OrderSerializer(order)
    return Response(serializer.data)


# -----------------------------------------
# CREATE PAYMENT (GENERATE REFERENCE)
# -----------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    data = request.data

    try:
        order = Order.objects.get(id=data.get('order'), user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    # Prevent duplicate payments
    if Payment.objects.filter(order=order).exists():
        return Response({"error": "Payment already exists"}, status=400)

    # ✅ Generate unique reference
    reference = str(uuid.uuid4())

    payment = Payment.objects.create(
        order=order,
        amount=order.total_price,
        method=data.get('method', 'CARD'),
        transaction_id=reference,
        status='PENDING'
    )

    return Response({
        "message": "Payment created",
        "reference": reference,
        "amount": payment.amount,
        "email": request.user.email
    }, status=201)


# -----------------------------------------
# OPTIONAL: VERIFY PAYMENT (Frontend Trigger)
# -----------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    reference = request.data.get("reference")

    if not reference:
        return Response({"error": "Reference required"}, status=400)

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if not data.get("status"):
        return Response({"error": "Verification failed"}, status=400)

    payment_data = data.get("data")

    if payment_data.get("status") != "success":
        return Response({"error": "Payment not successful"}, status=400)

    try:
        payment = Payment.objects.get(transaction_id=reference)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    order = payment.order

    # Validate amount
    amount = payment_data.get("amount") / 100
    if float(amount) != float(order.total_price):
        return Response({"error": "Amount mismatch"}, status=400)

    payment.status = "COMPLETED"
    payment.save()

    order.is_paid = True
    order.save()

    return Response({"message": "Payment verified"})


# -----------------------------------------
# PAYSTACK WEBHOOK (SECURE)
# -----------------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def payment_webhook(request):
    payload = request.body
    signature = request.headers.get('x-paystack-signature')

    # ✅ Verify Paystack signature
    computed_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
        payload,
        hashlib.sha512
    ).hexdigest()

    if computed_signature != signature:
        return Response({"error": "Invalid signature"}, status=400)

    data = json.loads(payload)

    # Only handle successful payments
    if data.get("event") != "charge.success":
        return Response({"message": "Ignored"}, status=200)

    payment_data = data.get("data")
    reference = payment_data.get("reference")
    amount = payment_data.get("amount") / 100

    try:
        payment = Payment.objects.get(transaction_id=reference)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    order = payment.order

    # Validate amount
    if float(amount) != float(order.total_price):
        return Response({"error": "Amount mismatch"}, status=400)

    # Update payment
    payment.status = "COMPLETED"
    payment.save()

    # Mark order as paid
    order.is_paid = True
    order.save()

    return Response({"message": "Webhook processed"})