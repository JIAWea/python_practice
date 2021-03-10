import time

import rx
import rxbp
from rxbp.schedulers.threadpoolscheduler import ThreadPoolScheduler
from rxbp.testing.tobserver import TObserver


def handler(observer, scheduler):
    for i in range(1_000_000):
        observer.on_next(i)
    observer.on_completed()


# 由于使用默认 scheduler 推送数据，scheduler 从一开始调度就被占用，只能等待所有数据推送完毕消费者才能消费
# 否则需要使用其他线程进行推送，例如使用 ThreadPoolScheduler
publisher = rxbp.from_rx(rx.create(handler), batch_size=1)
publisher = publisher.pipe(
    # rxbp.op.observe_on(scheduler=ThreadPoolScheduler("receiver"))
)
sink = TObserver(immediate_continue=5)
# publisher.subscribe(observer=sink)
publisher.subscribe(observer=sink, subscribe_scheduler=ThreadPoolScheduler("publisher"))

time.sleep(1)
print("received: ", sink.received)
