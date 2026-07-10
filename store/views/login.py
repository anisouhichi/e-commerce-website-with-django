from django.shortcuts import render, redirect
from django.views import View
from store.models.customer import Customer
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme

class Loginpage(View):
    def get(self, request):
        return HttpResponse("Login page")

class Login(View):
    def get(self, request):
        return_url = request.GET.get('return_url')
        if return_url:
            request.session['return_url'] = return_url
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                return_url = request.session.pop('return_url', None)
                if return_url and url_has_allowed_host_and_scheme(
                    return_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
                ):
                    return redirect(return_url)
                return redirect('homepage')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')
