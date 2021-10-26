from django.shortcuts import render
from .models import Item


def items_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'index.html', context)
