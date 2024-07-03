from django.contrib import admin
from .models import Company, Product, Invoice, Settings

# Register your models here.
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Settings)
