from rest_framework import serializers
from .models import Order, OrderItem , Payment
from cart.models import Cart



class CreateOrderSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100)
    customer_phone = serializers.CharField(max_length=20)
    delivery_address = serializers.CharField(required=False, allow_blank=True)
    delivery_method = serializers.ChoiceField(choices=["DELIVERY", "PICKUP"])
    payment_method = serializers.CharField(default="COD")

    def validate(self, data):
        if data["delivery_method"] == "DELIVERY" and not data.get("delivery_address"):
            raise serializers.ValidationError(
                {"delivery_address": "Delivery address is required"}
            )
        return data

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user if request.user.is_authenticated else None

        # Ensure session exists for guests
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        # Get cart (user or guest)
        cart = Cart.objects.filter(
            user=user,
            session_key=None if user else session_key
        ).first()

        if not cart or not cart.items.exists():
            raise serializers.ValidationError("Cart is empty")

        # Create order
        order = Order.objects.create(
            user=user,
            customer_name=validated_data["customer_name"],
            customer_phone=validated_data["customer_phone"],
            delivery_address=validated_data.get("delivery_address", ""),
            delivery_method=validated_data["delivery_method"],
            payment_method=validated_data["payment_method"],
        )

        # Move cart items → order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                item=cart_item.menu_item,
                quantity=cart_item.quantity,
            )

        # Clear cart
        cart.items.all().delete()

        return order


class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name")
    item_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["item_name", "quantity", "item_price"]

    def get_item_price(self, obj):
        return float(getattr(obj.item, "price", 0) or 0)



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'method', 'status', 'transaction_id', 'created_at']
        read_only_fields = ['id', 'created_at', 'status']  # status can be updated by backend only if needed





class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "customer_name",
            "customer_phone",
            "delivery_address",
            "delivery_method",
            "payment_method",
            "items",
            "total_price",
            "payment",
            "created_at",
        ]

    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            # ensure price is numeric
            price = getattr(item.item, "price", 0) or 0
            total += float(price) * item.quantity
        return total



