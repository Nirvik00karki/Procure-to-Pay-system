# Import necessary modules and models
from django.core.management.base import BaseCommand
from p2p_app.models import Requisition, PurchaseOrder, Supplier
from django.db import transaction
from django.utils import timezone


class Command(BaseCommand):
    help = 'Automatically creates purchase orders from approved requisitions'

    def handle(self, *args, **options):
        approved_requisitions = Requisition.objects.filter(status='Approved')
        supplier = Supplier.objects.first()

        try:
            with transaction.atomic():
                # Iterate over approved requisitions
                for requisition in approved_requisitions:
                    # Create purchase order for each requisition
                    PurchaseOrder.objects.create(
                        requisition=requisition,
                        # created_by=self.created_by,
                        total_amount=10000,
                        status='Pending',
                        supplier=supplier,
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        shipping_address = 'Kathmandu',
                        payment_terms = 'Should not be Damaged',
                        payment_due_date = '2024-05-13',
                        payment_method = 'Cash',
                        billing_address = 'kathmandu'
                    )                 
                    self.stdout.write(self.style.SUCCESS(f'Purchase order created for requisition {requisition.id}'))

                self.stdout.write(self.style.SUCCESS('All purchase orders created successfully'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
