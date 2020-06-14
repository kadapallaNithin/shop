from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Particular, Bill, Invoice, Payment
#from django.contrib import messages

# @receiver(pre_save,sender=Particular)
# def minus_previous(sender,instance,**kwargs):
#     b = Bill.objects.filter(id=instance.bill.id)[0]
#     b.total -= instance.amount
#     b.save()

@receiver(pre_save,sender=Payment)
def payment_effects(sender,instance,**kwargs):
    if instance.id:
        old = Payment.objects.get(pk=instance.id)
        instance.customer.due += old.amount
        if instance.bill :
            instance.bill.due += old.amount
    instance.bill.customer.due -= instance.amount
    if instance.bill:
        instance.bill.due -= instance.amount
        instance.bill.save()
    instance.bill.customer.save()

@receiver(pre_save,sender=Particular)
def particular_effects(sender,instance, **kwargs):
    if instance.id:
        old = Particular.objects.get(pk=instance.id)
        instance.bill.total -= old.amount
        instance.bill.due -= old.amount
        instance.bill.customer.due -= old.amount
        instance.rate_fk.product.quantity += old.quantity
    instance.bill.total += instance.amount
    instance.bill.due += instance.amount
    instance.bill.customer.due += instance.amount
    instance.rate_fk.product.quantity -= instance.quantity
    instance.bill.customer.save()
    instance.bill.save()
    instance.rate_fk.product.save()

@receiver(pre_save,sender=Invoice)
def invoice_effects(sender,instance,**kwargs):
    if instance.id:
        old = Invoice.objects.get(pk=instance.id)
        instance.product.quantity -= old.quantity
    instance.product.quantity += instance.quantity
    instance.product.save()

# @receiver(post_save,sender=Particular)
# def save_bill(sender,instance,**kwargs):
#     instance.bill.save()