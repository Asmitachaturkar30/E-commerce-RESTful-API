from django.db import models

class Product(models.Model):
    productId = models.CharField(max_length=50, unique=True)
    productName = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stockQuantity = models.PositiveIntegerField(default=0)
    imageUrl = models.URLField(blank=True, null=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName
