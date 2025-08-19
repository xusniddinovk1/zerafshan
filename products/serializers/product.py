from rest_framework import serializers, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import InstallmentPaymentSerializer
from ..models import Category, Product
from ..models.order import InstallmentPayment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'category', 'price', 'stock', 'created_at']


class InstallmentPayView(generics.UpdateAPIView):
    queryset = InstallmentPayment.objects.all()
    serializer_class = InstallmentPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(order__user=self.request.user)

    def update(self, request, *args, **kwargs):
        installment = self.get_object()

        if installment.is_paid:
            return Response(
                {"detail": "Bu oy uchun to‘lov allaqachon amalga oshirilgan."},
                status=status.HTTP_400_BAD_REQUEST
            )

        installment.is_paid = True
        installment.save()

        return Response(
            {"detail": f"{installment.month_number}-oy uchun to‘lov qabul qilindi."},
            status=status.HTTP_200_OK
        )
