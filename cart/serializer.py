# cart/serializer.py
from rest_framework import serializers
from .models import CartItem, Cart
from menu.models import MenuItem
from decimal import Decimal


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'image']  # customize fields


class CartItemSerializer(serializers.ModelSerializer):
    item = MenuItemSerializer(source='menu_item', read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menu_item', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'item_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [ 'id', 'items', 'total_items', 'total_price']

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        return sum(item.quantity * float(item.menu_item.price) for item in obj.items.all())



        
