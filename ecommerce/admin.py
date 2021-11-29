from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Shipping)
admin.site.register(ProductOrder)
admin.site.register(Payment)
admin.site.register(Notification)
