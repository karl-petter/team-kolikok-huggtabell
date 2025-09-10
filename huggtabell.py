from datetime import datetime, time, timedelta

fishing_start = time(8, 0)
fishing_end = time(17, 0)
major_weight = 2
minor_weight = 1

def get_solunar_data(city, start_date, end_date):
    """
    Returnerar solunar-data för angiven stad och datumintervall.
    För närvarande stöds endast 'Åndalsnes' och datumen 2025-09-10 till 2025-09-13.
    """
    if city.lower() != "åndalsnes":
        raise ValueError("Endast 'Åndalsnes' stöds i denna version.")
    all_data = {
        "2025-09-10": {
            "major": [("2025-09-10 02:35", "2025-09-10 04:35"),
                      ("2025-09-10 14:31", "2025-09-10 16:31")],
            "minor": [("2025-09-10 10:07", "2025-09-10 12:07"),
                      ("2025-09-10 19:25", "2025-09-10 20:25")]
        },
        "2025-09-11": {
            "major": [("2025-09-11 03:31", "2025-09-11 05:31"),
                      ("2025-09-11 15:26", "2025-09-11 17:26")],
            "minor": [("2025-09-11 12:06", "2025-09-11 14:06"),
                      ("2025-09-11 19:45", "2025-09-11 20:45")]
        },
        "2025-09-12": {
            "major": [("2025-09-12 04:42", "2025-09-12 06:42"),
                      ("2025-09-12 16:26", "2025-09-12 18:26")],
            "minor": [("2025-09-12 14:17", "2025-09-12 16:17"),
                      ("2025-09-12 18:36", "2025-09-12 20:36")]
        },
        "2025-09-13": {
            "major": [("2025-09-13 05:09", "2025-09-13 07:09"),
                      ("2025-09-13 17:29", "2025-09-13 19:29")],
            "minor": [("2025-09-13 16:55", "2025-09-13 17:55"),
                      ("2025-09-13 18:04", "2025-09-13 20:04")]
        }
    }

    result = {}
    current = start_date
    while current <= end_date:
        key = current.strftime("%Y-%m-%d")
        if key in all_data:
            result[key] = all_data[key]
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
start_date = datetime(2025, 9, 10)
end_date = datetime(2025, 9, 13)
solunar_data = get_solunar_data(city, start_date, end_date)
results = calculate_solunar_points(solunar_data, fishing_start, fishing_end, major_weight, minor_weight)

print("Date       Points")
for date_str, points in results:
    print(f"{date_str}  {points}")

