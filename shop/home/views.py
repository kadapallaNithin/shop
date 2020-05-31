from django.shortcuts import render, get_object_or_404,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlencode
from django.contrib import messages
from django.views.generic import ListView, CreateView
from .models import Product, Bill, Particular, Rate, Customer, Invoice, Village, Payment
from decimal import Decimal
denomi = [2000,500,200,100,50,20,10,5,2,1]

def error(request,message):
    return render(request,'home/error.html',{"message":message})

def payment(request,bill_id):
    context = {
        #'post':request.post,
        'title': 'Payments',
        'denomi':denomi,
    }
#    d = []
    taken_total = 0
    return_total = 0
    if request.method == "POST":
        POST = request.POST
        for i in list(POST.keys())[1:]:#POST.keys[0] is csrf_token
        #print(POST[i])
#        d.append(POST[i])
            if i[0] == 'r':
                return_total += int(POST[i]) * int(i[1:])
            elif i[0] == 't':
                taken_total += int(POST[i]) * int(i[1:])
    
    #context['POST'] = d 
        if bill_id == -1:
            context['total'] = taken_total - return_total # sum(list(POST.keys())[1:])
        else:
            try:
                bill = Bill.objects.get(pk=bill_id)
                amount = Decimal(request.POST['amount'])
                payment = Payment.objects.create(customer=bill.customer,bill=bill,amount=amount)
                messages.success(request,f"payment of Rs.{ payment.amount } successful ")
            except KeyError:
                messages.error(request,"Amount not defined!")
            except Customer.DoesNotExist:
                messages.error(request,f"customer with id { customer_id } does not exist!")
            except Bill.DoesNotExist:
                messages.error(request,f"bill with id { bill_id } does not exist!")
            return HttpResponseRedirect(reverse('bills'))
    if bill_id != -1:
        try:
            context['bill'] = Bill.objects.get(pk=bill_id)
        except Bill.DoesNotExist:
            messages.error(request,"Bill does not exists")
    return render(request,'home/home.html',context)#HttpResponse("Hi! Nithin")

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['rates'] = Rate.objects.raw('SELECT r.id, p.name as name, r.rate, p.quantity, r.date  FROM home_rate as r INNER JOIN home_product as p ON r.product_id = p.id  order by r.date desc')
        return context
    
def rate_create(request):
    if request.method == "POST":#
        try:
            if 'prod_id' in request.GET:
                prod_id = int(request.GET['prod_id'])
            else:
                prod_id = int(request.POST['prod_id'])
                # if prod_id == -1:
                #     Product.objects.create(name=request.POST['name'],)

            
            product = Product.objects.get(pk=prod_id)
            rate = Decimal(request.POST['rate'])
            rate = Rate.objects.create(product=product,rate=rate)
            messages.success(request,f"Successfully created rate for { product.name } @ { rate.rate }")

            if 'redirect' in request.GET:
                return HttpResponseRedirect(request.GET['redirect'])
            return HttpResponseRedirect(reverse('products')) #render(request,'home/error.html',{"message":"success"+str(prod_id)})
            
        except KeyError:
            message = "invalid data"
        except ValueError:
            message = "Invalid data got name instead of id"
        except Product.DoesNotExist:
            message = "Product does not exist"
        #if 'redirect' in request.POST:

        return HttpResponseRedirect(reverse('error',kwargs={"message":message})) #render(request,'home/error.html',{"message":message})
    else:
        if 'prod_id' in request.GET:
            try:
                context = {
                    'product':Product.objects.get(pk=int(request.GET['prod_id']))
                }
            except Product.DoesNotExist:
                return render(request,'home/error.html',{"message":"Product with id "+request.GET['prod_id']+" doesn't exist"})
        else:
            context = {
                'products': Product.objects.all(),
            }
        return render(request,'home/rate_form.html',context)

class BillListView(ListView):
    model = Bill
    context_object_name = 'bill'
    ordering = ['-date']
    paginate_by = 10

# class BillCreateView(CreateView):
#     model = Bill
#     fields = ['customer','total','due']

