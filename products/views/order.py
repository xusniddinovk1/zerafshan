from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Order
from ..serializers import OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permissions = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
