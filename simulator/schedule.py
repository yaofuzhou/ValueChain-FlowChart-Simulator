from operator import itemgetter

class Schedule:
    # 1. collect all timestamps as a list
    # 2. sort list of timestemps
    # 3. increment to the next timestamp
    # 4. evaluate an new timestamp
    # 5. insert new timestamp into sorted list of timestamps
    # 6. loop 3-5

    def __init__(self):
        self.dict_schedule = {}

    def update_schedule(self):
        self.dict_schedule = sorted(self.dict_schedule,
                                    key=itemgetter('timestamp'))

    pass
