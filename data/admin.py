import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import MerchantData
from django.utils.html import format_html
from django.utils import timezone
import xlwt
import datetime

@admin.register(MerchantData)
class MerchantDataAdmin(admin.ModelAdmin):
    list_display = [
        'merchant_name', 
        'merchant_location', 
        'new_code', 
        'full_name', 
        'before_photo_link', 
        'after_photo_link'
    ]
    actions = ["export_as_csv", "export_as_excel"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.request = request  # Store the request object
        return qs

    def before_photo_link(self, obj):
        if obj.before_photo:
            return format_html('<a href="{}" target="_blank">View Before Photo</a>', self.request.build_absolute_uri(obj.before_photo.url))
        return "No Image"
    before_photo_link.short_description = 'Before Photo'

    def after_photo_link(self, obj):
        if obj.after_photo:
            return format_html('<a href="{}" target="_blank">View After Photo</a>', self.request.build_absolute_uri(obj.after_photo.url))
        return "No Image"
    after_photo_link.short_description = 'After Photo'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name not in ['before_photo', 'after_photo']]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names + ['before_photo_url', 'after_photo_url'])
        for obj in queryset:
            row = []
            for field in field_names:
                value = getattr(obj, field)
                if isinstance(value, datetime.datetime):
                    if timezone.is_naive(value):
                        value = timezone.make_aware(value, timezone.get_current_timezone())
                    value = timezone.localtime(value, timezone.get_current_timezone())
                row.append(value)
            row.append(self.request.build_absolute_uri(obj.before_photo.url) if obj.before_photo else 'No Image')
            row.append(self.request.build_absolute_uri(obj.after_photo.url) if obj.after_photo else 'No Image')
            writer.writerow(row)

        return response
    export_as_csv.short_description = "Export Selected as CSV"

    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=exported_data.xls'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [field.name for field in self.model._meta.fields if field.name not in ['before_photo', 'after_photo']] + ['before_photo_url', 'after_photo_url']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        for obj in queryset:
            row_num += 1
            for col_num, field in enumerate(columns[:-2]):  # Exclude the last two custom columns for photos
                value = getattr(obj, field)
                if isinstance(value, datetime.datetime):
                    if timezone.is_naive(value):
                        value = timezone.make_aware(value, timezone.get_current_timezone())
                    value = timezone.localtime(value, timezone.get_current_timezone())
                ws.write(row_num, col_num, str(value), font_style)
            ws.write(row_num, len(columns) - 2, self.request.build_absolute_uri(obj.before_photo.url) if obj.before_photo else 'No Image', font_style)
            ws.write(row_num, len(columns) - 1, self.request.build_absolute_uri(obj.after_photo.url) if obj.after_photo else 'No Image', font_style)

        wb.save(response)
        return response
    export_as_excel.short_description = "Export Selected as Excel"