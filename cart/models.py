# cart/models.py
from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username if self.user else self.session_key


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE
    )
    menu_item = models.ForeignKey(
        MenuItem,
        related_name="cart_items",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)