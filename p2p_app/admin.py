from django.contrib import admin
from .models import Supplier, PurchaseOrder, Requisition, Invoice, CustomUser, Product

admin.site.register(Supplier)
admin.site.register(PurchaseOrder)
admin.site.register(Requisition)
admin.site.register(Invoice)
admin.site.register(CustomUser)
admin.site.register(Product)
# admin.site.register(CustomPermissions)

