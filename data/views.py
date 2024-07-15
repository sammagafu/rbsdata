from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import MerchantDataForm
from .models import MerchantData
from django.views.generic import TemplateView


class NewDataView(CreateView):
    model = MerchantData
    form_class = MerchantDataForm
    template_name = 'data/new_data.html'
    success_url = reverse_lazy('success')

class SuccessView(TemplateView):
    template_name = 'data/success.html'