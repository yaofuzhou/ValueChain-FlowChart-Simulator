import os
import csv

from auxiliary.read_datetime import start_with_plus
from auxiliary.read_datetime import str_to_datetime, str_to_later_datetime


class ReadItems():
    """ Reads a input_path/*.items.csv and convert it to a dictionary for the
    initial placement of items in the simulation """

    def __init__(self, ini_datetime, input_path):
        self.ini_datetime = ini_datetime
        self.dict_ini_items = {}
        csv_files = [file for file in os.listdir(input_path)
                     if file.endswith('.items.csv')]
        if len(csv_files) != 1:
            raise ValueError("should be only one .items.csv file in the "
                             + f"{input_path} directory")
        self.csv_file = input_path+csv_files[0]

    def init_items(self):
        with open(self.csv_file) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                id = row.pop("item", None)
                if "initial_datetime" in row:
                    initial_datetime = row["initial_datetime"]
                    if start_with_plus(initial_datetime):
                        initial_datetime =\
                            str_to_later_datetime(initial_datetime,
                                                  self.ini_datetime)
                    else:
                        initial_datetime = str_to_datetime(initial_datetime)
                    row["initial_datetime"] = initial_datetime
                self.dict_ini_items[id] \
                    = {key: value for key, value in row.items() if value}
        return self.dict_ini_items

    def __repr__(self):
        return str(self.init_items())


if __name__ == "__main__":
    input_path = "/Users/yaofuzhou/Documents/ValueChainSimulator/" \
        + "valuechain/scenarios/test/"
    a = ReadItems(input_path)

    print(a.init_items())
