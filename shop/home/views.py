from django.shortcuts import render, get_object_or_404,reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlencode
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from home.admin import BillResource,CustomerResource, InvoiceResource,ParticularResource, PaymentResource, ProductResource, VillageResource
from .models import Product, Bill, Particular, Rate, Customer, Invoice, Village, Payment
from .forms import VillageCreateForm
from decimal import Decimal
import datetime

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['name','address','phone','email']

    def get_form(self,form_class=None):
        form = super(CustomerUpdateView,self).get_form(form_class)
        form.fields['phone'].required = False
        form.fields['email'].required = False
        return form
def village_create(request):
    if request.method == "POST":
        form = VillageCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Village { request.POST["village"] } has been created')
            return redirect('new_bill')
        else:
            messages.error(request,'Something wrong with the data')
    else:
        form = VillageCreateForm()
    return render(request,'home/village_form.html',{"form":form})

def model_list(request,model,model_name):
#    objects = Village.objects.all()
    obj_fields = []
    for obj in model.objects.all():
        #obj.fields = 
        obj_fields.append(dict((field.name, field.value_to_string(obj)) for field in obj._meta.fields))#{'Village','Mandal','District'}
    context = {
        "object_name": model_name,
        "object_fields": obj_fields,
    }
    if len(obj_fields) > 0:
        context["fields"] = [field for field in obj_fields[0].keys()]#['id','Village','Mandal','District'],
    return render(request,'home/model_list.html',context)

def village_list(request):
    return model_list(request,Village,"Village")

def payment_list(request):
    return model_list(request,Payment,"Payment")

denomi = [2000,500,200,100,50,20,10]#,5,2,1

def error(request,message):
    return render(request,'home/error.html',{"message":message})

def export_list(request):
    return render(request,'home/export_list.html')
def export_all(request):
    resources = {"bills.xlsx": BillResource,"customers.xlsx":CustomerResource,"invoices.xlsx":InvoiceResource, "particulars.xlsx":ParticularResource,"payments.xlsx":PaymentResource,"products.xlsx":ProductResource,"villages.xlsx": VillageResource}
    export_dir = "/home/nithin/Downloads/exports/"
    for file_name,resource in resources.items():
        f = open(export_dir+file_name,'wb')
        f.write(resource().export().xlsx)
        f.close()
    messages.success(request,"See downloads at "+export_dir)
    return redirect('products')
def export(request,model_name):
    try:
        if model_name == "bills.xlsx":
            dataset = BillResource().export()
        elif model_name == "customers.xlsx":
            dataset = CustomerResource().export()
        elif model_name == "invoices.xlsx":
            dataset = InvoiceResource().export()
        elif model_name == "particulars.xlsx":
            dataset = ParticularResource().export()
        elif model_name == "payments.xlsx":
            dataset = PaymentResource().export()
        elif model_name == "products.xlsx":
            dataset = ProductResource().export()
        elif model_name == "villages.xlsx":
            dataset = VillageResource().export()

        else:
            response = 'invalid url'
        response = dataset.xlsx
    except AttributeError:
        response = 'Internal Error - Attribute'
    except UnboundLocalError:
        pass
    return HttpResponse(response)

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
#         for i in list(POST.keys())[1:]:#POST.keys[0] is csrf_token
#         #print(POST[i])
# #        d.append(POST[i])
#             if i[0] == 'r':
#                 return_total += int(POST[i]) * int(i[1:])
#             elif i[0] == 't':
#                 taken_total += int(POST[i]) * int(i[1:])
    
    #context['POST'] = d 
        if bill_id == -1:
            context['total'] = taken_total - return_total # sum(list(POST.keys())[1:])
        else:
            try:
                bill = Bill.objects.get(pk=bill_id)
                # if 'intrest_rate' in request.POST:
                intrest_rate = Decimal(POST['intrest_rate'])
                # else:
                #     intrest_rate = 0
                amount = Decimal(POST['amount'])
                remarks = ''
                if 'remarks' in POST:
                    remarks = POST['remarks']
                #payment = Payment.objects.create(customer=bill.customer,bill=bill,amount=amount,intrest_rate=intrest_rate)
                payment = Payment.objects.create(bill=bill,amount=amount,intrest_rate=intrest_rate,remarks=remarks)
                messages.success(request,f"payment of Rs.{ payment.amount } successful ")
            except KeyError:
                messages.error(request,"Amount or intrest not defined!")
            except Customer.DoesNotExist:
                messages.error(request,f"customer with id { customer_id } does not exist!")
            except Bill.DoesNotExist:
                messages.error(request,f"bill with id { bill_id } does not exist!")
            return HttpResponseRedirect(reverse('bills'))
    if bill_id != -1:
        try:
            context['bill'] = Bill.objects.get(pk=bill_id)
            context['period'] = datetime.datetime.now() - context['bill'].date
        except Bill.DoesNotExist:
            messages.error(request,"Bill does not exist")
    return render(request,'home/home.html',context)#HttpResponse("Hi! Nithin")
