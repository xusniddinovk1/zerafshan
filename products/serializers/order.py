from datetime import date
from rest_framework import serializers
from ..models import Order, OrderItem
from ..models.order import InstallmentPayment
from dateutil.relativedelta import relativedelta

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        read_only_fields = ['price']


class InstallmentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ['id', 'month_number', 'amount', 'due_date', 'is_paid']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    installments = InstallmentPaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'phone_number', 'payment_type', 'installment_months',
                  'total_price', 'items', 'installments', 'created_at']
        read_only_fields = ['user', 'total_price', 'installments', 'created_at']

    def validate(self, attrs):
        if attrs["payment_type"] == "installment" and not attrs.get("installment_months"):
            raise serializers.ValidationError("Muddatli to‘lovda oylar soni kiritilishi kerak.")
        if attrs["payment_type"] == "full" and attrs.get("installment_months"):
            raise serializers.ValidationError("To‘liq to‘lovda muddat kiritilmasligi kerak.")
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user
        order = Order.objects.create(user=user, **validated_data)

        total = 0
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]
            price = product.price * quantity
            total += price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

        order.total_price = total
        order.save()

        # Agar installment bo‘lsa -> jadval yaratamiz
        if order.payment_type == "installment":
            monthly_amount = round(total / order.installment_months, 2)
            today = date.today()
            for i in range(1, order.installment_months + 1):
                due_date = today + relativedelta(months=i)
                InstallmentPayment.objects.create(
                    order=order,
                    month_number=i,
                    amount=monthly_amount,
                    due_date=due_date
                )

        return order
