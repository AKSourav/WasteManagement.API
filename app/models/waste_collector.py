from django.db import models
from .district_waste_collector import DistrictWasteCollector
from .user import User
# GENDER = (
#     ("Male", "Male"),
#     ("Female", "Female"),
#     ("Others", "Others"),
# )

BLOOD_GROUP = (
    ("1", "A+"),
    ("2", "A-"),
    ("3", "B+"),
    ("4", "B-"),
    ("5", "O+"),
    ("6", "O-"),
)

class WasteCollector(models.Model):
    waste_collector_id=models.CharField(max_length=25,primary_key=True)

    join_date = models.DateTimeField(auto_now_add=True)
    district_waste_collector_ref = models.ForeignKey(DistrictWasteCollector, on_delete=models.CASCADE)
   
    user_ref = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.waste_collector_id)