from django.test import Client, TestCase
#from unittest import 
from .models import Product, Bill, Particular, Rate, Category, Customer, Invoice, Village, Payment

class ModelsTestCase(TestCase):
    
    def setUp(self):

        v0 = Village.objects.create(village="Kurthi",mandal="Pitlam",district="Kamareddy")
        v1 = Village.objects.create(village="Rampur",mandal="Pitlam",district="Kamareddy")

        c0 = Customer.objects.create(name="Kadapalla Mallappa",address=v0,phone=9010393565,email='kadapallamallappa@gmail.com')
        c1 = Customer.objects.create(name="Abdul Hafeez",address=v0)

        b0 = Bill.objects.create(customer=c0)

        p0 = Particular.objects.create(bill=b0)
    
    def test_bill(self):
        b0 = Bill.objects.get(id=1)

