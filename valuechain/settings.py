"""Value Chain Simulator global settings mdule

Reads in user settings from settings.cfg and store the information in
the variables.

Generate a default settings.cfg file if it is not found in the starting
directory.
"""

import os
import time
from datetime import date, datetime, timedelta
import re
from numpy.random import SeedSequence, default_rng

_settings_file = os.path.join(os.getcwd(), "settings.cfg")
_results_dir = os.path.join(os.getcwd(), "results/")
_result_dir_relative = "result_" + "_".join(time.asctime().replace(":", "")
                                                .split())
_result_dir = os.path.join(_results_dir, _result_dir_relative)

_enable_hyperthreading_accepts = ["true", "false", "yes", "no", "y", "n"]
_true_accepts = ["true", "yes", "y"]
_false_accepts = ["false", "no", "n"]
_ini_datetime_accepts = [
    "today", "now", "tomorrow", "yesterday", "yyyy-mm-dd",
    "yyyy-mm-dd HH:MM:SS.SS"
]
_final_datetime_accepts = list(
    (*_ini_datetime_accepts, "\n# +[integer] day(s)", "+HH:MM:SS.SS",
     "+[integer] day(s) HH:MM:SS.SS")
)

format_datetime = re.compile(
    r"(?P<date>(?P<YYYY>\d{4})[-/\.]?(?P<mm>0[1-9]|1[0-2])[-/\.]?"
    + r"(?P<dd>[0-2][0-9]|3[01]))\s*"
    + r"(?P<time>(?P<HH>[0-1][0-9]|2[0-3]):?(?P<MM>[0-5][0-9]):?"
    + r"(?P<SS>[0-5][0-9](\.\d*)?))?"
)

format_delta_daytime = re.compile(
    r"(?=\S)(((?P<d_day>^[1-9]\d*)\s*(day|days|day\(s\))\s*)?"
    + r"(?P<d_time>(?P<d_HH>[0-1][0-9]|2[0-3]):?(?P<d_MM>[0-5][0-9]):?"
    + r"(?P<d_SS>[0-5][0-9](\.\d*)?)?))"
    )

input_path_default = "scenarios/input/"
seed_default = 20
num_trials_default = 20
ini_datetime_default = "now"
final_datetime_default = (datetime.now() + timedelta(days=30)) \
    .strftime("%Y-%m-%d %H:%M:%S")
num_bins_default = 20
num_CPUs_default = "all"
enable_hyperthreading_default = True
num_logged_trials_default = 20
log_path_default = "results/result/"


def _cre_default_settings_file():
    with open(_settings_file, 'x') as fout:
        fout.write("# Value Chain Simulator user settings\n")
        fout.write("\n")
        fout.write("# Path to input files\n")
        fout.write(f"input_path = {input_path_default}\n")
        fout.write("\n")
        fout.write("# Random seed.\n")
        fout.write("# Accepts: left empty, integer\n")
        fout.write(f"seed = {seed_default}\n")
        fout.write("\n")
        fout.write("# Number of simulation trials\n")
        fout.write(f"num_trials = {num_trials_default}\n")
        fout.write("\n")
        fout.write("# Initial datetime of simulation.\n")
        fout.write(
            f"# Accepts: {', '.join(str(x) for x in _ini_datetime_accepts)}\n"
            )
        fout.write(f"ini_datetime = {ini_datetime_default}\n")
        fout.write("\n")
        fout.write("# Final datetime of simulation.\n")
        fout.write(
            f"# Accepts: {', '.join(str(x) for x in _final_datetime_accepts)}"
            + "\n"
            )
        fout.write(f"final_datetime = {final_datetime_default}\n")
        fout.write("\n")
        fout.write("# Number of histogram bins\n")
        fout.write(f"num_bins = {num_bins_default}\n")
        fout.write("\n")
        fout.write("# Number of CPU cores\n")
        fout.write("# Accepts: left empty, all, integer\n")
        fout.write("# If left empty, system default will be applied.\n")
        fout.write(f"num_CPUs = {num_CPUs_default}\n")
        fout.write("\n")
        fout.write("# Enable hyperthreading\n")
        fout.write(
            "# Accepts: "
            + f"{', '.join(str(x) for x in _enable_hyperthreading_accepts)}\n"
            )
        fout.write(
            f"enable_hyperthreading = {enable_hyperthreading_default}\n"
            )
        fout.write("\n")
        fout.write("# Number of simulation trials to log\n")
        fout.write(f"num_logged_trials = {num_logged_trials_default}\n")
        fout.write("\n")
        fout.write("# Path to logs and simulation results\n")
        fout.write(
            "# If not path is given, a default folder will be created under "
            + "results/\n"
            )
        fout.write(f"log_path = {log_path_default}\n")


