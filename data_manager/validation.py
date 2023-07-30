import datetime
import calendar
import pandas as pd

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

    good_fridays = [
        datetime.date(1984, 4, 6),
        datetime.date(1985, 3, 29),
        datetime.date(1986, 4, 11),
        datetime.date(1987, 4, 3),
        datetime.date(1988, 3, 25),
        datetime.date(1989, 4, 14),
        datetime.date(1990, 4, 6),
        datetime.date(1991, 3, 29),
        datetime.date(1992, 4, 17),
        datetime.date(1993, 4, 9),
        datetime.date(1994, 4, 1),
        datetime.date(1995, 4, 14),
        datetime.date(1996, 4, 5),
        datetime.date(1997, 3, 28),
        datetime.date(1998, 4, 10),
        datetime.date(1999, 4, 2),
        datetime.date(2000, 4, 21),
        datetime.date(2001, 4, 13),
        datetime.date(2002, 3, 29),
        datetime.date(2003, 4, 18),
        datetime.date(2004, 4, 9),
        datetime.date(2005, 3, 25),
        datetime.date(2006, 4, 14),
        datetime.date(2007, 4, 6),
        datetime.date(2008, 3, 21),
        datetime.date(2009, 4, 10),
        datetime.date(2010, 4, 2),
        datetime.date(2011, 4, 22),
        datetime.date(2012, 4, 6),
        datetime.date(2013, 3, 29),
        datetime.date(2014, 4, 18),
        datetime.date(2015, 4, 3),
        datetime.date(2016, 3, 25),
        datetime.date(2017, 4, 14),
        datetime.date(2018, 3, 30),
        datetime.date(2019, 4, 19),
        datetime.date(2020, 4, 10)
    ]
    for holiday in list_holidays[month]:
        if day == holiday[0] and week_day == holiday[1]:
            return True
    if date.date() in good_fridays:
        return True
    return False
