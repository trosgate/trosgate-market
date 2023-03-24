from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .stripe import StripeCheckout
import stripe


@require_POST
def stripe_checkout(request):
    # Get the form data from the request
    amount = int(request.POST.get("amount", 0))
    currency = "usd"
    description = request.POST.get("description", "")
    customer_email = request.POST.get("customer_email", "")
    success_url = request.POST.get("success_url", "")
    cancel_url = request.POST.get("cancel_url", "")
    
    # Create a new instance of the StripeCheckout class
    stripe_checkout = StripeCheckout()
    
    # Call the create_checkout method
    session_id = stripe_checkout.create_checkout(
        amount=amount, 
        currency=currency, 
        description=description, 
        customer_email=customer_email, 
        success_url=success_url,
        cancel_url=cancel_url
    )
    
    # Return a JSON response with the session ID
    return HttpResponse(json.dumps({"session_id": session_id}), content_type="application/json")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    # Retrieve the webhook data from the request
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the webhook event
    stripe_checkout = StripeCheckout()
    stripe_checkout.handle_webhook(event)

    # Return a success response
    return HttpResponse(status=200)
