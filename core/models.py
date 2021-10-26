from django.db import models
from django.conf import settings


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return f"item - {self.title}"


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_start = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(False)

    def __str__(self):
        return f"{self.user}'s order"