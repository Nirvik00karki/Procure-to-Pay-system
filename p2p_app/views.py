from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseForbidden
from reportlab.lib.units import inch
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
# from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Supplier, PurchaseOrder, Requisition, Invoice, CustomUser, GoodsReceivedNotice
from .forms import SupplierForm, PurchaseOrderForm, RequisitionForm, InvoiceForm, SupplierSearchForm, GoodsReceivedNoticeForm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import user_passes_test

def dashboard_view(request):
    return render(request, 'dashboard.html')
def supplier_dashboard_view(request):
    return render(request, 'supplier_dashboard.html')

def navbar_context(request):
    if request.user.is_authenticated:
        user_role = request.user.role
    else:
        user_role = None
    return {'user_role': user_role}


#Authentication and Authorization
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'supplier':
                return redirect('supplier_dashboard')
            elif user.role == 'user':
                return redirect('dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login') 
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        CustomUser.objects.create_user(username=username, email=email, password=password, firstname=firstname,lastname=lastname)

        return redirect('login') 
    else:
       return render(request, 'registration.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@permission_required('p2p_app.permission_name')
def restricted_view(request):
    return render(request, 'restricted.html')

def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)

def home_view(request):
    return render(request, 'home.html')

# def admin_dashboard_view(request):
#     return render(request, 'admin_dashboard.html')

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

# @user_passes_test(is_admin)
def pending_requisitions(request):
    if not request.user.groups.filter(name='Admin').exists():
        raise PermissionDenied

    if request.method == 'POST':
        requisition_id = request.POST.get('requisition_id')
        requisition = get_object_or_404(Requisition, pk=requisition_id)
        requisition.status = 'Approved'
        requisition.save()
        return redirect('pending_requisitions')  # Redirect to the same view to see the updated list

    pending_requisitions = Requisition.objects.filter(status='Pending')
    return render(request, 'admin_dashboard.html', {'pending_requisitions': pending_requisitions})
#Supplier
# @login_required

def supplier_list(request):
    form = SupplierSearchForm(request.GET)
    suppliers = Supplier.objects.all()

    if 'query' in request.GET:
        query = request.GET['query']
        suppliers = suppliers.filter(name__icontains=query) | \
                    suppliers.filter(contact_person__icontains=query) | \
                    suppliers.filter(email__icontains=query) | \
                    suppliers.filter(address__icontains=query)

    context = {'suppliers': suppliers, 'form': form}
    return render(request, 'supplier/supplier.html', context)

# @login_required

def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'supplier/supplier_detail.html', {'supplier': supplier})

# @login_required

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier/add_supplier.html', {'form': form})

# @login_required

def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_detail', pk=pk)
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier/edit_supplier.html', {'form': form})

# @login_required
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'supplier/delete_supplier.html', {'supplier': supplier})

# Purchase Order
# @user_passes_test(lambda u: u.groups.filter(name__in=['Supplier', 'User']).exists())
def purchase_order_list(request):
   if request.user.is_authenticated:
        if request.user.is_supplier():
            purchase_orders = PurchaseOrder.objects.filter(status='Approved')
        else:
            purchase_orders = PurchaseOrder.objects.all()
        search_criteria = request.GET.get('search_criteria')
        search_keyword = request.GET.get('search_keyword')
        if search_criteria and search_keyword:
            if search_criteria == 'item_name':
                purchase_orders = purchase_orders.filter(item__icontains=search_keyword)
            elif search_criteria == 'supplier_name':
                purchase_orders = purchase_orders.filter(supplier__name__icontains=search_keyword)

        return render(request, 'purchase/purchase_order_list.html', {'purchase_orders': purchase_orders})
   else:
        return redirect('login')

def purchase_order_detail(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, 'purchase/purchase_order_detail.html', {'purchase_order': purchase_order})

