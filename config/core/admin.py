from django import forms
from django.contrib import admin

from .models import Printer, Check


class PrinterAdminForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = '__all__'


class PrinterAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': (
                'name', 'api_key', 'check_type', 'point_id'
            )
        }),
    )
    form = PrinterAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'name', 'check_type', 'point_id')
    list_display_links = ('id', 'name')


class CheckAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('id', '__str__', 'printer_id', 'type', 'order', 'status', 'pdf_file')
    list_display_links = ('id', '__str__')
    list_filter = ('printer_id', 'type', 'status')


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
