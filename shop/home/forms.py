from django.forms import ModelForm, ChoiceField
from .models import Village
class VillageCreateForm(ModelForm):
    #ex = ChoiceField(choices=[1,234])
    class Meta:
        model = Village
        fields = ['village','mandal','district']
