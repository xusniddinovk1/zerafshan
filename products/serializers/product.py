from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


class InstallmentPayView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            installment = InstallmentPayment.objects.get(pk=pk, order__user=request.user)
        except InstallmentPayment.DoesNotExist:
            return Response({"error": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        if installment.is_paid:
            return Response({"message": "Bu to‘lov allaqachon qilingan"}, status=status.HTTP_400_BAD_REQUEST)

        installment.is_paid = True
        installment.save()
        return Response({"message": f"{installment.month_number}-oy to‘lov qabul qilindi ✅"})
