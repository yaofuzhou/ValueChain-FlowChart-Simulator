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
        for key, value in self._state.items():
            for child_key, child_value in value:
                if child_value["type"] == "next":
                    next_ = child_value["next"]

                    item_ = self._state.pop()
                    pass
        # self._new_state

    # keep items not let in in the gates?
