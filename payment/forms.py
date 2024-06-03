from django import forms

class PaymentForm(forms.Form):
    stripe_token = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput()
    )