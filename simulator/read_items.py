class ReadItems():
    """ a singleton to read a input_path/*.items.csv and convert it to a 
    dictionary of items for the simulation """

    def __init__(self, input_path):
        self.dict_items = {1:"bad", 2:"worse"}

    def generate_items(self):
        return self.dict_items


if __name__ == "__main__":
    a = ReadItems()
    print(a.generate_items())