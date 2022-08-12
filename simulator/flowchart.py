class Flowchart():

    def __init__(self, _steps, _items):
        self._steps = _steps
        self._items = _items
        self._state = self._steps

    def display_flowchart(self):
        return self._steps

    def display_init_items(self):
        return self._items

    def put_items_on_steps(self):  # put items on flowchart. works!
        for key, value in self._items.items():
            if "initial_position" in value:
                self._state[value["initial_position"]][key] = value

        print("\n state:\n", self._state, "\n")

    def move_once(self):  # trying to move items once to the next step
        self._previous_state = self._state  # saved for conflict resolution

        for step_id, items_ in self._state.items():
            if isinstance(items_, dict):
                for item_id, item_info in list(items_.items()):
                    if "type" in item_info and item_info["type"] == "next":
                        next_step = item_info["next"]
                        print(next_step)
                    if "type" in item_info and item_info["type"] == "item":
                        moved_item = items_.pop(item_id)
                        self._state[next_step][item_id] = moved_item

        print("\n state:\n", self._state, "\n")

        # self._new_state

    # keep items not let in in the gates? Or where to put awaiting items
