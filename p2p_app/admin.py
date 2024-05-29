from django.contrib import admin
from .models import Supplier, PurchaseOrder, Requisition, Invoice, CustomUser

admin.site.register(Supplier)
admin.site.register(PurchaseOrder)
admin.site.register(Requisition)
admin.site.register(Invoice)
admin.site.register(CustomUser)
# admin.site.register(CustomPermissions)

