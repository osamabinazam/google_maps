from django.shortcuts import render, HttpResponse
from .models import User
import googlemaps
from django.conf import settings
from datetime import datetime



# Create your views here.
def index (request):

    # Access API key Defined in setting.py file in project level directory
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    # Fixed destination of IBA Sukkur University
    destination = ( 27.727215611705144, 68.81900645847442)

    # Retrieving data from database
    users = User.objects.all()
    number_of_users = User.objects.all().count()

    # Current Time 
    current_time = datetime.now()  # Use current time as departure_time
    total_distance = 0  # Initialize total distance
    driving_total_time = 0      # Initialize total time
    walking_total_time=0
    results = []
    # 
    for user in users:

        # Making an API call to get the time through driving model
        origin = (user.latitude, user.longitude)
        driving_results = gmaps.distance_matrix(
            origins=origin,
            destinations=destination,
            departure_time=current_time,
            mode="driving",
            traffic_model="best_guess"
        )

        driving_eta_seconds = driving_results['rows'][0]['elements'][0]['duration_in_traffic']['value']
        driving_eta_minutes = driving_eta_seconds // 60
        driving_distance = (driving_results['rows'][0]['elements'][0]['distance']['value'])/1000


        # Making an API call to get the time through walking model
        origin = (user.latitude, user.longitude)
        walking_results = gmaps.distance_matrix(
            origins=origin,
            destinations=destination,
            departure_time=current_time,
            mode="walking",
        )

        walking_eta_seconds = walking_results['rows'][0]['elements'][0]['duration']['value']
        walking_eta_minutes = walking_eta_seconds // 60

        # Calculating total distance and time(minutes)
        total_distance +=(driving_distance)
        driving_total_time += (driving_eta_minutes)
        walking_total_time += walking_eta_minutes

        results.append({
            "user": f"{user.f_name} {user.l_name}",
            "latitude": user.latitude,
            "longitude":user.longitude,
            "driving_eta_minutes":f"{ driving_eta_minutes}  minutes" ,
            "driving_distance": f"{driving_distance} km",
            "walking_eta_minutes":f"{walking_eta_minutes} minutes",
        })
        
    
    # Calculating Averages
    average_distance = total_distance / number_of_users  # Calculate average distance

    context = {
        'results': results, 
        'average_distance': average_distance,
        'total_distance':total_distance,
        'driving_total_time':driving_total_time,
        'walking_total_time':walking_total_time,
        'total_distance':total_distance
        
        }
    return render(request, 'index.html', context)

