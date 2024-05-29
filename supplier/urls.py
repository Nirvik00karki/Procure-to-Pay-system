from django.urls import path
from . import views

urlpatterns = [
    path('supplier_dashboard/', views.supplier_dashboard_view, name='supplier_dashboard'),
    path('invoice_list_s/', views.invoice_list_s, name='invoice_list_s'),
    path('purchase_list_s/', views.purchase_order_list_s, name='purchase_list_s'),
    path('grn_list_s/', views.grn_list_s, name='grn_list_s'),

]