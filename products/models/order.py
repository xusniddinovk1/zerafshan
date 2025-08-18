from django.db import models
from users.models import CustomUser, phone_regex
from .product import Product


class Order(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('full', 'Full payment'),
        ('installment', 'Installment payment')
    ]

    INSTALLMENT_CHOICES = [
        (3, '3'),
        (6, '6'),
        (9, '9'),
        (12, '12'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, validators=[phone_regex], unique=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    installment_months = models.PositiveIntegerField(choices=INSTALLMENT_CHOICES)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#Order {self.id} by {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=3)

    def __str__(self):
        return f'{self.product.title} x {self.quantity}'


class InstallmentPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="installments")
    month_number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order} - {self.month_number}-oy ({'To‘langan' if self.is_paid else 'Kutilmoqda'})"
