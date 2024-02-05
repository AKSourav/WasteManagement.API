from django.db import models
from .state_waste_collector import StateWasteCollector
from .user import User
GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Others", "Others"),
)

BLOOD_GROUP = (
    ("1", "A+"),
    ("2", "A-"),
    ("3", "B+"),
    ("4", "B-"),
    ("5", "O+"),
    ("6", "O-"),
)

class DistrictWasteCollector(models.Model):
    district_waste_collector_id=models.CharField(max_length=25,primary_key=True)
    join_date = models.DateTimeField(auto_now_add=True)
    district_level = models.CharField(max_length=255, blank=True,unique=True)
    state_waste_collector_ref = models.ForeignKey(StateWasteCollector, on_delete=models.CASCADE)

    user_ref = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return str(self.district_level)