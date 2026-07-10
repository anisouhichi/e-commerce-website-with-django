from django.shortcuts import render
from django.views import View

from store.models.products import Products


class Cart(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Products.get_products_by_id(cart.keys())
        cart_items = [
            {'product': product, 'quantity': cart.get(str(product.id), 0)}
            for product in products
        ]
        return render(request, 'cart.html', {'cart_items': cart_items})
