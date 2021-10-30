from django import forms
from django.contrib import admin

from .models import Printer, Check


class PrinterAdminForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = '__all__'


class PrinterAdmin(admin.ModelAdmin):
    form = PrinterAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'name', 'api_key', 'check_type', 'point_id')


# class CheckAdminForm(forms.ModelForm):
#     class Meta:
#         model = Printer
#         fields = '__all__'


class CheckAdmin(admin.ModelAdmin):
    list_filter = ('printer_id', 'type')


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
