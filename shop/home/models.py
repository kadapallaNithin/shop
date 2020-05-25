from django.db import models
from django.urls import reverse
# Create your models here.

class Village(models.Model):
    village = models.CharField(max_length=64)
    mandal = models.CharField(max_length=64)
    district = models.CharField(max_length=64)

    def __str__(self):
        return self.village +" (v), "+ self.mandal +" (m), "+ self.district
class Customer(models.Model):
    name = models.CharField(max_length=64)
    phone = models.IntegerField()
    address = models.ForeignKey(Village,models.CASCADE,related_name='user_address')#models.CharField(max_length=128)
    due = models.DecimalField(default=0,decimal_places=2,max_digits=10)
    
    def __str__(self):
        return " "+self.name+", "+" "+self.address.village#+str(self.phone)

class Payment(models.Model):
    customer = models.ForeignKey(Customer,models.CASCADE,related_name='Payment')
    denom2000 = models.IntegerField(default=0)
    denom500 = models.IntegerField(default=0)
    denom200 = models.IntegerField(default=0)
    denom100 = models.IntegerField(default=0)
    #denom50 = models.IntegerField()
    #denom20 = models.IntegerField()
    #denom10 = models.IntegerField()
    #denom5 = models.IntegerField()
    #denom2 = models.IntegerField()
    #denom1 = models.IntegerField()

    def __str__(self):
        return str(self.denom2000*2000+self.denom500*500+self.denom200*200+self.denom100*100)

class Product(models.Model):
    'name - of the product, quantity - of the product in stock'
    name = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name#str(self.id)+" "++"("+str(self.quantity)+")"

class Rate(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rate}'#{self.product} @ 

class Bill(models.Model):
    '(customer,date, (total - amount), and due )- of the bill, '
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    due = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return str(self.customer)+' - '+str(self.total)#str(self.date)#
    def get_absolute_url(self):
        return reverse('bill_particular',kwargs={'id':self.id})
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