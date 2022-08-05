""" Entry point of Value Chain Simulator
This is not the start script """

from multiprocessing import Pool, Manager

from simulator.decorators import timer
from simulator.simulation import a_simulation


@timer
def main():
    import valuechain.settings as vcs
    from simulator.read_steps import ReadSteps

    manager = Manager()
    settings_queue = manager.Queue()
    steps_queue = manager.Queue()
    items_queue = manager.Queue()
    budget_schedule_queue = manager.Queue()
    result_queue = manager.Queue()

    probability_log = vcs.num_logged_trials/vcs.num_trials

    for _ in range(vcs.num_CPUs):
        settings_queue.put((vcs.ini_datetime, vcs.final_datetime, vcs.num_bins,
                            probability_log))
        
    steps_read = ReadSteps(vcs.input_path)
    dict_flowchart = steps_read.generate_flowchart()

    pool_tuple = [(i, vcs.rng_list[i], dict_flowchart, settings_queue,
                   steps_queue, items_queue, budget_schedule_queue,
                   result_queue)
                  for i in range(vcs.num_trials)]

    print(f"Starting simulation with {vcs.num_trials} trials...\n")

    with Pool(processes=vcs.num_CPUs) as pool:
        result = pool.starmap(a_simulation, pool_tuple)
        print(f"Dumping results: {result}\n")

    for i in range(vcs.num_trials):
        print(f"#{i} to finish: {result_queue.get()}")

    return "Value Chain Simulator normal end"
