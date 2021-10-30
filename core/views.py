from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from .models import Item, Order, OrderItem
from django.utils import timezone
from django.contrib import messages

class HomeView(ListView):
    model         = Item
    template_name = 'index.html'
    

class ItemDetailView(DetailView):
    model         = Item
    template_name = 'product.html'


def checkout(request):
    return render(request, 'checkout.html')


def add_item_to_card(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item's quantity increased by one")
            return redirect('product', slug=item.slug)
        else:
            order.items.add(order_item)  
            messages.info(request, "Item's been added to the cart")
            return redirect('product', slug=item.slug) 
    else:
        order = Order.objects.create(user=request.user, order_date=timezone.now())
        order.items.add(order_item)
        messages.info(request, "Order's been placed and item added to the cart")
        return redirect('product', slug=item.slug) 


def remove_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)  
            messages.info(request, "Item's been removed from the cart")
            return redirect('product', slug=item.slug) 
        else:
           messages.info(request, "Item's not in the cart")
           return redirect('product', slug=item.slug) 
    else:
        messages.info(request, "You don't have an active order")
        return redirect('product', slug=item.slug)