def bill_create(request):
    if request.method == "POST":
        try:
            post = request.POST
            cust_id = int(post['cust_id'])
            if cust_id == -1:
                name = post['name']
                if 'phone' in post:
                    phone = int(post['phone'])
                else:
                    phone = -1
                if 'email' in post:
                    email = post['email']
                else:
                    email = ''
                address_id = int(post['address_id'])
                customer = Customer.objects.create(name=name,phone=phone,email=email,address_id=address_id)
            else:
                customer = Customer.objects.get(pk=cust_id)
            bill = Bill.objects.create(customer=customer,total=0,due=0)
            return HttpResponseRedirect(reverse('bill_particular',args=(bill.id,)))
        except KeyError:
            return render(request,'home/error.html',{"message":"Invalid data"})  
        except ValueError:
            return render(request,'home/error.html',{"message":"Invalid data got name instead of id"})
        except IntegrityError :
            messages.error(request,"Please check address")
            return render(request,'home/error.html',{"message":"Invalid data got name instead of id"})
 
        except Customer.DoesNotExist:
            return render(request,'home/error.html',{'message':'contact nithin customer does not exist'})
    else:
        context = {
            "customers": Customer.objects.all(),
            "addresses": Village.objects.all(),
        }
        return render(request,'home/bill_form.html',context)

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
    fields = ['bill','rate_fk','rate','quantity']
    
    def form_valid(self,form):
        form.instance.rate = 0 #form.instance.rate_fk.rate
        form.instance.amount = 0
        #form.save()
        form_is_valid = super().form_valid(form) 
        if form_is_valid:
        #     form.save()
            messages.success(self.request,"created")
        else:
            messages.warning(self.request,"Failed to create particular")
        return form_is_valid
def add_particular(request,bill_id):
    try:
        #particular_id = int(request.POST['particular'])
        rate = Decimal(request.POST['rate'])
        rate_fk_id = int(request.POST['rate_fk'])
        quantity = int(request.POST['quantity'])
        amount = Decimal(request.POST['amount'])
        if amount == quantity*rate:
#        particular = Particular.objects.get(pk=particular_id)
            bill = Bill.objects.get(pk=bill_id)
            rate_fk = Rate.objects.get(pk=rate_fk_id)
            Particular.objects.create(bill=bill,rate_fk=rate_fk,rate=rate,quantity=quantity,amount=amount)
        else:
            return render(request,'home/error.html',{'message':'amount calculation error. Please re-enter'})
    except KeyError:
        return render(request,'home/error.html',{'message':'invalid data provided'})
    except Bill.DoesNotExist:
        return render(request,'home/error.html',{'message':"bill does not exist"})
    except Rate.DoesNotExist:
        return render(request,'home/error.html',{'message':"Rate does not exist"})
    return HttpResponseRedirect(reverse('bill_particular',args=(bill_id,)))
# def cart(request):
#     context = {
#         'title' : 'Cart',
#         'products' : Product.objects.all(),
#     }
#     return render(request,'home/cart.html',context)
class InvoiceListView(ListView):
    model = Invoice
    context_object_name = 'invoices'
    ordering = ['-date']
    paginate_by = 10

class CustomerListView(ListView):
    model = Customer
    context_object_name = 'customers'
    ordering = ['-due']
    paginate_by = 10

def invoice(request):
    if request.method == 'POST':
        try:
            prod_id = int(request.POST['prod_id'])
            if prod_id == -1:
                name = request.POST['name']
                product = Product.objects.create(name=name,quantity=0)
            else:
                product = Product.objects.get(pk=prod_id)
            rate = Decimal(request.POST['rate'])
            quantity = int(request.POST['quantity'])
            Invoice.objects.create(product=product,rate=rate,quantity=quantity)
            return HttpResponseRedirect(reverse('new_rate')+"?"+urlencode({"prod_id":product.pk,"redirect":reverse('products')}))
        except Product.DoesNotExist:
            return render(request,'home/error.html',{"message":'Call nithin and say "error at invoice product does not exist"'})
        except ValueError:
            return render(request,'home/error.html',{"message":"invalid data"})
        except KeyError:
            return render(request,'home/error.html',{"message":"Invalid data"})
    else:
        context = {
            "products":Product.objects.all()
        }
        return render(request,'home/invoice_form.html',context)