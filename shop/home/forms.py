from django.forms import ModelForm, ChoiceField, Select
from .models import Village, Product
class VillageCreateForm(ModelForm):
    #ex = ChoiceField(choices=[1,234])
    class Meta:
        model = Village
        fields = ['village','mandal','district']
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','quantity','category','contents']
        labels = {
            'category' : "Category or Type"
        }
        widgets = {
            'category' : Select(attrs={'class':'browser_default'})
        }
