import os
from datetime import date, timedelta

from simulator.decorators import slow_down
from simulator.time_increment import TimeIncrementMixin as TIM
from simulator.flowchart import Flowchart

# @slow_down(2)
def a_simulation(trial_id, rng_, settings_queue, dict_flowchart,
                 dict_init_items, budget_schedule_queue, result_queue):
    """Simulation Main Body"""

    ini_datetime, final_datetime, num_bins, probability_log \
        = settings_queue.get()

    # print(dict_flowchart)
    # print(dict_init_items)
    flowchart = Flowchart(dict_flowchart, dict_init_items)

    day_delta = timedelta(days=1)
    print(f"Process {os.getpid()}: trial {trial_id} with RNG {rng_}" )
    print(ini_datetime, final_datetime, num_bins, probability_log)

    for i in range((final_datetime - ini_datetime).days):
        # print(ini_datetime + i*day_delta)
        pass

    result = rng_.random()
    result_queue.put((trial_id, result))
    print(trial_id, result, "\n")

    return trial_id, result
