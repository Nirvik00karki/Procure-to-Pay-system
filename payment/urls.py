from django.urls import path
from . import views


urlpatterns = [
    # path('payment/', views.payment_view, name='payment'),
    path('payment_success/', views.payment_success_view, name='payment_success'),
]
