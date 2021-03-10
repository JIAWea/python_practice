"""

使用 rxbp.from_rx 来创建一个 Flowable 发送数据效率比 rx 低很多

"""
import time
from threading import Thread

import rx
import rxbp
from rx.scheduler import TimeoutScheduler
from rxbp.acknowledgement.acksubject import AckSubject
from rxbp.acknowledgement.continueack import continue_ack
from rxbp.observer import Observer
from rxbp.schedulers.timeoutscheduler import TimeoutScheduler
from rxbp.schedulers.eventloopscheduler import EventLoopScheduler
from rxbp.schedulers.threadpoolscheduler import ThreadPoolScheduler
from rxbp.testing.tobserver import TObserver


class TASubscribe(Observer):
    def __init__(self):
        self.request_n = 2

    def on_next(self, val):
        """
        :return: 如果返回 AckSubject 则会向 Observable 反压，即不会再发送数据
        """

        print("Received: ", val)
        self.request_n -= 1

        if self.request_n < 1:
            reture_ack = AckSubject()
            self.ack = reture_ack
            return reture_ack

        return continue_ack

    def on_completed(self):
        print('Done!')

    def on_error(self, exc):
        print('Exception: ', exc)


def handler(observer, scheduler):
    for i in range(100_000):
        observer.on_next(i)
    observer.on_completed()


def create_flowable():
    # range(100_000)
    # rxbp.from_rx(rx.create(handler), is_batched=True).subscribe(observer=TASubscribe())
    # >>> Done!
    # >>> create_from_rx: spend 5.65883731842041

    # range(100_000)
    # rxbp.from_rx(rx.create(handler), batch_size=1).subscribe(observer=TASubscribe())
    # >>> Done!
    # >>> create_from_rx: spend 13.459003210067749

    # range(100_000)
    # rxbp.from_rx(rx.create(handler), batch_size=10).subscribe(observer=TASubscribe())
    # >>> Done!
    # >>> create_from_rx: spend 1.4401209354400635

    # range(100_000)
    # rxbp.from_rx(rx.create(handler), batch_size=1000).subscribe(observer=TASubscribe())
    # >>> Done!
    # >>> create_from_rx: spend 0.1825110912322998

    # range(100_000)
    # source = rxbp.from_rx(rx.create(handler), batch_size=1000).pipe(rxbp.op.first())
    # source.subscribe(observer=sink)
    # >>> Done!
    # >>> create_from_rx: spend 0.19148802757263184
    pass


def create_rx():
    # range(100_000)
    rx.create(handler).subscribe(observer=TASubscribe())
    # >>> Done!
    # >>> create_rx: spend 0.015957117080688477


def from_rx_iterable():
    source = rxbp.from_rx(rx.of(1, 3, 5, 7, 9, 11, 13, 15))
    sink = TObserver(immediate_continue=5)
    # sink = TASubscribe()
    # source.subscribe(observer=sink)
    source.subscribe(observer=sink, subscribe_scheduler=ThreadPoolScheduler("publisher"))
    time.sleep(1)
    assert sink.received == [1, 3, 5, 7, 9, 11]


if __name__ == '__main__':
    # start = time.time()
    # print('create_rx: spend {}'.format(time.time() - start))

    # create_flowable()

    create_rx()

    # from_rx_iterable()
