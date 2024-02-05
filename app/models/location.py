
from django.db import models
from .user import User

class SavedAddress(models.Model):
    customer_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_address_id = models.CharField(max_length=25,primary_key=True)
    address = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255)
    pincode = models.IntegerField()
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    lattitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)


    def __str__(self):
        return str(self.saved_address_id)