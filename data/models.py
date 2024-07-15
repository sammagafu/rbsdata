from django.db import models

class MerchantData(models.Model):
    merchant_name = models.CharField(max_length=100)
    merchant_location = models.CharField(max_length=100)
    new_code = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    before_photo = models.ImageField(upload_to='before_photos/')
    after_photo = models.ImageField(upload_to='after_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.merchant_name