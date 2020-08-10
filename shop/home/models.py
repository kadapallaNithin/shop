from django.db import models
from django.urls import reverse
from django.utils import timezone
class Village(models.Model):
    village = models.CharField(max_length=64)
    mandal = models.CharField(max_length=64)
    district = models.CharField(max_length=64)

    def __str__(self):
        return self.village +" (v), "+ self.mandal +" (m), "+ self.district
class Customer(models.Model):
    name = models.CharField(max_length=64)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    id_in_book = models.IntegerField(default=0)
    address = models.ForeignKey(Village,models.CASCADE,related_name='user_address')#models.CharField(max_length=128)
    due = models.DecimalField(default=0,decimal_places=2,max_digits=10)
    
    def __str__(self):
        phone = ''
        if self.phone != -1:
            phone = self.phone
        return " "+self.name+", "+" "+self.address.village+" "+str(phone)
    def get_absolute_url(self):
        return reverse('customers')
class Category(models.Model):
    'name - of the category'
    name = models.CharField(max_length=32)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('new_invoice')

class Product(models.Model):
    'name - of the product, quantity - of the product in stock, category - like cement, fertilizer ect,  details -  like uses, usage, external links'
    name = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.SET_DEFAULT,default=1)# 1 for others
    contents = models.CharField(max_length=16)
    details = models.TextField(default='')

    def __str__(self):
        return self.name+" "+self.contents+"("+str(self.quantity)+")"#str(self.id)+" "++"("+str(self.quantity)+")"

class Rate(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name } @ {self.rate }'# 

class Bill(models.Model):
    '(customer,date, (total - amount), and due )- of the bill, '
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    due = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
    @property
    def time_isoformat(self):
        return self.date.time().isoformat()[:8]

    def __str__(self):
        return str(self.customer)+' - '+str(self.total)#str(self.date)#
    def get_absolute_url(self):
        return reverse('bill_particular',kwargs={'id':self.id})
    def save(self,*args,**kwargs):
        if not self.id :
            self.date = timezone.now()
        return super(Bill,self).save(*args,**kwargs)

class Payment(models.Model):
    #customer = models.ForeignKey(Customer,models.CASCADE,related_name='Payment') # redundant bill has this
    bill = models.ForeignKey(Bill,models.CASCADE)
    intrest_rate = models.DecimalField(max_digits=5,decimal_places=2,default=0)#default may be used in views.payment as 0
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    remarks = models.TextField(default='')
#    denom2000 = models.IntegerField(default=0)
 #   denom500 = models.IntegerField(default=0)
  #  denom200 = models.IntegerField(default=0)
   # denom100 = models.IntegerField(default=0)
    #denom50 = models.IntegerField()
    #denom20 = models.IntegerField()
    #denom10 = models.IntegerField()
    #denom5 = models.IntegerField()
    #denom2 = models.IntegerField()
    #denom1 = models.IntegerField()

    def __str__(self):
        # if self.bill:
        #     s = self.bill
        # else:
        #     s = self.customer
        return str(s.bill)+', '+str(self.amount) #str(self.denom2000*2000+self.denom500*500+self.denom200*200+self.denom100*100)

class Particular(models.Model):
    '''bill - in which the particular is in,
       rate_fk - the particular and its rate,
       rate - selling rate,
       quantity - of the particular,
       amount - for the particular'''
    bill = models.ForeignKey(Bill,on_delete=models.CASCADE)
    rate_fk = models.ForeignKey(Rate,on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f'{ self.rate_fk.rate }* ({ self.quantity })'
    def get_absolute_url(self):
        return reverse('bill_particular',kwargs={'id':self.bill.id})
class Invoice(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{ self.product.name } ({ self.quantity })'