from simulator.container import Container
from simulator.duration import Duration
from simulator.size import Size
from simulator.cost import Cost


class Items():
    def __init__(self):
        self._items = {}

    def set_dict_items(self, new_dict):
        self._items = new_dict

    def items(self):
        return [Item(id_) for id_ in sorted(self._items)]

    def get_item_info(self, item_id):
        info = self._items.get(item_id)
        if not info:
            raise ValueError('invalid item_id')
        return info


class Item():  # can inherit from a mixin class for easy output/log
    def __init__(self, id):
        self.id = id
        info = items.get_item_info(self.id)
        self.name = info.get("name")
        self.description = info.get("description")
        self.type = info.get("type")
        self.ini_position = info.get("initial_position")
        self.ini_datetime = info.get("initial_datetime")
        self.previous_position = None
        self.position = None

        container_info = []
        duration_info= []
        size_info = []
        cost_info = []
        for k, v in info.items():
            if isinstance(v, dict):
                if v["type"] == "container":
                    container_info.append(v)
                if v["type"] == "duration":
                    duration_info.append(v)
                if v["type"] == "cost":
                    size_info.append(v)
                if v["type"] == "next":
                    cost_info.append(v)

        self.container = Container(container_info)
        self.duration = Duration(duration_info)
        self.size = Size(size_info)
        self.cost = Cost(cost_info)

    def __repr__(self):
        return str(self.description)

    def move(self, target):
        # belongs to, this is something that gets updated
        # has component, this is something that gets updated
        # current position
        pass

    def log_something(self):
        pass


items = Items()
