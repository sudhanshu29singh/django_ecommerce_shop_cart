from django.contrib import admin

# Register your models here.
from app1.models import Contact,Product,Orders

admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Orders)