# @login_required
def add_purchase_order(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm()
    return render(request, 'purchase/add_purchase_order.html', {'form': form})

def edit_purchase_order(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=purchase_order)
        if form.is_valid():
            form.save()
            return redirect('purchase_order_detail', pk=pk)
    else:
        form = PurchaseOrderForm(instance=purchase_order)
    return render(request, 'purchase/edit_purchase_order.html', {'form': form})

# @login_required
def delete_purchase_order(request, pk):
    if not request.user.groups.filter(name='Admin').exists():
        raise PermissionDenied
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        purchase_order.delete()
        return redirect('purchase_order_list')
    return render(request, 'purchase/delete_purchase_order.html', {'purchase_order': purchase_order})

#Requisition
# @login_required

def requisition_list(request):
    search_date = request.GET.get('search_date')
    if search_date:
        requisitions = Requisition.objects.filter(issued_date=search_date)
    else:
        requisitions = Requisition.objects.all()
    return render(request, 'requisition/requisition_list.html', {'requisitions': requisitions})


def requisition_detail(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    return render(request, 'requisition/requisition_detail.html', {'requisition': requisition})


def add_requisition(request):
    if request.method == 'POST':
        form = RequisitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('requisition_list')
    else:
        form = RequisitionForm()
    return render(request, 'requisition/add_requisition.html', {'form': form})


def edit_requisition(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    if request.method == 'POST':
        form = RequisitionForm(request.POST, instance=requisition)
        if form.is_valid():
            form.save()
            return redirect('requisition_detail', pk=pk)
    else:
        form = RequisitionForm(instance=requisition)
    return render(request, 'requisition/edit_requisition.html', {'form': form})



def delete_requisition(request, pk):
    requisition = get_object_or_404(Requisition, pk=pk)
    if request.method == 'POST':
        requisition.delete()
        return redirect('requisition_list')
    return render(request, 'requisition/delete_requisition.html', {'requisition': requisition})

# @user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
# def change_requisition_status(request, requisition_id, new_status):
#     requisition = get_object_or_404(Requisition, pk=requisition_id)
    
#     if request.user.is_authenticated and request.user.has_perm('your_app_name.change_requisition_status'):
#         requisition.status = new_status
#         requisition.save()
#         return redirect('requisition_detail', requisition_id=requisition_id)
#     else:
#         return HttpResponseForbidden("You are not authorized to change the status of requisitions.")

#Invoice
def invoice_list(request):
    invoices = Invoice.objects.all()
    search_criteria = request.GET.get('search_criteria')
    search_keyword = request.GET.get('search_keyword')
    if search_criteria and search_keyword:
        if search_criteria == 'item_name':
            invoices = invoices.filter(item__icontains=search_keyword)

    return render(request, 'invoice/invoice_list.html', {'invoices': invoices})

# @user_passes_test(lambda u: u.groups.filter(name='Supplier').exists())
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoice/invoice_detail.html', {'invoice': invoice})

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Supplier').exists())
def add_invoice(request):
    if not request.user.groups.filter(name='Supplier').exists():
        raise PermissionDenied
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = InvoiceForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('invoice_list')
        else:
            form = InvoiceForm()
        return render(request, 'invoice/add_invoice.html', {'form': form})
    else:
        return redirect('login')

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Supplier').exists())
def edit_invoice(request, pk):
    if not request.user.groups.filter(name='Supplier').exists():
        raise PermissionDenied
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoice_detail', pk=pk)
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'invoice/edit_invoice.html', {'form': form})

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='Supplier').exists())
def delete_invoice(request, pk):
    if not request.user.groups.filter(name='Supplier').exists():
        raise PermissionDenied
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'invoice/delete_invoice.html', {'invoice': invoice})

#Generate PDF
def generate_requisition_pdf(request, requisition_id):
    requisition = Requisition.objects.get(pk=requisition_id)  
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="requisition_{requisition.id}.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=letter)

    requisition_data = [
        ["Requisition ID", requisition.id],
        ["Department", requisition.department],
        ["Description", requisition.description],
        ["Urgency", requisition.urgency],
        ["Issued Date", requisition.issued_date.strftime('%Y-%m-%d')],
        ["Shipping Address", requisition.shipping_address],
        ["Payment Method", requisition.payment_method],
        ["Billing Address", requisition.billing_address],
    ]

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),  # Header font size
        ('FONTSIZE', (0, 1), (-1, -1), 12),  # Body font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black), 
    ])
    column_widths = [2 * inch, 4 * inch] 
    requisition_table = Table(requisition_data, colWidths=column_widths)
    requisition_table.setStyle(style)

    pdf.build([requisition_table])

    return response

