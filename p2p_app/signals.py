from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Requisition, PurchaseOrder, Supplier

@receiver(post_save, sender=Requisition)
def create_purchase_order(instance, created, **kwargs):
    supplier = Supplier.objects.first()
    if not created and instance.status == 'Approved':
        supplier = instance.preferred_supplier
        PurchaseOrder.objects.create(
            requisition=instance,
            supplier=supplier,
            product=instance.product,
            status='Pending',
            quantity=instance.quantity,
            unit_price=instance.unit_price,
            subtotal=instance.subtotal,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            shipping_address=instance.shipping_address,
            # payment_terms=instance.payment_terms,
            payment_due_date='2024-06-01',
            payment_method=instance.payment_method,
            billing_address=instance.billing_address
        )
