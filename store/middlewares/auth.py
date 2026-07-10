from functools import wraps

from django.shortcuts import redirect


def auth_middleware(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('customer'):
            return redirect(f"/login/?return_url={request.get_full_path()}")
        return view_func(request, *args, **kwargs)
    return wrapper
