from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User,WasteCollector,DistrictWasteCollector,StateWasteCollector,WasteCollectionPoint,WasteCollectionRecord,Wallet,WasteTypeDetail,SavedAddress
# from .waste_collector import WasteCollector


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone','email','first_name', 'user_type','status','delete']


@admin.register(WasteCollector)
class UserAdmin(admin.ModelAdmin):
    list_display = ['waste_collector_id','district_waste_collector_ref','user_ref','join_date']


@admin.register(DistrictWasteCollector)
class UserAdmin(admin.ModelAdmin):
    list_display = ['district_waste_collector_id','district_level','state_waste_collector_ref','user_ref','join_date']

@admin.register(StateWasteCollector)
class UserAdmin(admin.ModelAdmin):
    list_display = ['state_waste_collector_id','state_level','user_ref','join_date']

@admin.register(WasteCollectionPoint)
class UserAdmin(admin.ModelAdmin):
    list_display = ['collection_point_id','customer_ref','waste_collector_ref','date','status','created','updated']

@admin.register(WasteCollectionRecord)
class UserAdmin(admin.ModelAdmin):
    list_display = ['record_id','collection_point_ref','collection_date','total_price']

@admin.register(WasteTypeDetail)
class UserAdmin(admin.ModelAdmin):
    list_display = ['record_ref','waste_type','price','weight','total_cost','image']


@admin.register(Wallet)
class UserAdmin(admin.ModelAdmin):
    list_display = ['order_id','payment_id']


@admin.register(SavedAddress)
class UserAdmin(admin.ModelAdmin):
    list_display = ['saved_address_id']
