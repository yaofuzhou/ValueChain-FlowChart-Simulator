class InputChecks():
    """ A singleton to read input_path/*.items.csv and *.steps.csv to check for
    obvious errors such as duplicate id's in the user input. """

    def __init__(self, input_path):
        pass

    # No duplicate id's

    # Any step leads to another step, except for the destination
