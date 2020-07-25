from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Bill, Category, Customer, Invoice, Particular, Payment, Product, Rate, Village
# Register your models here.
class BillResource(resources.ModelResource):
    class Meta:
        model = Bill
class BillAdmin(ImportExportModelAdmin):
    resource_class = BillResource
admin.site.register(Bill, BillAdmin)

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
admin.site.register(Category, CategoryAdmin)

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
admin.site.register(Customer, CustomerAdmin)

class InvoiceResource(resources.ModelResource):
    class Meta:
        model = Invoice
class InvoiceAdmin(ImportExportModelAdmin):
    resource_class = InvoiceResource
admin.site.register(Invoice, InvoiceAdmin)

class ParticularResource(resources.ModelResource):
    class Meta:
        model = Particular
class ParticularAdmin(ImportExportModelAdmin):
    resource_class = ParticularResource
admin.site.register(Particular, ParticularAdmin)

class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment
class PaymentAdmin(ImportExportModelAdmin):
    resource_class = PaymentResource
admin.site.register(Payment,PaymentAdmin)

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
admin.site.register(Product, ProductAdmin)

class RateResource(resources.ModelResource):
    class Meta:
        model = Rate
class RateAdmin(ImportExportModelAdmin):
    resource_class = RateResource
admin.site.register(Rate, RateAdmin)

class VillageResource(resources.ModelResource):
    class Meta:
        model = Village
class VillageAdmin(ImportExportModelAdmin):
    resource_class = VillageResource
admin.site.register(Village, VillageAdmin)