from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CartItem
from .serializer import CartSerializer, CartItemSerializer
from .utils import get_or_create_cart


@api_view(['GET'])
@permission_classes([AllowAny])
def get_cart_items(request):
    cart = get_or_create_cart(request)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_item_to_cart(request):
    cart = get_or_create_cart(request)

    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.validated_data['menu_item']
        qty = serializer.validated_data.get('quantity', 1)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=item
        )
        if not created:
            cart_item.quantity += qty
        else:
            cart_item.quantity = qty
        cart_item.save()

        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def remove_item_from_cart(request, item_id):
    cart = get_or_create_cart(request)

    try:
        cart_item = CartItem.objects.get(cart=cart, id=item_id)
        cart_item.delete()
        return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
