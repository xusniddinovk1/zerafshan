from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Category, Product
from ..models.order import InstallmentPayment
from ..permissions import IsInstallmentOwner
from ..serializers import CategorySerializer, ProductSerializer, InstallmentPaymentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class InstallmentPayView(generics.UpdateAPIView):
    queryset = InstallmentPayment.objects.all()
    serializer_class = InstallmentPaymentSerializer
    permission_classes = [IsAuthenticated, IsInstallmentOwner]

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
