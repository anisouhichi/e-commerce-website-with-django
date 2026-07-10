from django.test import TestCase

from store.models import Category, Customer, Order, Products


class StoreFlowTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Books')
        self.product = Products.objects.create(
            name='Django Book', price=1200, category=category, image='book.jpg'
        )
        self.customer = Customer(
            first_name='Ada', last_name='Lovelace', phone='1234567890',
            email='ada@example.com', password='secure-password',
        )
        self.customer.register()

    def test_home_adds_product_to_cart(self):
        response = self.client.post('/', {'product': self.product.id})
        self.assertRedirects(response, '/')
        self.assertEqual(self.client.session['cart'], {str(self.product.id): 1})

    def test_cart_requires_login(self):
        response = self.client.get('/cart/')
        self.assertRedirects(response, '/login/?return_url=/cart/')

    def test_login_checkout_and_orders_flow(self):
        response = self.client.post('/login/', {
            'email': self.customer.email, 'password': 'secure-password',
        })
        self.assertRedirects(response, '/')

        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()
        response = self.client.post('/check-out/', {
            'address': '1 Main Street', 'phone': '1234567890',
        })
        self.assertRedirects(response, '/cart/')
        order = Order.objects.get()
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(self.client.session['cart'], {})

        response = self.client.get('/orders/')
        self.assertContains(response, 'Django Book')
