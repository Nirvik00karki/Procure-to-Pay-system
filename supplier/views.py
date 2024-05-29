from django.shortcuts import render, redirect
from p2p_app.models import Invoice, PurchaseOrder, GoodsReceivedNotice

def supplier_dashboard_view(request):
    return render(request, 'supplier_dashboard.html')

def purchase_order_list_s(request):
   if request.user.is_authenticated:
        purchase_orders = PurchaseOrder.objects.filter(status='Approved')
        search_criteria = request.GET.get('search_criteria')
        search_keyword = request.GET.get('search_keyword')
        if search_criteria and search_keyword:
            if search_criteria == 'item_name':
                purchase_orders = purchase_orders.filter(item__icontains=search_keyword)
            elif search_criteria == 'supplier_name':
                purchase_orders = purchase_orders.filter(supplier__name__icontains=search_keyword)
        return render(request, 'purchase_list_s.html', {'purchase_orders': purchase_orders})
   else:
        return redirect('login')
   
def invoice_list_s(request):
    invoices = Invoice.objects.all()
    search_criteria = request.GET.get('search_criteria')
    search_keyword = request.GET.get('search_keyword')
    if search_criteria and search_keyword:
        if search_criteria == 'item_name':
            invoices = invoices.filter(item__icontains=search_keyword)

    return render(request, 'invoice_list_s.html', {'invoices': invoices})

def grn_list_s(request):
    grns = GoodsReceivedNotice.objects.all()
    return render(request, 'grn_list_s.html', {'grns': grns})
# def grn_detail_s(request, grn_id):
#     grn = get_object_or_404(GoodsReceivedNotice, pk=grn_id)
#     return render(request, 'grn_detail_s.html', {'grn': grn})

# def invoice_detail_s(request, pk):
#     invoice = get_object_or_404(Invoice, pk=pk)
#     return render(request, 'invoice_detail_s.html', {'invoice': invoice})

# def purchase_detail_s(request, pk):
#     purchase_order_s = get_object_or_404(PurchaseOrder, pk=pk)
#     return render(request, 'purchase_detail_s.html', {'purchase_order_s': purchase_order_s})
