from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .models import Payment
from p2p_app.models import Invoice
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# @login_required
# def payment_view(request):
#     invoice = get
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             stripe_token = form.cleaned_data['stripe_token']
#             try:
#                 charge = stripe.Charge.create(
#                     amount=5000,  
#                     currency='usd',
#                     description='Example charge',
#                     source=stripe_token,
#                 )
#                 Payment.objects.create(
#                     user=request.user,
#                     stripe_charge_id=charge.id,
#                     amount=charge.amount / 100,
#                     currency=charge.currency,
#                     description=charge.description,
#                     status=charge.status,
#                 )

#                 return redirect('payment_success')
#             except stripe.error.StripeError as e:
#                 return render(request, 'payment_error.html', {'error': str(e)})
#     else:
#         form = PaymentForm()

#     context = {
#         'form': form,
#         'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
#     }
#     return render(request, 'payment.html', context)

@login_required
def payment_success_view(request):
    return render(request, 'payment_success.html')

