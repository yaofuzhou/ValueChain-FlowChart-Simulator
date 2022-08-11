import os
import csv


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
        dict_csv_file = {}
        with open(self.csv_file) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                id = row.pop("step", None)
                dict_csv_file[id] \
                    = {key: value for key, value in row.items() if value}

        for key, value in dict_csv_file.items():
            if "parent_id" not in value:
                self.dict_flowchart[key] = value
            else:
                id = value.pop("parent_id")
                self.dict_flowchart[id][key] = value

        return self.dict_flowchart


if __name__ == "__main__":
    input_path = "/Users/yaofuzhou/Documents/ValueChainSimulator/" \
        + "valuechain/scenarios/test/"
    a = ReadSteps(input_path)

    print(a.generate_flowchart())
