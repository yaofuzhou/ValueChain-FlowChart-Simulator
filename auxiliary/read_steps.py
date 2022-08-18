import os
import csv

from valuechain.settings import input_path


class ReadSteps():
    """ A singleton to read a input_path/*.steps.csv and convert it to a
    dictionary of flowchart for the simulation """

    def __init__(self, input_path):
        self.dict_flowchart = {}
        csv_files = [file for file in os.listdir(input_path)
                     if file.endswith('.steps.csv')]
        if len(csv_files) != 1:
            raise ValueError("should be only one .steps.csv file in the "
                             + f"{input_path} directory")
        self.csv_file = input_path+csv_files[0]

    def generate_flowchart(self):
        # self.dict_flowchart["datetime"] = ini_datetime
        with open(self.csv_file) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                id = row.pop("step", None)
                self.dict_flowchart[id] \
                    = {key: value for key, value in row.items() if value}

        for key, value in list(self.dict_flowchart.items()):
            if isinstance(value, dict) and "parent_id" in value:
                id = value.pop("parent_id")
                component = self.dict_flowchart.pop(key)
                self.dict_flowchart[id][key] = component

        return self.dict_flowchart


    def __repr__(self):
        return str(self.generate_flowchart())


# steps_read = ReadSteps()
# dict_flowchart = steps_read.generate_flowchart()
# print("\nsteps:")
# print(str(steps_read),"\n")


if __name__ == "__main__":
    input_path = "/Users/yaofuzhou/Documents/ValueChainSimulator/" \
        + "valuechain/scenarios/test/"
    a = ReadSteps(input_path)

    print(a.generate_flowchart())
