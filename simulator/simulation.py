import os
from datetime import timedelta

from simulator.decorators import slow_down
# from simulator.time_increment import TimeIncrementMixin as TIM
from simulator.items import items
from simulator.flowchart import flowchart


# @slow_down(2)
def a_simulation(trial_id, rng_, settings_queue, dict_flowchart,
                 dict_ini_items, budget_schedule_queue, result_queue):
    """Simulation Main Body"""

    ini_datetime, final_datetime, num_bins, probability_log \
        = settings_queue.get()

    flowchart.set_dict_steps(dict_flowchart)
    items.set_dict_items(dict_ini_items)
    
    steps = flowchart.steps()
    items_list = items.items()
    
    print(items_list[1].id)
    print(steps[0].id)

    day_delta = timedelta(days=1) ############
    print(f"Process {os.getpid()}: trial {trial_id} with RNG {rng_}") #########
    print(ini_datetime, final_datetime, num_bins, probability_log) ############

    for i in range((final_datetime - ini_datetime).days): #########
        # print(ini_datetime + i*day_delta)
        pass

    result = rng_.random() ############
    result_queue.put((trial_id, result)) ############
    print(trial_id, result, "\n") ############

    return trial_id, result
