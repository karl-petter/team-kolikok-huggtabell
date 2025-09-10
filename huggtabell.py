from datetime import datetime, time, timedelta

fishing_start = time(8, 0)
fishing_end = time(17, 0)
major_weight = 2
minor_weight = 1

from astral import LocationInfo
from astral.sun import sun
from astral.moon import moonrise, moonset

def get_solunar_data(city, start_date, end_date):
    """
    Returnerar solunar-data för angiven stad och datumintervall.
    Hämtar koordinater och beräknar sol- och måntider med astral.
    """
    # Lägg till fler städer vid behov
    city_coords = {
        "åndalsnes": {"lat": 62.5667, "lon": 7.6911, "region": "Norway"},
    }
    city_key = city.lower()
    if city_key not in city_coords:
        raise ValueError(f"Stad '{city}' stöds inte.")
    coords = city_coords[city_key]
    location = LocationInfo(city, coords["region"], "Europe/Oslo", coords["lat"], coords["lon"])

    result = {}
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        s = sun(location.observer, date=current, tzinfo=location.timezone)
        try:
            mrise = moonrise(location.observer, date=current, tzinfo=location.timezone)
        except Exception:
            mrise = None
        try:
            mset = moonset(location.observer, date=current, tzinfo=location.timezone)
        except Exception:
            mset = None

        # Enkla solunarperioder: major = moonrise/set, minor = soluppgång/nedgång
        major = []
        if mrise and mset:
            # Major: 2h centered on moonrise and moonset
            major.append(( (mrise - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"), (mrise + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M") ))
            major.append(( (mset - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"), (mset + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M") ))
        elif mrise:
            major.append(( (mrise - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"), (mrise + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M") ))
        elif mset:
            major.append(( (mset - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"), (mset + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M") ))

        minor = []
        # Minor: 1h centered on sunrise and sunset
        minor.append(( (s["sunrise"] - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"), (s["sunrise"] + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M") ))
        minor.append(( (s["sunset"] - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"), (s["sunset"] + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M") ))

        result[date_str] = {"major": major, "minor": minor}
        current += timedelta(days=1)
    return result

def minutes_in_window(period_start, period_end, window_start, window_end):
    start = max(period_start, window_start)
    end = min(period_end, window_end)
    delta = (end - start).total_seconds() / 60
    return max(0, delta)

def calculate_solunar_points(solunar_data, fishing_start, fishing_end, major_weight, minor_weight):
    results = []
    for date_str, periods in solunar_data.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        window_start = datetime.combine(date_obj, fishing_start)
        window_end = datetime.combine(date_obj, fishing_end)

        total_points = 0

        for start_str, end_str in periods["major"]:
            start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
            minutes = minutes_in_window(start_dt, end_dt, window_start, window_end)
            total_points += minutes * major_weight

        for start_str, end_str in periods["minor"]:
            start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
            minutes = minutes_in_window(start_dt, end_dt, window_start, window_end)
            total_points += minutes * minor_weight

        results.append((date_str, int(total_points)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results

city = "Åndalsnes"
start_date = datetime(2025, 9, 1)
end_date = datetime(2025, 9, 14)
solunar_data = get_solunar_data(city, start_date, end_date)
results = calculate_solunar_points(solunar_data, fishing_start, fishing_end, major_weight, minor_weight)

print("Date       Points")
for date_str, points in results:
    print(f"{date_str}  {points}")

