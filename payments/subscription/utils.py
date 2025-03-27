from django.http import JsonResponse
from djstripe.models import Customer, Subscription, Price
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response

@login_required
@require_POST
def subscribe(request):
    user = request.user
    # Retrieve or create the Stripe customer for the user
    customer, created = Customer.get_or_create(subscriber=user)

    # The plan/price ID should be passed from the frontend (e.g., via a form or AJAX request)
    plan_id = request.POST.get("plan_id")
    if not plan_id:
        return JsonResponse({"error": "Plan ID is required."}, status=400)

    try:
        price = Price.objects.get(id=plan_id)
    except Price.DoesNotExist:
        return JsonResponse({"error": "Invalid plan ID."}, status=400)

    # If it's a free tier (price.amount == 0) or if you want to bypass checkout for trial
    if price.unit_amount == 0:
        subscription = Subscription.objects.create(
            customer=customer,
            items=[{"price": price.id}],
        )
        return JsonResponse({"subscription": subscription.id, "status": "subscribed"})
   
    # For paid plans, you would typically create a Checkout Session
    # (Note: You might want to use stripe.checkout.Session.create here with dj-stripe integration.)
    import stripe
    stripe.api_key = "your_stripe_test_secret_key"
    session = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=["card"],
        line_items=[{
            "price": price.id,
            "quantity": 1,
        }],
        mode="subscription",
        success_url="https://yourdomain.com/success/",
        cancel_url="https://yourdomain.com/cancel/",
    )
    return JsonResponse({"checkout_session": session, "status": "pending_payment"})

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from djstripe.models import Customer, Subscription

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@login_required
def subscription_details(request):
    """
    Retrieve the current subscription details for the logged-in user.
    """
    # Ensure customer exists or create one
    customer, created = Customer.get_or_create(subscriber=request.user)
    subscriptions = Subscription.objects.filter(customer=customer)
   
    # Convert subscriptions to a simple dictionary format (or JSON as needed)
    subscription_data = [sub.to_dict() for sub in subscriptions]
   
    return JsonResponse({"subscriptions": subscription_data})

from django.views.decorators.http import require_POST

@login_required
@require_POST
def update_subscription(request):
    """
    Update the user's subscription by switching to a new plan.
    The new Price ID should be provided in the POST data as 'new_price_id'.
    """
    new_price_id = request.POST.get("new_price_id")
    if not new_price_id:
        return JsonResponse({"error": "New plan ID is required."}, status=400)
   
    customer, _ = Customer.get_or_create(subscriber=request.user)
    subscriptions = Subscription.objects.filter(customer=customer, status="active")
    if not subscriptions:
        return JsonResponse({"error": "No active subscription found."}, status=400)
   
    # For simplicity, update the first active subscription
    for subscription in subscriptions:
        subscription = subscription
   
    try:
        # Update subscription with new plan. Prorations will be applied automatically.
        updated_subscription = stripe.Subscription.modify(
            subscription.id,
            items=[{
                "id": subscription.id,
                "price": new_price_id,
            }],
            proration_behavior="create_prorations",
        )
        return JsonResponse({"subscription": updated_subscription})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
@require_POST
def cancel_subscription(request):
    """
    Cancel the user's active subscription. The cancellation is set to occur at the period end.
    """
    customer, _ = Customer.get_or_create(subscriber=request.user)
    subscriptions = Subscription.objects.filter(customer=customer, status="active")
    if not subscriptions:
        return JsonResponse({"error": "No active subscription found."}, status=400)
   
    for subscription in subscriptions:
        subscription = subscription
   
    try:
        # Cancel at period end to avoid immediate service disruption
        canceled_subscription = stripe.Subscription.modify(
            subscription.id,
            cancel_at_period_end=True,
        )
        return JsonResponse({"subscription": canceled_subscription})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



# from django.shortcuts import redirect, render
# from django.contrib.auth.decorators import login_required
# from djstripe.models import Subscription, Price
# from .models import SubscriptionManager

# @login_required
# def subscription_dashboard(request):
#     user = request.user
#     try:
#         subscription = Subscription.objects.get(customer=user.stripe_customer)
#         manager = SubscriptionManager.objects.get(user=user)
#     except Subscription.DoesNotExist:
#         manager = SubscriptionManager.objects.get_or_create(user=user)[0]
#         subscription = None
   
