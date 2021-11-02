from django.db import models
from django.conf import settings
from django.urls import reverse


CATEGORY_CHOISES = [
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
]

LABEL_CHOISES = [
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
]


class Item(models.Model):
    title          = models.CharField(max_length=100)
    price          = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category       = models.CharField(choices=CATEGORY_CHOISES, max_length=2)
    label          = models.CharField(choices=LABEL_CHOISES, max_length=2)
    slug           = models.SlugField()
    description    = models.TextField()

    def __str__(self):
        return f"item - {self.title}"

    def get_absolute_url(self):
        return reverse('product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('add_to_card', kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item        = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=1)
    ordered     = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def get_item_total_price(self):
        return self.quantity * self.item.price

    def get_discounted_item_total_price(self):
        return self.quantity * self.item.discount_price

    def get_saved_amount(self):
        return self.get_item_total_price() - self.get_discounted_item_total_price()

    def get_total_item(self):
        if self.item.discount_price: return self.get_discounted_item_total_price()

        return self.get_item_total_price()


class Order(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items       = models.ManyToManyField(OrderItem)
    order_start = models.DateTimeField(auto_now_add=True)
    order_date  = models.DateTimeField()
    ordered     = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s order"

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_total_item()
        return total

