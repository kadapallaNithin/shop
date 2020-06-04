from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Payment, Customer, Village, Product, Bill, Particular, Rate, Invoice
# Register your models here.
class VillageResource(resources.ModelResource):
    class Meta:
        model = Village
class VillageAdmin(ImportExportModelAdmin):
    resource_class = VillageResource

admin.site.register(Payment)
admin.site.register(Customer)
admin.site.register(Village, VillageAdmin)
admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(Particular)
admin.site.register(Rate)
admin.site.register(Invoice)