try:
    open(_settings_file)
except FileNotFoundError:
    print("settings.cfg not found in your Value Chain Simulator starting")
    print("directory. Creating default settings.cfg...\n")
    _cre_default_settings_file()
    print("Default settings.cfg created. Edit it and run program.py")
else:
    print(f"Reading settings from {_settings_file}...\n")
    with open(_settings_file) as fin:
        lines = (line.rstrip() for line in fin)
        lines = (line for line in lines if line)
        for line in lines:
            if line.lstrip().startswith("#"):
                continue

            elif line.lstrip().startswith("input_path"):
                input_path = line.replace("input_path", "").replace("=", "") \
                                 .replace(" ", "").replace("'", "") \
                                 .replace("\"", "")
                if not os.path.exists(input_path):
                    raise FileNotFoundError(f"{input_path} is not a valid \
                                            filename or does not exist.")

            elif line.lstrip().startswith("seed"):
                seed_ = line.replace("seed", "").replace("=", "") \
                            .replace(" ", "").replace("'", "") \
                            .replace("\"", "")
                if seed_ == "":
                    seed_ = None
                elif seed_.isnumeric():
                    seed_ = int(seed_)

            elif line.lstrip().startswith("num_trials"):
                num_trials = line.replace("num_trials", "").replace("=", "") \
                                 .replace(" ", "")
                if num_trials.isnumeric():
                    num_trials = int(num_trials)
                else:
                    raise TypeError(f"{num_trials} is not an integer")

            elif line.lstrip().startswith("ini_datetime"):
                ini_datetime = line.replace("ini_datetime", "") \
                               .replace("=", "") \
                               .replace(" ", "").replace("'", "") \
                               .replace("\"", "")
                if ini_datetime.isalpha():
                    if ini_datetime == "today":
                        ini_datetime = date.today()
                        ini_datetime = datetime(
                            ini_datetime.year, ini_datetime.month,
                            ini_datetime.day
                            )
                    elif ini_datetime == "yesterday":
                        ini_datetime = date.today() - timedelta(days=1)
                        ini_datetime = datetime(
                            ini_datetime.year, ini_datetime.month,
                            ini_datetime.day
                            )
                    elif ini_datetime == "tomorrow":
                        ini_datetime = date.today() + timedelta(days=1)
                        ini_datetime = datetime(
                            ini_datetime.year, ini_datetime.month,
                            ini_datetime.day
                            )
                    elif ini_datetime == "now":
                        ini_datetime = datetime.now()
                    else:
                        raise ValueError(f"ini_datetime accepts \
                                         {_ini_datetime_accepts} .")
                else:
                    datetime_match = format_datetime.fullmatch(ini_datetime)
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
                            microsecond_ = int(
                                1000000*(float(datetime_dict.get("SS")) % 1)
                                )
                        else:
                            seconds_ = 0
                            microsecond_ = 0
                        ini_datetime = datetime(
                            year=int(datetime_dict.get("YYYY")),
                            month=int(datetime_dict.get("mm")),
                            day=int(datetime_dict.get("dd")),
                            hour=hours_,
                            minute=minutes_,
                            second=seconds_,
                            microsecond=microsecond_
                            )
                    else:
                        raise ValueError(
                            f"ini_datetime accepts {_ini_datetime_accepts}."
                            )

            elif line.lstrip().startswith("final_datetime"):
                final_datetime = line.replace("final_datetime", "") \
                               .replace("=", "") \
                               .replace(" ", "").replace("'", "") \
                               .replace("\"", "")
                if final_datetime.isalpha():
                    if final_datetime == "today":
                        final_datetime = date.today()
                        final_datetime = datetime(
                            final_datetime.year, final_datetime.month,
                            final_datetime.day
                            )
                    elif final_datetime == "yesterday":
                        final_datetime = date.today() - timedelta(days=1)
                        final_datetime = datetime(
                            final_datetime.year, final_datetime.month,
                            final_datetime.day
                            )
                    elif final_datetime == "tomorrow":
                        final_datetime = date.today() + timedelta(days=1)
                        final_datetime = datetime(
                            final_datetime.year, final_datetime.month,
                            final_datetime.day
                            )
                    elif final_datetime == "now":
                        final_datetime = datetime.now()
                    else:
                        raise ValueError(f"final_datetime accepts \
                                         {_final_datetime_accepts}.")
                elif final_datetime.startswith("+"):
                    final_datetime = final_datetime.replace("+", "")
                    delta_daytime_match = format_delta_daytime \
                        .fullmatch(final_datetime)
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
                            days=days_, hours=hours_, minutes=minutes_,
                            seconds=seconds_
                            )
                    else:
                        raise ValueError(f"final_datetime accepts \
                                         {_final_datetime_accepts}.")
                else:
                    datetime_match = format_datetime.fullmatch(final_datetime)
                    if datetime_match:
                        datetime_dict = datetime_match.groupdict()
                        final_datetime = datetime(
                            year=int(datetime_dict.get("YYYY")),
                            month=int(datetime_dict.get("mm")),
                            day=int(datetime_dict.get("dd")),
                            hour=int(datetime_dict.get("HH")),
                            minute=int(datetime_dict.get("MM")),
                            second=int(datetime_dict.get("SS"))
                            )
                    else:
                        raise ValueError(
                            "final_datetime accepts "
                            f"{_final_datetime_accepts}."
                            )

            elif line.lstrip().startswith("num_bins"):
                num_bins = line.replace("num_bins", "").replace("=", "") \
                               .replace(" ", "")
                if num_bins.isnumeric():
                    num_bins = int(num_bins)
                else:
                    raise TypeError(f"{num_bins} is not an integer")

            elif line.lstrip().startswith("num_CPUs"):
                num_CPUs = line.replace("num_CPUs", "").replace("=", "") \
                               .replace(" ", "")
                if num_CPUs.isnumeric():
                    if num_CPUs > 0:
                        num_CPUs = int(num_CPUs)
                    else:
                        raise ValueError(f"{num_CPUs} cannot specify \
                                         the number of CPUs.")
                else:
                    num_CPUs = num_CPUs.replace("'", "").replace("\"", "") \
                                       .lower()
                    if num_CPUs in ["", "all"]:
                        num_CPUs = None
                    else:
                        raise ValueError(f"{num_CPUs} cannot specify \
                                         the number of CPUs.")

            elif line.lstrip().startswith("enable_hyperthreading"):
                enable_hyperthreading = line.replace("enable_hyperthreading",
                                                     "").replace("=", "")\
                                            .replace(" ", "") \
                                            .replace("'", "").lower() \
                                            .replace("\"", "").lower()
                if enable_hyperthreading in _enable_hyperthreading_accepts:
                    if enable_hyperthreading in _true_accepts:
                        enable_hyperthreading = True
                    else:
                        enable_hyperthreading = False
                else:
                    raise ValueError(f"enable_hyperthreading accepts: \
                                     {_enable_hyperthreading_accepts}.")

            elif line.lstrip().startswith("num_logged_trials"):
                num_logged_trials = line.replace("num_logged_trials", "") \
                                        .replace("=", "").replace(" ", "")
                if num_logged_trials.isnumeric():
                    num_logged_trials = int(num_logged_trials)
                else:
                    raise TypeError(f"{num_logged_trials} is not an integer")

            elif line.lstrip().startswith("log_path"):
                log_path = line.replace("log_path", "").replace("=", "") \
                               .replace(" ", "").replace("'", "") \
                               .replace("\"", "")
                if log_path.lower() in ["", "default", "none"]:
                    print(f"No log_path given. Using default log_path: \
                          {_result_dir} .")
                    try:
                        os.makedirs(_result_dir)
                    except FileExistsError:
                        print(f"{_result_dir} already exists.")
                else:
                    try:
                        os.makedirs(log_path)
                    except FileExistsError:
                        print(f"{log_path} already exists.")

            else:
                raise ValueError(f"Invalid setting: {line}")


if not num_CPUs:
    num_CPUs = os.cpu_count()
if enable_hyperthreading:
    if not num_CPUs:
        num_CPUs = 2*os.cpu_count()
    else:
        num_CPUs = 2 * num_CPUs


_ss = SeedSequence(entropy=seed_)
seed_list = _ss.spawn(num_trials)
rng_list = [default_rng(s) for s in seed_list]


if __name__ == "__main__":
    print(f"\nused settings from {_settings_file}:\n")
    print("input_path", type(input_path), input_path)
    print("seed_", type(seed_), seed_)
    print("num_trials", type(num_trials), num_trials)
    print("ini_datetime", type(ini_datetime), ini_datetime)
    print("final_datetime", type(final_datetime), final_datetime)
    print("num_bins", type(num_bins), num_bins)
    print("num_CPUs", type(num_CPUs), num_CPUs)
    print("enable_hyperthreading", type(enable_hyperthreading),
          enable_hyperthreading)
    print("num_logged_trials", type(num_logged_trials), num_logged_trials)
    print("log_path", type(log_path), log_path)
