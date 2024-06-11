# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Supplier, PurchaseOrder, Requisition, Invoice, GoodsReceivedNotice, Product
from django import forms

        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'requisition': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'customer_tax': forms.NumberInput(attrs={'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = '__all__'
        widgets = {
            'preferred_supplier': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'customer_tax': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # 'order_deadline': forms.DateTimeInput(attrs={'class': 'form-control'}),
            # 'expected_arrival': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'purchase_order': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'customer_tax': forms.NumberInput(attrs={'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control'}),
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'payment_due_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SupplierSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class GoodsReceivedNoticeForm(forms.ModelForm):
    class Meta:
        model = GoodsReceivedNotice
        fields = ['received_quantity', 'received_date', 'remarks']  
