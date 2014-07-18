from multiprocessing import current_process
from multiprocessing.pool import Pool
import atexit

from lmh.lib.init import std, err

class Generator():
    def __init__(self, verbose, quiet, **config):
        # Inits options
        self.supportsMoreThanOneWorker = True # Do we allow more than one worker?
        self.prefix = "GEN" # Some prefix for logs
    def needs_file(self,module, gen_mode):
        # Check if we need a job
        return False
    def make_job(self,module):
        # Creates a job from a file
        pass
    def run_init(self,worker_id):
        # Initlaises Running jobs (called once per worker, worker_id == None => Master)
        return True
    def run_deinit(self, worker_id):
        # Deinitalises running jobs (called once per worker, worker_id == None => Master)
        return True
    def run_job(self,job,worker_id):
        # Runs a single job
        return True
    def dump_init(self):
        # initialisation code for dumping.
        return True
    def dump_deinit(self):
        # deinitalisation code for dumping.
        return True
    def dump_job(self, job):
        # Dumps a job to the command line.
        return True

def run(modules, simulate, update_mode, verbose, quiet, num_workers, GeneratorClass, **config):

    # Create generator and job list
    the_generator = GeneratorClass(verbose, quiet, **config)
    jobs = []

    # All the modules which need to be generated should be added in the list
    for m in modules:
        if the_generator.needs_file(m, update_mode):
            jobs.append((m, the_generator.make_job()))

    if simulate:
        return run_simulate(the_generator, jobs, quiet)
    else:
        return run_generate(the_generator, num_workers, jobs, quiet)


def run_simulate(the_generator, jobs, quiet, verbose):

    # Initialise dumping or fail
    if not the_generator.dump_init():
        if not quiet:
            err("Unable to initalise with --simulate. ")
        return (False, [], [])

    # Run all of the jobs
    for (m, j) in jobs:
        if not the_generator.dump_job(j):
            if not quiet:
                err("Unable to dump job. ")
            return (False, [], [])

    # Deinitalise everything
    if not the_generator.dump_deinit():
        err("Unable to deinitalise with --simulate. ")
        return (False, [], [])

    # Thats it
    return (True, [], [])

def run_generate(the_generator, num_workers, jobs, quiet):
    # What worked, what didn't
    successes = []
    fails = []

    if the_generator.supportsMoreThanOneWorker and num_workers != 1:
        # Multiple Code here
        if not the_generator.run_init(None):
            err("Unable to intialise main Worker. ")
            return False

        # Create the worker Pool
        the_worker_pool = Pool(processes=num_workers, initaliser=worker_initer,initargs=[the_generator])

        res = the_worker_pool.map(lambda j:worker_runner(j, quiet, the_generator), jobs)

        the_worker_pool.close()
        the_worker_pool.join()

        for (r, (m, j)) in zip(res, jobs):
            if r:
                successes.append(m)
            else:
                fails.append(m)
    else:
        if not the_generator.run_init(None):
            err("Unable to intialise main Worker. ")
            return (False, successes, fails)

        # Run all of the jobs
        for (m, j) in jobs:
            if not run_generate_single(the_generator, None, (m, j), quiet):
                if not quiet:
                    err(the_generator.prefix, "Did not generate", m)
                    return (False, successes, fails)
                fails.append(m)
            else:
                if not quiet:
                    std(the_generator.prefix, "Generated", m)
                successes.append(m)

        if not the_generator.run_deinit(None):
            err("Unable to deintialise main Worker. ")
            return (False, successes, fails)
    return (True, successes, fails)

def worker_initer(the_generator):
    worker_id = current_process()

    def worker_deiniter():
        if not the_generator.run_deinit(worker_id)
            err("Unable to deinitalise worker", worker_id)
            raise "UnableToDeInit"

    atexit.register(lambda: worker_deiniter)

    if not the_generator.run_init(worker_id)
        err("Unable to initalise worker", worker_id)
        raise "UnableToInit"

def worker_runner(job, quiet, the_generator):
    worker_id = current_process()
    prefix = the_generator.prefix+"["+str(current_process())+"]:"
    (m, j) = job

    if not run_generate_single(the_generator, worker_id, (m, j), quiet):
        if not quiet:
            err(prefix, "Did not generate", m)
            return (False, successes, fails)
        return False
    else:
        if not quiet:
            std(prefix, "Generated", m)
        return True


def run_generate_single(the_generator, worker_id, job, quiet):
    (m, j) = job

    #Print out a debug message
    if not quiet:
        if worker_id == None:
            std(the_generator.prefix+": Generating", m)
        else:
            std(the_generator.prefix+"["+str(worker_id)+"]: Generating", m)

    # Run a job
    return the_generator.run_job(j, worker_id)