from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def user_is_active(redirect_url=None):
    '''
    Decorator for checking if the currently logged in user has is_active=True
    '''
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_active:
                messages.error(
                    request, 
                    "Nie można wyświelić żądanej strony, \
                        ponieważ konto jest deaktywowane." +
                    " Aby aktywować konto, należy opłacić składke.")
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator