from auxiliary.read_items import dict_init_items


class _Items():
    def __init__(self):
        self._items = dict_init_items

    def items(self):
        return [Item(id_) for id_ in sorted(self._itemss)]

    def get_item_info(self, item_id):
        info = self._items.get(item_id)
        if not info:
            raise ValueError('invalid item_id')
        return info


class Item():  # can inherit from a mixin class for easy output/log
    def __init__(self, id):
        self.id = id
        info = items.get_item_info(self.id)
        self.name = info.get('name')
        # get tpye
        # has component
        # belongs to
        # current position
        # initial position
        # initial time
        # other extendable/optional attribubes

    def move(self, target):
        pass

    def log_something(self):
        pass

items = _Items()
