from functools import wraps
from django.shortcuts import redirect
from django.conf import settings

def userprofile_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user_id exists in session (logged in via OTP)
        if request.session.get('user_id'):
            return view_func(request, *args, **kwargs)
        # Redirect to your custom login page
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    return wrapper
