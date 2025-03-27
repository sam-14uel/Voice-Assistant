from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import SubscriptionManager

def subscription_required(allowed_plans=["basic", "standard"]):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            try:
                manager = SubscriptionManager.objects.get(user=request.user)
                if manager.plan not in allowed_plans or not manager.active:
                    raise PermissionDenied("Feature requires a paid subscription")
            except SubscriptionManager.DoesNotExist:
                raise PermissionDenied("Feature requires a paid subscription")
           
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator