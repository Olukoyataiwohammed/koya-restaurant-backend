from rest_framework import serializers

from .models import Category,MenuItem

class CategorySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["createdAt"]


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"
        read_only_fields = ["createdAt"]


