from django.shortcuts import render, get_object_or_404,reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlencode
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views.generic import ListView, CreateView, UpdateView
from home.admin import BillResource,CustomerResource, InvoiceResource,ParticularResource, PaymentResource, ProductResource, RateResource, VillageResource
from .models import Product, Bill, Particular, Rate, Category, Customer, Invoice, Village, Payment
from .forms import VillageCreateForm, ProductForm
from decimal import Decimal
import os
import config
import datetime

class CategoryCreateView(PermissionRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    permission_required = ['add_category']
    def get_context_data(self):
        context  = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context
    
class MyListView(ListView):
    paginate_by = 100
    page = 1
    order_by = 'id'
    order = 'asc'
    where = '1'

    def get_context_data(self):
#        self.ordering = ['date']
        context = super().get_context_data()
        context['sort_links'] = self.sort_links
        context['page'] = self.page
        context['order'] = self.order
        context['order_by'] = self.order_by
        context['paginate_by'] = self.paginate_by
        return context
    # def get_ordering(self):
    #     if self.request.method == 'GET':
    #         if 'sort_by' in self.request.GET :
    #             ordering = [self.request.GET['sort_by']]#.get('sort_by','order_by')
    #             return ordering
    def get_queryset(self):
        if self.request.method == 'GET':
            GET = self.request.GET
            if 'page' in GET:
                self.page = GET['page']
            if 'order_by' in GET:
                self.order_by = GET['order_by']
            if 'order' in GET :
                self.order = GET['order']
        if self.table :
            return self.model.objects.raw("SELECT * FROM "+self.table+" WHERE "+self.where+" ORDER BY "+self.order_by+" "+self.order)#+" LIMIT "+str(int(self.page))+" , "+str(int(self.paginate_by)))
        return self.model.objects.raw("SELECT * FROM home_"+self.model._meta.object_name+" WHERE "+self.where+" ORDER BY "+self.order_by+" "+self.order)#+" LIMIT "+str(int(self.page))+" , "+str(int(self.paginate_by)))

class CustomerUpdateView(PermissionRequiredMixin, UpdateView):
    model = Customer
    fields = ['name','address','phone','email','id_in_book']
    permission_required = ['change_customer']

    def get_form(self,form_class=None):
        form = super(CustomerUpdateView,self).get_form(form_class)
        form.fields['phone'].required = False
        form.fields['email'].required = False
        return form

@permission_required('add_village',raise_exception=True)
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

@permission_required('view_payment')
def payment_list(request):
    return model_list(request,Payment,"Payment")

denomi = [2000,500,200,100,50,20,10]#,5,2,1

def error(request,message):
    return render(request,'home/error.html',{"message":message})

@permission_required(['view_bill','view_customer','view_category','view_invoice','view_product','view_particular','view_payment','view_rate'],raise_exception=True)
def export_list(request):
    return render(request,'home/export_list.html')

@permission_required(['view_bill','view_customer','view_category','view_invoice','view_product','view_particular','view_payment','view_rate'],raise_exception=True)
def export_all(request):
    resources = {"bills.xlsx": BillResource,"customers.xlsx":CustomerResource,"invoices.xlsx":InvoiceResource, "particulars.xlsx":ParticularResource,"payments.xlsx":PaymentResource,"products.xlsx":ProductResource,"rates.xlsx":RateResource, "villages.xlsx": VillageResource}
    export_dir = config.path_for.export_dir #"/home/nithin/Downloads/exports/"
    if os.path.exists(export_dir):
        for file_name,resource in resources.items():
            f = open(export_dir+file_name,'wb')
            f.write(resource().export().xlsx)
            f.close()
        messages.success(request,"See downloads at "+export_dir)
        return redirect('products')
    else:
        messages.error(request,'Path "'+export_dir+'" does not exist')
    return redirect('export_list')

@permission_required(['view_bill','view_customer','view_category','view_invoice','view_product','view_particular','view_payment','view_rate'],raise_exception=True)
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

@permission_required('add_payment',raise_exception=True)
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
                bill = get_object_or_404(Bill,id=bill_id)
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
            return HttpResponseRedirect(reverse('bills'))
    if bill_id != -1:
        context['bill'] = get_object_or_404(Bill,id=bill_id)
        context['period'] = datetime.datetime.now() - context['bill'].date
    return render(request,'home/home.html',context)#HttpResponse("Hi! Nithin")

class PaymentCreateView(PermissionRequiredMixin, CreateView):
    model = Payment
    fields = ['intrest_rate','amount','remarks']
    template_name = 'home/home.html'
    permission_required = 'add_payment'
    def get_form(self,form_class=None):
        form = super(PaymentCreateView,self).get_form(form_class)
        form.fields['remarks'].required = False
        return form

class PaymentsListView(PermissionRequiredMixin, MyListView):
    model = Payment
    permission_required = 'view_payment'
#    fields = ['customer','bill','amount','date','remarks']
    context_object_name = "payments"
#    ordering = ['-date']
    paginate_by = 10
    table = "home_payment AS p INNER JOIN home_bill as b ON p.bill_id = b.id INNER JOIN home_customer AS c ON b.customer_id = c.id "
    sort_links = ['id','c.name','b.due','amount','date','id']

class ProductUpdateView(UpdateView):
    form_class = ProductForm
    model = Product

class ProductListView(PermissionRequiredMixin, ListView):
    model = Product
    permission_required = ['view_product','view_rate']
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self):
        context = super().get_context_data()
        context['rates'] = Rate.objects.raw('SELECT r.id, p.name as name, p.contents as contents, r.rate, p.quantity, MAX(r.date)  FROM home_rate as r INNER JOIN home_product as p ON r.product_id = p.id GROUP BY p.id  ORDER BY p.category_id, p.name')#r.date DESC
        context['without_rate'] = Product.objects.raw('SELECT * FROM home_product WHERE id not in (SELECT product_id FROM home_rate)')
        return context

