import datetime
import calendar

# from dateutil.easter import easter

# def calculate_good_friday(year):
#     easter_date = easter(year)
#     good_friday_date = easter_date - datetime.timedelta(days=2)
#     return good_friday_date

# year = 2023  # Replace with the desired year
# good_friday_date = calculate_good_friday(year)
# print(f"Good Friday in {year} is on: {good_friday_date}")


def authenticate_holidays(null_dates):
    holidays = []
    for date in null_dates:
        # date = datetime.datetime(date)
        if check_holiday(date):
            holidays.append(date)
    return holidays


def check_holiday(date):
    date = date.to_pydatetime()
    # print("type(date)", type(date))
    week = date.weekday()  # 0 -> sunday 6 -> saturday
    week_day = calendar.day_name[week]
    day = date.day
    month = date.month
    year = date.year
    # print("month", month)
    list_holidays = {
        1: [(1, "all"), (2, "Monday")] + [(i, "Monday") for i in range(15, 22)],
        2: [(i, "Monday") for i in range(15, 22)],
        3: [],
        4: [],
        5: [(i, "Monday") for i in range(25, 32)],
        6: [],
        7: [(4, "all"), (5, "Monday"), (3, "Friday")],
        8: [],
        9: [(i, "Monday") for i in range(1, 8)],
        10: [],
        11: [(i, "Thursday") for i in range(22, 29)],
        12: [(25, "all"), (24, "Friday"), (26, "Monday")]
    }

    good_fridays = [datetime.date(2010, 4, 2), datetime.date(2011, 4, 22), datetime.date(2012, 4, 6), datetime.date(
        2013, 3, 29), datetime.date(2014, 4, 18), datetime.date(2015, 4, 3), datetime.date(2016, 3, 25)]
    for holiday in list_holidays[month]:
        if day == holiday[0] and week_day == holiday[1]:
            return True
    if date.date() in good_fridays:
        return True
    return False
