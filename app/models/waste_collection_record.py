from django.db import models
from .waste_collector import WasteCollector
from .waste_collection_point import WasteCollectionPoint

WASTE_TYPE = (
    ("plastic", "plastic"),
    ("iron", "iron"),
    ("glass", "glass"),
    ("paper","paper"),
)

WORK_PROCESS = (
    ("complete", "complete"),
    ("pending", "pending"),
    ("cancel", "cancel"),
)

import random

def unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            n=WasteCollectionRecord.objects.get(record_id=uq)
        except:
            return uq

class WasteCollectionRecord(models.Model):
    collection_point_ref = models.OneToOneField(WasteCollectionPoint, on_delete=models.CASCADE)
    # order_id=models.CharField(max_length=25,unique=True,default="NONE")
    record_id=models.CharField(max_length=25,primary_key=True)
    collection_date = models.DateTimeField(auto_now_add=True)
    total_price=models.FloatField(default=0)
    # status = models.CharField(max_length = 20,choices = WORK_PROCESS,default = 'completed')
    # payment_status = models.CharField(max_length = 20,default = 'failed')

    def save(self, *args, **kwargs):
        # Generate a unique record_id using UUID
        if not self.record_id:
            self.record_id = unique_number("record") # Take the first 8 characters of the UUID
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.record_id)
    


class WasteTypeDetail(models.Model):
    record_ref = models.ForeignKey(WasteCollectionRecord, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length = 20,default = 'plastic')
    price=models.FloatField(default=0)
    weight=models.FloatField(default=0)
    total_cost=models.FloatField(default=0)
    image= models.CharField(max_length=400,default='')