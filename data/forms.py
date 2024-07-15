from django import forms
from .models import MerchantData

class MerchantDataForm(forms.ModelForm):
    class Meta:
        model = MerchantData
        fields = ['merchant_name', 'merchant_location', 'new_code', 'full_name', 'before_photo', 'after_photo']