class PaymentCreateView(CreateView):
    model = Payment
    fields = ['intrest_rate','amount','remarks']
    template_name = 'home/home.html'

    def get_form(self,form_class=None):
        form = super(PaymentCreateView,self).get_form(form_class)
        form.fields['remarks'].required = False
        return form

class PaymentsListView(ListView):
    model = Payment
    fields = ['customer','bill','amount','date','remarks']
    context_object_name = "payments"
    ordering = ['-date']
    paginate_by = 10

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self):
        context = super().get_context_data()
        context['rates'] = Rate.objects.raw('SELECT r.id, p.name as name, r.rate, p.quantity, MAX(r.date)  FROM home_rate as r INNER JOIN home_product as p ON r.product_id = p.id GROUP BY p.id  ORDER BY r.date DESC')
        context['without_rate'] = Product.objects.raw('SELECT * FROM home_product WHERE id not in (SELECT product_id FROM home_rate)')
        return context

def rate_create(request,prod_id):
    product = get_object_or_404(Product,id=prod_id) #Product.objects.get(pk=prod_id)
    if request.method == "POST":#
        rate = Decimal(request.POST['rate'])
        rate = Rate.objects.create(product=product,rate=rate)
        messages.success(request,f"Successfully created rate for { product.name } @ { rate.rate }")
        if 'redirect' in request.GET:
            return HttpResponseRedirect(request.GET['redirect'])
        return HttpResponseRedirect(reverse('products')) #render(request,'home/error.html',{"message":"success"+str(prod_id)})
    context = {"product":product}
    return render(request,'home/rate_form.html',context)


# def rate_create_notused(request,prod_id):
#     if request.method == "POST":#
#         try:
#             # if 'prod_id' in request.GET:
#             #     prod_id = int(request.GET['prod_id'])
#             # else:
#             #     prod_id = int(request.POST['prod_id'])
#                 # if prod_id == -1:
#                 #     Product.objects.create(name=request.POST['name'],)

            
#             product = get_object_or_404(Product,id=prod_id) #Product.objects.get(pk=prod_id)
#             rate = Decimal(request.POST['rate'])
#             rate = Rate.objects.create(product=product,rate=rate)
#             messages.success(request,f"Successfully created rate for { product.name } @ { rate.rate }")

#             if 'redirect' in request.GET:
#                 return HttpResponseRedirect(request.GET['redirect'])
#             return HttpResponseRedirect(reverse('products')) #render(request,'home/error.html',{"message":"success"+str(prod_id)})
            
#         # except KeyError:
#         #     message = "invalid data"
#         # except ValueError:
#         #     message = "Invalid data got name instead of id"
#         # except Product.DoesNotExist:
#         #     message = "Product does not exist"
#         # #if 'redirect' in request.POST:

