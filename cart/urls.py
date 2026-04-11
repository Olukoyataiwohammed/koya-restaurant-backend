from django.urls import path
from .views import (
    add_item_to_cart,
    get_cart_items,
    remove_item_from_cart
)

urlpatterns = [
    path("add-items/", add_item_to_cart, name="add-item"),
    path("get-items/", get_cart_items, name="get-cart"),
    path("delete-item/<int:item_id>/", remove_item_from_cart, name="delete-item"),
]
