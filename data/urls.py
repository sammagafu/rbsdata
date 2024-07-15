from django.urls import path
from .views import NewDataView,SuccessView

urlpatterns = [
    path('', NewDataView.as_view(), name='new_data'),
    path('success/', SuccessView.as_view(), name='success'),
]