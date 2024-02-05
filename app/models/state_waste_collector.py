from django.db import models
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

class StateWasteCollector(models.Model):
    state_waste_collector_id=models.CharField(max_length=25,primary_key=True)
    # first_name = models.CharField(max_length=255, blank=True)
    # last_name = models.CharField(max_length=255, blank=True)
    # phone = models.CharField(max_length=13,blank=True)
    # email = models.EmailField(max_length=255, blank=True)
    # password = models.CharField(max_length=255, blank=True,default="none")
    # age = models.IntegerField()
    # gender = models.CharField(max_length = 20,choices = GENDER,default = 'Male')
    # blood_group = models.CharField(max_length = 20,choices = BLOOD_GROUP,default = '1')
    join_date = models.DateTimeField(auto_now_add=True)
    state_level = models.CharField(max_length=255, blank=True, unique=True)
    # status = models.BooleanField(default=False)
    # delete = models.BooleanField(default=False)
    user_ref = models.OneToOneField(User, on_delete=models.SET_NULL,null=True)


    def __str__(self):
        return str(self.state_level)