#     return render(request, "subscription_dashboard.html", {
#         "subscription": subscription,
#         "manager": manager,
#         "plans": Price.objects.filter(product__metadata__type__in=["basic", "standard"])
#     })

# @login_required
# def cancel_subscription(request):
#     user = request.user
#     try:
#         subscription = Subscription.objects.get(customer=user.stripe_customer)
#         subscription.delete()
#         manager = SubscriptionManager.objects.get(user=user)
#         manager.plan = "free"
#         manager.active = False
#         manager.save()
#         return redirect("subscription_dashboard")
#     except Subscription.DoesNotExist:
#         return redirect("subscription_dashboard")

# @login_required
# def upgrade_subscription(request, plan):
#     user = request.user
#     try:
#         subscription = Subscription.objects.get(customer=user.stripe_customer)
#         price = Price.objects.get(id=plan)
       
#         # Cancel current subscription
#         subscription.delete()
       
#         # Create new subscription
#         new_subscription = Subscription.objects.create(
#             customer=user.stripe_customer,
#             items=[{"price": price.id}],
#             trial_period_days=7 if price.product.metadata["type"] == "basic" else 14
#         )
       
#         manager = SubscriptionManager.objects.get(user=user)
#         manager.plan = price.product.metadata["type"]
#         manager.active = True
#         manager.save()
#         return redirect("subscription_dashboard")
       
#     except Exception as e:
#         messages.error(request, str(e))
#         return redirect("subscription_dashboard")

# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required
# from djstripe.models import Customer, Subscription
# from .models import ReferralCode, Referral

# @login_required
# def generate_referral_code(request):
#     code = ReferralCode.objects.create(
#         code=f"REF{request.user.id}{datetime.now().timestamp()}",
#         user=request.user
#     )
#     return redirect("dashboard")

# @login_required
# def apply_referral_code(request, code):
#     try:
#         referral_code = ReferralCode.objects.get(code=code)
#         if referral_code.used:
#             messages.error(request, "Code already used")
#             return redirect("signup")
           
#         # Create referral entry
#         Referral.objects.create(
#             referrer=referral_code.user,
#             referee=request.user,
#             code=referral_code
#         )
#         referral_code.used = True
#         referral_code.save()
#         return redirect("plans")
       
#     except ReferralCode.DoesNotExist:
#         messages.error(request, "Invalid referral code")
#         return redirect("signup")


# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
# from djstripe.models import Event
# from .models import Referral

# @require_http_methods(["POST"])
# def stripe_webhook(request):
#     event = None
#     payload = request.body
#     sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
   
#     try:
#         event = Event.construct_event(
#             payload, sig_header, endpoint_secret=STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         return JsonResponse({"error": str(e)}, status=400)
#     except SignatureVerificationError as e:
#         return JsonResponse({"error": str(e)}, status=400)

#     # Handle subscription events
#     if event.type == "invoice.paid":
#         handle_subscription_paid(event)

#     return JsonResponse({"received": True})

# def handle_subscription_paid(event):
#     invoice = event.data.object
#     customer = Customer.objects.get(id=invoice.customer)
#     user = customer.user
   
#     # Find referrals for this user
#     referrals = Referral.objects.filter(
#         referee=user,
#         reward_applied=False
#     )
   
#     for referral in referrals:
#         apply_referral_reward(referral)
#         referral.reward_applied = True
#         referral.save()

# def apply_referral_reward(referral):
#     # Apply reward based on plan
#     plan = referral.plan
#     if plan == "basic":
#         reward = 5
#     elif plan == "standard":
#         reward = 15
   
#     # Apply coupon to referrer
#     referrer = referral.referrer
#     referrer.stripe_customer.apply_coupon(f"REFERRAL{reward}")


# @login_required
# def subscribe(request, plan):
#     try:
#         customer = request.user.stripe_customer
#         subscription = customer.subscriptions.create(
#             items=[{"price": plan}],
#             trial_period_days=7 if plan == "basic-monthly" else 14
#         )
#         return redirect("dashboard")
       
#     except Exception as e:
#         messages.error(request, str(e))
#         return redirect("plans")