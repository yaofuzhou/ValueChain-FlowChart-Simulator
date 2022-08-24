"""Convert relevant strings to datetime objects"""

import re
from datetime import date, datetime, timedelta

datetime_accepts = ("today", "now", "tomorrow", "yesterday", "yyyy-mm-dd",
                    "yyyy-mm-dd HH:MM:SS.SS")

delta_datetime_accepts = ("+[integer] day(s)", "+HH:MM:SS.SS",
                          "+[integer] day(s) HH:MM:SS.SS")

final_datetime_accepts = (
    *datetime_accepts, "\n# +[integer] day(s)", "+HH:MM:SS.SS",
    "+[integer] day(s) HH:MM:SS.SS")

format_datetime = re.compile(
    r"(?P<date>(?P<YYYY>\d{4})[-/\.]?(?P<mm>0[1-9]|1[0-2])[-/\.]?"
    + r"(?P<dd>[0-2][0-9]|3[01]))\s*"
    + r"(?P<time>(?P<HH>[0-1][0-9]|2[0-3]):?(?P<MM>[0-5][0-9]):?"
    + r"(?P<SS>[0-5][0-9](\.\d*)?))?"
    )

format_delta_daytime = re.compile(
    r"\s*\+\s*(?=\S)(((?P<d_day>[1-9]\d*)\s*(day|days|day\(s\))\s*)?"
    + r"(?P<d_time>(?P<d_HH>[0-1][0-9]|2[0-3]):?(?P<d_MM>[0-5][0-9]):?"
    + r"(?P<d_SS>[0-5][0-9](\.\d*)?)?\s*)?)"
    )


def start_with_plus(line):
    if line.replace(" ", "").replace("'", "").replace("\"", "") \
           .startswith("+"):
        return True
    else:
        return False


def str_to_datetime(datetime_str):
    datetime_str = datetime_str.replace(" ", "").replace("'", "") \
        .replace("\"", "")

    if datetime_str.isalpha():
        today_ = date.today()
        if datetime_str == "today":
            datetime_ = datetime(today_.year, today_.month, today_.day)
        elif datetime_str == "yesterday":
            yesterday_ = today_ - timedelta(days=1)
            datetime_ = datetime(yesterday_.year, yesterday_.month,
                                 yesterday_.day)
        elif datetime_str == "tomorrow":
            tomorrow_ = today_ + timedelta(days=1)
            datetime_ = datetime(tomorrow_.year, tomorrow_.month,
                                 tomorrow_.day)
        elif datetime_str == "now":
            datetime_ = datetime.now()
        else:
            raise ValueError("Invalid date or datetime input."
                             + f"Accepts: {datetime_accepts}."
                             + f"Received: {datetime_str}.")

    else:
        datetime_match = format_datetime.fullmatch(datetime_str)
        if datetime_match:
            datetime_dict = datetime_match.groupdict()
            if datetime_dict.get("HH"):
                hours_ = int(datetime_dict.get("HH"))
            else:
                hours_ = 0
            if datetime_dict.get("MM"):
                minutes_ = int(datetime_dict.get("MM"))
            else:
                minutes_ = 0
            if datetime_dict.get("SS"):
                seconds_ = int(float(datetime_dict.get("SS")))
                microsecond_ = int(1E6*(float(datetime_dict.get("SS")) % 1))
            else:
                seconds_ = 0
                microsecond_ = 0
            datetime_ = datetime(year=int(datetime_dict.get("YYYY")),
                                 month=int(datetime_dict.get("mm")),
                                 day=int(datetime_dict.get("dd")),
                                 hour=hours_,
                                 minute=minutes_,
                                 second=seconds_,
                                 microsecond=microsecond_
                                 )
        else:
            raise ValueError("Invalid date or datetime input. "
                             + f"Accepts: {datetime_accepts}. "
                             + f"Received: {datetime_str}.")

    return datetime_


def str_to_later_datetime(delta_datetime_str, ini_datetime):
    delta_datetime_str = delta_datetime_str.replace(" ", "").replace("'", "") \
        .replace("\"", "")

    delta_daytime_match = format_delta_daytime.fullmatch(delta_datetime_str)
    if delta_daytime_match:
        dalta_daytime_dict = delta_daytime_match.groupdict()
        if dalta_daytime_dict.get("d_day"):
            days_ = int(dalta_daytime_dict.get("d_day"))
        else:
            days_ = 0
        if dalta_daytime_dict.get("d_HH"):
            hours_ = int(dalta_daytime_dict.get("d_HH"))
        else:
            hours_ = 0
        if dalta_daytime_dict.get("d_MM"):
            minutes_ = int(dalta_daytime_dict.get("d_MM"))
        else:
            minutes_ = 0
        if dalta_daytime_dict.get("d_SS"):
            seconds_ = float(dalta_daytime_dict.get("d_SS"))
        else:
            seconds_ = 0
        final_datetime = ini_datetime + timedelta(
            days=days_, hours=hours_, minutes=minutes_, seconds=seconds_
            )
    else:
        raise ValueError("Invalid input for date or datetime difference. "
                         + f"Accepts: {delta_datetime_accepts}. "
                         + f"Received: {delta_datetime_str}.")

    return final_datetime


if __name__ == "__main__":
    datetime_str = "2022-09-09"
    if format_datetime.fullmatch(datetime_str):
        print(f'{datetime_str} matches')

    delta_datetime_str = "+ 30days 13:13:45.55"
    if format_delta_daytime.fullmatch(delta_datetime_str):
        print(f'{delta_datetime_str} matches')

    ini_datetime = str_to_datetime(datetime_str)
    print("\n", "ini_datetime =", ini_datetime, "\n")

    final_datetime = str_to_later_datetime(delta_datetime_str, ini_datetime)
    print("\n", "final_datetime =", final_datetime, "\n")
