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


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Order(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items       = models.ManyToManyField(OrderItem)
    order_start = models.DateTimeField(auto_now_add=True)
    order_date  = models.DateTimeField()
    ordered     = models.BooleanField(False)

    def __str__(self):
        return f"{self.user}'s order"
