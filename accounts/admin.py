from django.contrib import admin
from .models import *

# Change the admin panel header, and page title
admin.site.site_header = "CRM Admin Area"
admin.site.site_title = "CRM"
admin.site.index_title = "Admin Dashoard"


# Register Models
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
