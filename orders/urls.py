from django.urls import path
from . import views



urlpatterns = [
    path("create/", views.create_order, name="create_order"),
    path("", views.list_orders, name="list_orders"),      
    path("<int:pk>/", views.order_detail, name="order_detail"),
    path('payments/', views.create_payment, name='create_payment'),
    path('payments/webhook/', views.payment_webhook, name='payment_webhook'),
]

