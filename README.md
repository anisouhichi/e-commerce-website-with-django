# Marketly

A small Django ecommerce storefront with customer signup, login, a session-backed shopping bag, checkout, and order history.

## Features

- Responsive storefront UI built with Django templates and CSS
- Product category filtering
- Customer authentication and protected cart, checkout, and order pages
- Session-backed bag and order checkout flow
- Django admin for managing categories, products, customers, and orders

## Run locally

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

To add products, create an admin account with `python manage.py createsuperuser`, then visit `http://127.0.0.1:8000/admin/`.

## Verification

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
```
