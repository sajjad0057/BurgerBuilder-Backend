from django.contrib import admin
from .models import UserProfile,Ingredient,Order,CustomerDetail

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(CustomerDetail)
admin.site.register(Order)                   
admin.site.register(Ingredient)

