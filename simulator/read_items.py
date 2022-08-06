import os
import csv

class ReadItems():
    """ a singleton to read a input_path/*.items.csv and convert it to a 
    dictionary for the initial placement of items in the simulation """

    def __init__(self, input_path):
        self.dict_init_items = {}
        csv_files = [file for file in os.listdir(input_path)
                     if file.endswith('.items.csv')]
        if len(csv_files) != 1:
            raise ValueError(f"should be only one .items.csv file in the "
                             +f"{input_path} directory")
        self.csv_file = input_path+csv_files[0]

    def place_items(self):
        with open(self.csv_file) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                id = row.pop("item", None)
                self.dict_init_items[id] \
                    = {key: value for key, value in row.items() if value}
        return self.dict_init_items


if __name__ == "__main__":
    input_path = "/Users/yaofuzhou/Documents/ValueChainSimulator/valuechain/scenarios/test/"
    a = ReadItems(input_path)

    print(a.place_items())
