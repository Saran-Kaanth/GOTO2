from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.exceptions import ValidationError

def check_num(value):
    leng=len(str(value))
    if leng<10:
        raise ValidationError("Invalid Contact Number")
    else:
        return value


class Hospital(models.Model):
    userlink=models.OneToOneField(User,on_delete=models.CASCADE,blank=True)
    hospital_name=models.CharField(max_length=100,blank=True,null=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    hospital_latitude=models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)
    hospital_longitude=models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)
    staff_name=models.CharField(max_length=30,blank=True,null=True)
    contact=models.CharField(max_length=15,blank=True,null=True,validators=[check_num])
    oxygen_available=models.FloatField(blank=True,null=True)
    oxygen_supply=models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.userlink.username


class Place(models.Model):
    place_name=models.CharField(max_length=200)
    place_latitude=models.DecimalField(max_digits=9,decimal_places=6)
    place_longitude=models.DecimalField(max_digits=9,decimal_places=6)

# Create your models here.
  # def __str__(self):
    #     len=0
    #     temp=self.contact
    #     while(temp):
    #         leng=leng+1
    #         temp=temp//10
        
    #     if(leng>11 or leng<10):
    #         raise ValidationError("Enter Valid Contact number")
    #     else:
    #         return self.contact

    # def __str__(self):
    #     return self.hospital_name.title()