def generate_invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)  
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=letter)

    invoice_data = [
        ["Invoice ID", invoice.id],
        ["Purchase Order", invoice.purchase_order],
        ["Amount", invoice.amount],
        ["Payment Method", invoice.payment_method],
        ["Invoice Due Date", invoice.payment_due_date.strftime('%Y-%m-%d')],
        ["Billing Address", invoice.billing_address],
        ["Invoice Date", invoice.invoice_date.strftime('%Y-%m-%d')],
    ]
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    column_widths = [2 * inch, 4 * inch] 
    invoice_table = Table(invoice_data, colWidths=column_widths)
    invoice_table.setStyle(style)

    pdf.build([invoice_table])

    return response

def generate_purchase_pdf(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)  
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="purchase_order_{purchase_order.id}.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=letter)

    purchase_data = [
        ["Purcchase Order ID", purchase_order.id],
        ["Supplier", purchase_order.supplier.name],
        ["Payment Term", purchase_order.payment_terms],
        ["Item of Purchase", purchase_order.item],
        ["Issued Date", purchase_order.created_at],
        ["Shipping Address", purchase_order.shipping_address],
        ["Payment Method", purchase_order.payment_method],
        ["Billing Address", purchase_order.billing_address],
    ]

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    column_widths = [2 * inch, 4 * inch] 
    purchase_table = Table(purchase_data, colWidths=column_widths)
    purchase_table.setStyle(style)

    pdf.build([purchase_table])
    return response

#Goods Received Notice
def create_grn(request, purchase_order_id):
    if not request.user.groups.filter(name='User').exists():
        raise PermissionDenied
    grns = GoodsReceivedNotice.objects.all()
    purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
    if request.method == 'POST':
        form = GoodsReceivedNoticeForm(request.POST)
        if form.is_valid():
            grn = form.save(commit=False)
            grn.purchase_order = purchase_order
            grn.save()
            return render(request, 'grn/grn_list.html', {'grns': grns})
    else:
        form = GoodsReceivedNoticeForm()
    return render(request, 'grn/create_grn.html', {'form': form, 'purchase_order': purchase_order})

def grn_list(request):
    grns = GoodsReceivedNotice.objects.all()
    return render(request, 'grn/grn_list.html', {'grns': grns})
def grn_detail(request, grn_id):
    grn = get_object_or_404(GoodsReceivedNotice, pk=grn_id)
    return render(request, 'grn/grn_detail.html', {'grn': grn})

def purchase_order_summary(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    query = PurchaseOrder.objects.all()
    
    if date_from and date_to:
        query = query.filter(created_at__range=[date_from, date_to])
    
    summary = query.aggregate(
        total_amount=Sum('amount'),
        total_count=Count('id'),
        average_amount=Avg('amount')
    )
    
    status_summary = query.values('status').annotate(count=Count('status')).order_by('status')
    monthly_data = query.annotate(month=TruncMonth('created_at')).values('month').annotate(total_amount=Sum('amount'), total_count=Count('id')).order_by('month')
    
    return render(request, 'reports/purchase_order_summary.html', {
        'summary': summary,
        'status_summary': status_summary,
        'monthly_data': monthly_data,
        'date_from': date_from,
        'date_to': date_to
    })

def invoice_summary(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    query = Invoice.objects.all()
    
    if date_from and date_to:
        query = query.filter(created_at__range=[date_from, date_to])
    
    summary = query.aggregate(
        total_amount=Sum('amount'),
        total_count=Count('id'),
        average_amount=Avg('amount')
    )
    
    status_summary = query.values('status').annotate(count=Count('status')).order_by('status')
    monthly_data = query.annotate(month=TruncMonth('created_at')).values('month').annotate(total_amount=Sum('amount'), total_count=Count('id')).order_by('month')
    
    return render(request, 'reports/invoice_summary.html', {
        'summary': summary,
        'status_summary': status_summary,
        'monthly_data': monthly_data,
        'date_from': date_from,
        'date_to': date_to
    })

def requisition_summary(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    query = Requisition.objects.all()
    
    if date_from and date_to:
        query = query.filter(created_at__range=[date_from, date_to])
    
    summary = query.aggregate(
        total_count=Count('id')
    )
    
    status_summary = query.values('status').annotate(count=Count('status')).order_by('status')
    monthly_data = query.annotate(month=TruncMonth('created_at')).values('month').annotate(total_count=Count('id')).order_by('month')
    
    return render(request, 'reports/requisition_summary.html', {
        'summary': summary,
        'status_summary': status_summary,
        'monthly_data': monthly_data,
        'date_from': date_from,
        'date_to': date_to
    })