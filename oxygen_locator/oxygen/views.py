import pandas as pd
import numpy as np
import folium,time
from geopy.geocoders import Nominatim
from geopy import distance
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .forms import *
import random

# def home(request):
#     return render(request,"oxygen/home.html")
@csrf_exempt
def oxygen(request):
    return render(request,"oxygen/oxygen.html")


def signup(request):
    cache.clear()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            print(user)
            Hospital.objects.create(userlink=user)
            messages.success(request,"Account Created Successfully")
            return redirect('login')
            
        # return render(request,'register.html',locals())
    
    else:
        form=UserCreationForm()
    return render(request,'registration/signup.html',{'form':form})


def HospitalView(request):
    if request.user.is_superuser:
        return redirect("/admin/")
    geolocator=Nominatim(user_agent="newone")
    def getloc(address):
        time.sleep(1)
        try:
            return geolocator.geocode(address)
        except:
            # messages.error(request,"Cant find location")
            return getloc(address)

    form=HospitalForm(request.POST or None,instance=Hospital.objects.get(userlink=request.user))
    if request.method=="POST":
        if form.is_valid():
            # name=form.data['userlink']
            form.save()
            hosp_user=Hospital.objects.get(userlink=request.user)
            print(hosp_user.hospital_name+",",hosp_user.city)
            location=getloc(hosp_user.hospital_name+","+hosp_user.city)
            print(location)
            hosp_user.hospital_name=hosp_user.hospital_name.title()
            hosp_user.staff_name=hosp_user.staff_name.title()
            hosp_user.city=hosp_user.city.title()
            hosp_latitude=location.latitude
            hosp_longitude=location.longitude
            hosp_user.hospital_latitude=hosp_latitude
            hosp_user.hospital_longitude=hosp_longitude
            hosp_user.save()
            # form.save()
            messages.success(request,"Data Updated Successfully")
    # messages.warning(request,"Update your oxygen!")              
    return render(request,"oxygen/hospital.html",locals())

def result(request):
    cache.clear()
    q=Place.objects.all()

    place=request.GET['Place']
    oxygen=request.GET['Oxygen']

    #creating a user agent for accessing location
    letters="ejoindnkpdw_2874"
    name=''.join(random.sample(letters,len(letters)))
    geolocator=Nominatim(user_agent=name)
    def getloc(address,count=0):
        # i=1
        # time.sleep(1)
        if count<2:
            try:
                return geolocator.geocode(address)
            except:
                count+=1
                print("loading")
                return getloc(address,count)
        else:
            return None

    #returning location
    
    # if getloc(place)==None:
    #     for i in q:
    #         if i.place_name.lower()==place.lower():
    #             loc1=[float(i.place_latitude),float(i.place_longitude)]
    #             print(i.place_latitude,i.place_longitude)
    #             break;
    #     print("db")
    #     print(loc1)
    
    # else:
    #     loc=getloc(place)
    #     loc1=[loc.latitude,loc.longitude]
    #     print("by func")
    #     print(loc1)
        
    if getloc(place)==None:
        obj=Place.objects.get(place_name=place)
        print(obj)
        if obj!=None:
            print(obj)
            # obj=Place.objects.get(place_name=place)
            loc1=[float(obj.place_latitude),float(obj.place_longitude)]
            print(obj.place_latitude,obj.place_longitude)
        else:
            messages.error("Can't Find the coordinates! Please try again!")
    
    else:
        loc=getloc(place)
        loc1=[loc.latitude,loc.longitude]



    #Adding Distance 
    l1=[]
    for i in Hospital.objects.filter(oxygen_supply__gte=oxygen):
        loc3=[float(i.hospital_latitude),float(i.hospital_longitude)]
        dist1=distance.distance(loc1,loc3).km
        dist=round(dist1,2)
        t1=(i.id,dist)
        l1.append(t1)
        t2=tuple(l1)

    t2=sorted(t2,key=lambda x:x[1])
    print(t2)

    #creating map using folium
    map_sam=folium.Map(loc1,tiles="openstreetmap",zoom_start=9,width=1500,height=650)
    #Marker for the corresponding location
    folium.Marker(location=loc1,popup=["You're here \n",place],tooltip="Click here to see popup",icon=folium.Icon(color="darkpurple",icon_color='lightgray',icon="male",prefix="fa")).add_to(map_sam)

    hos_list=[]
    for i in t2:
        sep_hosp=Hospital.objects.get(id=i[0])
        context={"name":sep_hosp.hospital_name,
                "address":sep_hosp.address,
                "city":sep_hosp.city,
                "staff_name":sep_hosp.staff_name,
                "contact_number":sep_hosp.contact,
                "distance":i[1],
                "oxygen_supply":sep_hosp.oxygen_supply,
                "oxygen":oxygen
                }
        hos_list.append(context)  
        loc3=[float(sep_hosp.hospital_latitude),float(sep_hosp.hospital_longitude)]

        folium.Marker(loc3,
                      tooltip="Click to view details",
                      popup=["Name:",sep_hosp.hospital_name,
                            "\nOxygen Available:",sep_hosp.oxygen_available,
                            "\nDistance:",i[1],"km"],
                            icon=folium.Icon(color="red",icon="hospital-o",icon_color="white",prefix="fa")).add_to(map_sam)
    map_sam=map_sam._repr_html_()  
    return render(request,"oxygen/result.html",locals())

def loaddata(request):
    df=pd.read_csv("oxygen/places.csv")
    row_iter=df.iterrows()
    

    objs=[
        Place(
            place_name=row["places"],
            place_latitude=row["latitude"],
            place_longitude=row["longitude"]
        )
        for i,row in row_iter
    ]
    Place.objects.bulk_create(objs)
    # df1=pd.read_csv("hospital.csv")
    #  # row_iter1=df1.iterrows()
    # objs1=[
    #     Hospital(
    #         hosp_name=row["hosp_name"],
    #         addr=row["addr"],
    #         h_latitude=row["latitude"],
    #         h_longitude=row["longitude"],
    #         incharge=row["incharge"],
    #         mob_num=row["mob_num"],
    #         o2_avail=row["o2_avail"],
    #         o2_supply=row["o2_supply"]
    #     )
    #     for i,row in row_iter1
    # ]
    # Hospital.objects.bulk_create(objs1)
# Create your views here.
