from django.db import models
from .user import User
from .waste_collector import WasteCollector
from .location import SavedAddress
WORK_PROCESS = (
    ("complete", "complete"),
    ("accepted","accepted"),
    ("pending", "pending"),
    ("cancel", "cancel"),
)

USER_TYPE = (
    ("user", "user"),
    ("wc","wc"),
)


class WasteCollectionPoint(models.Model):
    customer_ref = models.ForeignKey(User, on_delete=models.CASCADE,related_name='waste_points')
    collection_point_id = models.CharField(max_length=25,primary_key=True)
    date = models.DateField(blank=True,null=True)
    slot_time = models.TimeField(blank=True,null=True)    
    status = models.CharField(max_length = 20,choices = WORK_PROCESS,default = 'pending')
    waste_collector_ref = models.ForeignKey(WasteCollector, on_delete=models.CASCADE,blank=True,null=True)
    optional_phone=models.CharField(max_length=225,blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    pincode = models.IntegerField()
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    lattitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_waste_points')
    

    def __str__(self):
        return str(self.collection_point_id)
    

    
class OrderCancel(models.Model):
    waste_collection_point_ref = models.ForeignKey(WasteCollectionPoint, on_delete=models.CASCADE)
    canceled_by = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length = 20,choices = USER_TYPE,default = 'user')
    reason = models.CharField(max_length = 20,default="none")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



