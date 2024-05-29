from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import Permission
from decimal import Decimal
from django.utils import timezone


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('supplier', 'Supplier'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        related_query_name='user',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        related_query_name='user',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    def is_supplier(self):
        return self.groups.filter(name='Supplier').exists()

# class CustomPermissions(models.Model):
#     class Meta:
#         permissions = (
#             ("change_requisition_status", "Can change the status of requisitions"),
#         )
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
# @receiver(post_save, sender=Supplier)
# def log_supplier_creation_update(sender, instance, created, **kwargs):
#     action = 'created' if created else 'updated'
#     logging.info(f'Supplier {instance.name} {action} by {instance.created_by.username} at {timezone.now()}')

# @receiver(pre_delete, sender=Supplier)
# def log_supplier_deletion(sender, instance, **kwargs):
#     logging.info(f'Supplier {instance.name} deleted by {instance.created_by.username} at {timezone.now()}')
class Requisition(models.Model):
    # created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    preferred_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=1)
    department = models.CharField(max_length=100, null=True)
    urgency = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], null=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)
    issued_date = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address = models.CharField(max_length=255, default='')
    payment_method = models.CharField(max_length=50, default='e.g.Cash')
    billing_address = models.TextField(default='')


    def __str__(self):
        return f"Requisition#{self.id}"
    
class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    requisition = models.OneToOneField(Requisition, on_delete=models.CASCADE, related_name='purchase_order', blank=True, null=True)
    # created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.CharField(max_length=20, default='e.g.Laptop')
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=1)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address = models.TextField(default='')
    payment_terms = models.CharField(max_length=50, null=True)
    payment_due_date = models.DateField()
    payment_method = models.CharField(max_length=50, default='e.g.Cash')
    billing_address = models.TextField(default='')

    def __str__(self):
        return f"PO#{self.id} - {self.supplier.name}"

class Invoice(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    item = models.CharField(max_length=20, default='e.g.Laptop')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])
    invoice_date = models.DateField()
    payment_due_date = models.DateField()
    payment_method = models.CharField(max_length=50, default='e.g.Cash')
    billing_address = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice#{self.id} - {self.purchase_order}"
    

class GoodsReceivedNotice(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    received_date = models.DateTimeField(default=timezone.now)
    received_quantity = models.PositiveIntegerField()
    remarks = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"GRN #{self.id} for Purchase Order #{self.purchase_order.id}"

