from django.shortcuts import render, redirect
from store.models.products import Products
from store.models.categorie import Category
from django.views import View

class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')

        # ensure cart exists and keys are normalized to strings
        cart = request.session.get('cart', {})

        if product:
            pid = str(product)
            quantity = cart.get(pid, 0)

            if remove:
                # remove one or delete
                if quantity <= 1:
                    cart.pop(pid, None)
                else:
                    cart[pid] = quantity - 1
            else:
                # add/increment
                cart[pid] = quantity + 1

            # save back to session
            request.session['cart'] = cart

        # always redirect after POST (PRG pattern)
        return redirect('homepage')

    def get(self, request):
        # list products and categories (same as before)
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')

        if categoryID:
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            products = Products.get_all_products()

        data = {
            'products': products,
            'categories': categories
        }
        return render(request, 'index.html', data)

def store(request):
    return render(request, 'store.html')