#         return HttpResponseRedirect(reverse('error',kwargs={"message":message})) #render(request,'home/error.html',{"message":message})
#     else:
#         if 'prod_id' in request.GET:
#             try:
#                 context = {
#                     'product':Product.objects.get(pk=int(request.GET['prod_id']))
#                 }
#             except Product.DoesNotExist:
#                 return render(request,'home/error.html',{"message":"Product with id "+request.GET['prod_id']+" doesn't exist"})
#         else:
#             context = {
#                 'products': Product.objects.all(),
#             }
#         return render(request,'home/rate_form.html',context)

class CustomerBillsListView(ListView):
    model = Bill
    template_name = 'home/customer_bill_list.html'
    context_object_name = 'bills'
    paginate_by = 10

    def get_queryset(self):
        customer = get_object_or_404(Customer,id=self.kwargs.get('id'))
        return Bill.objects.filter(customer=customer).order_by('-due')
    def get_context_data(self):
         context = super().get_context_data()
         context['customer'] = get_object_or_404(Customer,id=self.kwargs.get('id'))
         return context
    
class BillListView(ListView):
    model = Bill
    context_object_name = 'bill'
    ordering = ['-date']
    paginate_by = 10

# class BillCreateView(CreateView):
#     model = Bill
#     fields = ['customer','total','due']

def bill_create(request):
    context = dict()
    if request.method == "POST":
        try:
            post = request.POST
            cust_id = int(post['cust_id'])
            context['cust_id'] = cust_id
            if cust_id == -1:
                name = post['name']
                context['name'] = name
                if 'phone' in post:
                    if post['phone'] == '':
                        phone = -1
                    else:
                        phone = int(post['phone'])
                        context['phone'] = phone
                else:
                    phone = -1
                if 'email' in post:
                    email = post['email']
                else:
                    email = ''
                context['email'] = email
                address_id = int(post['address_id'])
                context['address_id'] = address_id
                address = Village.objects.get(pk=address_id)
                customer = Customer.objects.create(name=name,phone=phone,email=email,address=address)
            else:
                customer = Customer.objects.get(pk=cust_id)
            bill = Bill.objects.create(customer=customer,total=0,due=0)
            return HttpResponseRedirect(reverse('bill_particular',args=(bill.id,)))
        except KeyError:
            messages.error(request,"Invalid data")
#            return render(request,'home/error.html',{"message":"Invalid data"})  
        except ValueError:
            messages.error(request,"Invalid data. Got name instead of id")
#            return render(request,'home/error.html',{"message":"Invalid data. Got name instead of id"})
        except Village.DoesNotExist :
            messages.error(request,"Please check address")
            #return render(request,'home/error.html',{"message":"Invalid data. Village is not selected properly. Try selecting again."})
        except Customer.DoesNotExist:
            messages.error(request,'contact nithin customer does not exist')
            #return render(request,'home/error.html',{'message':'contact nithin customer does not exist'})
    #else:
    context["customers"] = Customer.objects.all()
    context["addresses"] = Village.objects.all()
#    messages.success(request,context['cust_id'])
#    context['cust_id'] = 'nithin'
    return render(request,'home/bill_form.html',context)

class BillParticularsListView(ListView):
    model = Particular
    template_name = 'home/particulars.html'
    context_object_name = 'particulars'
    paginate_by = 10

    def get_queryset(self):
        bill = get_object_or_404(Bill,id=self.kwargs.get('id'))
        return Particular.objects.filter(bill=bill).order_by('-amount')
    def get_context_data(self):
        context = super().get_context_data()
        context['bill'] = get_object_or_404(Bill,id=self.kwargs.get('id'))
        #context['customer'] = Customer.objects.get_object_or_404()
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

class DataListForm:
    'Create Form with a datalist for the model'
    model = None
    model_name = None
    def view(self,request):
        return render(request,'home/datalist_form.html',self.get_context_data())
    def as_view(self):
        return self.view
    def get_context_data(self):
        #try:
        objects = self.model.objects.all()
        return {"objects":objects,"model_name":model_name}
class InvoiceCreate(DataListForm):
    model = Product
    context_object_name = "Product"
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
            return HttpResponseRedirect(reverse('new_rate',args=(product.id,)))#"?"+urlencode({"prod_id":product.pk,"redirect":reverse('products')}))
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