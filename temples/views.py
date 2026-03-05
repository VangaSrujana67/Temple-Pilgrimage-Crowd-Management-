from django.shortcuts import render, get_object_or_404
from math import radians, cos, sin, asin, sqrt
from .models import Temple
from django.db.models import Q
from crowd_ai.logic import predict_crowd
from datetime import date
from bookings.models import DarshanSlot
from django.utils import timezone

def temple_list(request):
    # Retrieve GET parameters from the search form
    query = request.GET.get('q')
    state_filter = request.GET.get('state')
    
    temples = Temple.objects.all()
    
    # Requirement F.6: Filter by Name or District
    if query:
        temples = temples.filter(
            Q(name__icontains=query) | 
            Q(district__icontains=query)
        )
    
    # Requirement F.7: Filter by State
    if state_filter:
        temples = temples.filter(state=state_filter)
        
    return render(request, 'temples/temple_list.html', {'temples': temples})

def temple_detail(request, pk):
    temple = get_object_or_404(Temple, pk=pk)
    today = date.today()

    # ✅ AI crowd prediction
    status, reason = predict_crowd(temple, today)

    # ✅ IMPORTANT: fetch future darshan slots for this temple
    slots = DarshanSlot.objects.filter(
        temple=temple,
        date__gte=timezone.localdate()
    ).order_by("date", "slot_type")

    context = {
        'temple': temple,
        'crowd_status': status,
        'crowd_reason': reason,
        'slots': slots,  # 🔴 THIS WAS MISSING
    }

    return render(request, 'temples/temple_detail.html', context)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Requirement 3: Haversine formula to find distance in KM
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c

def nearby_temples(request):
    import requests

    user_lat = request.GET.get('lat')
    user_lon = request.GET.get('lon')

    temples = []

    if user_lat and user_lon:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)

            overpass_query = f"""
            [out:json][timeout:15];
            node["amenity"="place_of_worship"]["religion"="hindu"]
            (around:30000,{user_lat},{user_lon});
            out 50;
            """

            response = requests.get(
                "https://overpass.kumi.systems/api/interpreter",
                params={"data": overpass_query},
                timeout=20
            )

            data = response.json()

            print("Overpass results:", len(data.get("elements", [])))  # Debug

            for element in data.get("elements", []):
                name = element.get("tags", {}).get("name", "Temple")
                lat = element.get("lat")
                lon = element.get("lon")

                if lat and lon:
                    temples.append({
                        "name": name,
                        "latitude": lat,
                        "longitude": lon
                    })

        except Exception as e:
            print("Overpass error:", e)

    return render(request, "temples/nearby_temples.html", {
        "temples": temples
    })

def live_temple_detail(request):
    context = {
        "name": request.GET.get("name"),
        "lat": request.GET.get("lat"),
        "lon": request.GET.get("lon"),
        "street": request.GET.get("street"),
        "city": request.GET.get("city"),
        "wheelchair": request.GET.get("wheelchair"),
        "wikipedia": request.GET.get("wikipedia"),
    }
    return render(request, "temples/live_temple_detail.html", context)
