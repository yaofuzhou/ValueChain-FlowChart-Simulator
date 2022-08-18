class Flowchart():
    def __init__(self):
        self._steps = {}

    def set_dict_steps(self, new_dict):
       self._steps = new_dict

    def steps(self):
        return [Step(id_) for id_ in sorted(self._steps)]

    def get_step_info(self, step_id):
        info = self._steps.get(step_id)
        if not info:
            raise ValueError('invalid step_id')
        return info


class Step():  # can inherit from a mixin class for easy output/log
    def __init__(self, id):
        self.id = id
        info = flowchart.get_step_info(self.id)
        self.name = info.get("name")
        self.type = info.get("type")
        self.description = info.get("description")
        # has component, this is something that gets updated
        # belongs to, this is something that gets updated
        # other extendable/optional attribubes

    def __repr__(self):
        return str(self.description)

    def log_something(self):
        pass


flowchart = Flowchart()