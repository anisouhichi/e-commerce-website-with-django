from django.shortcuts import redirect, render
from django.views import View

from store.models.categorie import Category
from store.models.products import Products


class Index(View):
    def post(self, request):
        product_id = request.POST.get('product')
        cart = request.session.get('cart', {})

        if product_id:
            product_id = str(product_id)
            quantity = cart.get(product_id, 0)
            if request.POST.get('remove'):
                if quantity <= 1:
                    cart.pop(product_id, None)
                else:
                    cart[product_id] = quantity - 1
            else:
                cart[product_id] = quantity + 1
            request.session['cart'] = cart
        return redirect('homepage')

    def get(self, request):
        return store(request)


def store(request):
    request.session.setdefault('cart', {})
    category_id = request.GET.get('category')
    products = (
        Products.get_all_products_by_categoryid(category_id)
        if category_id else Products.get_all_products()
    )
    return render(request, 'index.html', {
        'products': products,
        'categories': Category.get_all_categories(),
    })
