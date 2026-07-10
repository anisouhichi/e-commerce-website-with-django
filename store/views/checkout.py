from django.shortcuts import redirect, render
from store.models.customer import Customer
from django.views import View
from store.models.products import Products
from store.models.orders import Order

class CheckOut(View):
    def get(self, request):
        return render(request, 'checkout.html')

    def post(self, request):
        address = (request.POST.get('address') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        customer = request.session.get('customer')
        cart = request.session.get('cart', {})
        if not customer:
            return redirect('login')
        if not cart or not address or not phone:
            return redirect('cart')
        products = Products.get_products_by_id(list(cart.keys()))

        for product in products:
            quantity = cart.get(str(product.id), 0)
            if quantity <= 0:
                continue
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=quantity)
            order.save()
        request.session['cart'] = {}

        return redirect('cart')
