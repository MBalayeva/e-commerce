from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<str:slug>', views.ItemDetailView.as_view(), name='product'),
    path('add-to-card/<str:slug>', views.add_item_to_card, name='add_to_card'),
    path('remove-from-card/<str:slug>', views.remove_item_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
