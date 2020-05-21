from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Product, Bill, Particular

denomi = [2000,500,200,100,50,20,10,5,2,1]
def index(request):
    context = {
        #'post':request.post,
        'title': 'Payments',
        'denomi':denomi,
    }
#    d = []
    total = 0
    POST = request.POST
    for i in list(POST.keys())[1:]:
        #print(POST[i])
#        d.append(POST[i])
        total += int(POST[i]) * int(i)
    
    #context['POST'] = d 
    context['total'] = total # sum(list(POST.keys())[1:])
    return render(request,'home/home.html',context)#HttpResponse("Hi! Nithin")

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'

class BillListView(ListView):
    model = Bill
    context_object_name = 'bill'
    ordering = ['-date']
    paginate_by = 2

class BillParticularsListView(ListView):
    model = Particular
    template_name = 'home/particulars.html'
    context_object_name = 'particulars'

    def get_queryset(self):
        bill = get_object_or_404(Bill,id=self.kwargs.get('id'))
        return Particular.objects.filter(bill=bill).order_by('-amount')

def cart(request):
    context = {
        'title' : 'Cart',
        'products' : Product.objects.all(),
    }
    return render(request,'home/cart.html',context)