from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView, CreateView
from .models import Product, Bill, Particular, Rate

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
class BillCreateView(CreateView):
    model = Bill
    fields = ['customer','total','due']
    
class BillParticularsListView(ListView):
    model = Particular
    template_name = 'home/particulars.html'
    context_object_name = 'particulars'
    def get_queryset(self):
        bill = get_object_or_404(Bill,id=self.kwargs.get('id'))
        return Particular.objects.filter(bill=bill).order_by('-amount')
    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = Product.objects.all()
        context['rates'] = Rate.objects.all()
        return context
class ParticularCreateView(CreateView):
    model = Particular
    fields = ['bill','rate_fk','quantity']


    def form_valid(self,form):
        form.instance.rate = 0 #form.instance.rate_fk.rate
        form.instance.amount = 0
        valid = super().form_valid(form) 
        if valid:
            form.save()
            messages.success(self.request,"created")
        else:
            messages.warning(self.request,"Failed to create particular")
        return valid
# def cart(request):
#     context = {
#         'title' : 'Cart',
#         'products' : Product.objects.all(),
#     }
#     return render(request,'home/cart.html',context)