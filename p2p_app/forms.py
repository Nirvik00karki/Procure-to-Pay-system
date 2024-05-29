# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Supplier, PurchaseOrder, Requisition, Invoice, GoodsReceivedNotice
from django import forms

        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = '__all__'

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

class SupplierSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class GoodsReceivedNoticeForm(forms.ModelForm):
    class Meta:
        model = GoodsReceivedNotice
        fields = ['received_quantity', 'received_date', 'remarks']  
