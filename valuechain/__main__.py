""" Entry point of Value Chain Simulator
This is not the start script """

import imp
from multiprocessing import Pool, Manager

from simulator.decorators import timer
from simulator.simulation import a_simulation


@timer
def main():
    import valuechain.settings as vcs
    from simulator.read_steps import ReadSteps
    from simulator.read_items import ReadItems

    manager = Manager()
    settings_queue = manager.Queue()
    budget_schedule_queue = manager.Queue()
    result_queue = manager.Queue()

    probability_log = vcs.num_logged_trials/vcs.num_trials

    for _ in range(vcs.num_CPUs):
        settings_queue.put((vcs.ini_datetime, vcs.final_datetime, vcs.num_bins,
                            probability_log))
        
    steps_read = ReadSteps(vcs.input_path)
    dict_flowchart = steps_read.generate_flowchart()
    items_read = ReadItems(vcs.input_path)
    dict_init_items = items_read.place_items()

    pool_tuple = [(i, vcs.rng_list[i], settings_queue, dict_flowchart,
                   dict_init_items, budget_schedule_queue,
                   result_queue)
                  for i in range(vcs.num_trials)]

    print(f"Starting simulation with {vcs.num_trials} trials...\n")

    with Pool(processes=vcs.num_CPUs) as pool:
        result = pool.starmap(a_simulation, pool_tuple)
        print(f"Dumping results: {result}\n")

    for i in range(vcs.num_trials):
        print(f"#{i} to finish: {result_queue.get()}")

    return "Value Chain Simulator normal end"
