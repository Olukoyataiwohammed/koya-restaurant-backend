from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
from django.utils import timezone



class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

   
    customer_name = models.CharField(max_length=100 , default="Guest")
    customer_phone = models.CharField(max_length=20)
    delivery_address = models.TextField(blank=True)

    DELIVERY_CHOICES = [
        ("DELIVERY", "Delivery"),
        ("PICKUP", "Pickup"),
    ]
    delivery_method = models.CharField(
        max_length=10,
        choices=DELIVERY_CHOICES,
        default="DELIVERY"
    )

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("PREPARING", "Preparing"),
        ("ON_THE_WAY", "On the way"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    payment_method = models.CharField(max_length=20, default="COD")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"




class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"






class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CARD', 'Card'),
        ('CASH', 'Cash'),
        ('PAYPAL', 'PayPal'),
        ('BANK', 'Bank Transfer'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    order = models.OneToOneField(
        'Order',  # assuming your order model is named Order
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.order.id} - {self.status} - {self.amount}"

