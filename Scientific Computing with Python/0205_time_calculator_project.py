def add_time(start, duration, starting_day=None):
    start_hour, rest = start.split(":")
    start_minute, period = rest.split(" ")
    start_hour = int(start_hour)
    start_minute = int(start_minute)

    duration_hour, duration_minute = map(int, duration.split(":"))

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_index = None
    if starting_day:
        starting_day = starting_day.capitalize()
        day_index = days_of_week.index(starting_day)

    total_minutes = start_minute + duration_minute
    extra_hour = total_minutes // 60
    new_minute = total_minutes % 60

    total_hours = start_hour + duration_hour + extra_hour
    periods_passed = total_hours // 12
    new_hour = total_hours % 12
    if new_hour == 0:
        new_hour = 12

    total_periods = periods_passed + (0 if period == "AM" else 1)
    new_period = "AM" if total_periods % 2 == 0 else "PM"

    total_days = total_periods // 2

    if day_index is not None:
        day_index = (day_index + total_days) % 7
        result_day = days_of_week[day_index]
    else:
        result_day = None

    result = f"{new_hour}:{new_minute:02d} {new_period}"
    if result_day:
        result += f", {result_day}"
    if total_days == 1:
        result += " (next day)"
    elif total_days > 1:
        result += f" ({total_days} days later)"

    return result