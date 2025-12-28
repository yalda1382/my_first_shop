from rest_framework import generics
from orders.models import Order
from .serializers import OrderSerializer

class OrderListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer