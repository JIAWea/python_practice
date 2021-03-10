import multiprocessing
import random
import time
from threading import current_thread

import rx
from rx import operators as ops
from rx.scheduler import ThreadPoolScheduler


def intense_calculation(value):
    time.sleep(random.randint(5, 20) * 0.1)
    return value


def err(v):
    if v == "Beta":
        raise ValueError("not Beta")


# calculate number of CPUs, then create a ThreadPoolScheduler with that number of threads
cpu_num = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(cpu_num)

# Create Process 1
rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon").pipe(
    ops.map(lambda s: intense_calculation(s)),
    ops.map(lambda v: err(v)),
    ops.subscribe_on(pool_scheduler),
).subscribe(
    on_next=lambda s: print("PROCESS 1: {0} {1}".format(current_thread().name, s)),
    on_error=lambda e: print(e),
    on_completed=lambda: print("PROCESS 1 done!"),
)

# Create Process 2
rx.range(1, 10).pipe(
    ops.map(lambda s: intense_calculation(s)),
    ops.subscribe_on(pool_scheduler),
).subscribe(
    on_next=lambda i: print("PROCESS 2: {0} {1}".format(current_thread().name, i)),
    on_error=lambda e: print(e),
    on_completed=lambda: print("PROCESS 2 done!"),
)

# Create Process 3, which is infinite
rx.interval(1).pipe(
    ops.map(lambda i: i * 100),
    ops.observe_on(pool_scheduler),
    ops.map(lambda s: intense_calculation(s)),
).subscribe(
    on_next=lambda i: print("PROCESS 3: {0} {1}".format(current_thread().name, i)),
    on_error=lambda e: print(e),
)

input("Press any key to exit\n")