@permission_required('add_rate',raise_exception=True)
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



class CustomerBillsListView(LoginRequiredMixin, PermissionRequiredMixin, MyListView):
    model = Bill
    permission_required = 'view_bill'
    template_name = 'home/customer_bill_list.html'
    context_object_name = 'bills'
    order_by = 'date'
    order = 'desc'
    table = "home_bill AS b INNER JOIN home_customer AS c ON b.customer_id = c.id"
    sort_links = ['id','c.name','total','due','date']

    def get_queryset(self):
        customer = get_object_or_404(Customer,id=self.kwargs.get('id'))
#        return Bill.objects.filter(customer=customer).order_by('-due')
        self.where = " c.id = "+str(customer.id)
        return super().get_queryset()
    def get_context_data(self):
         context = super().get_context_data()
         context['customer'] = get_object_or_404(Customer,id=self.kwargs.get('id'))
         return context

class BillListView(PermissionRequiredMixin, MyListView):
    model = Bill
    permission_required = 'view_bill'
    context_object_name = 'bill'
    #ordering = ['-date']
    paginate_by = 10
    order_by = "date"
    order = 'desc'
    table = "home_bill AS b INNER JOIN home_customer as c ON b.customer_id = c.id "
    sort_links = ['id','c.name','total','due','date']

@permission_required('change_bill',raise_exception=True)
def bill_update_date(request,bill_id):
    if request.method == "POST":
        POST = request.POST
        try:
            bill = get_object_or_404(Bill,id=bill_id)
            d = POST['date'].split('-')
            bill_time = bill.date.time()
            new_time = bill_time
            if 'time' in POST:
                t = POST['time'].split(':')
                new_time = datetime.time(int(t[0]),int(t[1]),int(t[2]))
                #new_time = datetime.time.fromisoformat(POST['time'])
            bill.date = datetime.datetime(int(d[0]),int(d[1]),int(d[2]),new_time.hour,new_time.minute,new_time.second)
            bill.save()
            messages.success(request,f"Bill { bill }'s date is updated to { bill.date }")
        except KeyError:
            messages.warning(request,'Date or time is not posted!')
        except IndexError:
            messages.warning(request,'Date or time is not appropriate')
        except ValueError:
            messages.warning(request,'Date or time is not well formed')
    #messages.warning(request,f'There was a mistake!')
    return HttpResponseRedirect(reverse('bills'))#customer_,args=(bill.customer.id,)))

# class BillCreateView(CreateView):
#     model = Bill
#     fields = ['customer','total','due']

@permission_required('add_bill')
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

class BillParticularsListView(PermissionRequiredMixin, ListView):
    model = Particular
    permission_required = 'view_particular'
    template_name = 'home/particulars.html'
    context_object_name = 'particulars'
    paginate_by = 10

    def get_queryset(self):
        bill = get_object_or_404(Bill,id=self.kwargs.get('id'))
        return Particular.objects.filter(bill=bill).order_by('id')
    def get_context_data(self):
        context = super().get_context_data()
        context['bill'] = get_object_or_404(Bill,id=self.kwargs.get('id'))
        #context['customer'] = Customer.objects.get_object_or_404()
        context['products'] = Product.objects.all()
        context['rates'] = Rate.objects.all()
        return context

class ParticularCreateView(PermissionRequiredMixin, CreateView):
    model = Particular
    permission_required = "add_particular"
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

@permission_required('add_particular',raise_exception=True)
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

class InvoiceListView(PermissionRequiredMixin, MyListView):
    model = Invoice
    permission_required = 'view_invoice'
    context_object_name = 'invoices'
    table = "home_invoice AS i INNER JOIN (home_product AS p INNER JOIN home_category AS c ON p.category_id = c.id) ON i.product_id = p.id "
    sort_links = ["id","name","contents","quantity","rate","category_id","date"]

class CustomerListView(PermissionRequiredMixin, MyListView):
    model = Customer
    permission_required = 'view_customer'
    context_object_name = 'customers'
    #ordering = ['-due']
    order_by = "due"
    order = 'desc'
    paginate_by = 10
    table = "home_customer AS c INNER JOIN home_village AS v ON c.address_id = v.id "
    sort_links = ["id","name","v.village","due","id_in_book","phone","email"]
    def get_context_data(self):
        context = super().get_context_data()
        context['all_customers'] = Customer.objects.all()
        return context

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
class InvoiceCreate(PermissionRequiredMixin, DataListForm):
    model = Product
    permission_required = 'add_invoice'
    context_object_name = "Product"

@permission_required('add_invoice',raise_exception=True)
def invoice(request):
    if request.method == 'POST':
        try:
            prod_id = int(request.POST['prod_id'])
            if prod_id == -1:
                name = request.POST['name']
                category = Category.objects.get(id=request.POST['category'])
                product = Product.objects.create(name=name,category=category,contents=request.POST['contents'],quantity=0)
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
            "products":Product.objects.all(),
            "categories": Category.objects.all(),
        }
        return render(request,'home/invoice_form.html',context)

