"""

Flowable: 在 rxpy 的 Observable 之上封装了一层，在 subscribe 中调用了 unsafe_subscribe 方法，然后
          再调用了 Observable 中的 observe
    - subscribe 方法是在继承的父类 FlowableSubscribeMixin 中，并在后续调用继承的父类 FlowableOpMixin 中的
      self.unsafe_subscribe，接着调用 self.underlying.unsafe_subscribe 即调用初始化后的 Flowable 的 unsafe_subscribe

扩展：
    - subscription = self.unsafe_subscribe(subscriber: Subscriber)          # scheduler
    - subscription.observable.fast_loop()

- just: 内部调用 return_value()，把它封装成一个可迭代对象 FromSingleElementFlowable()，lazy_elem=lambda: [val]

- from_range:
    - 带 batch_size:
        - 内部会把它封装成一个可迭代对象 FromIteratorObservable()，每一次迭代都是一个 range(batch_size)
        - 如果 subscribe() 中没有接收一个 Subscriber 对象，则会在内部 on_next 中接收一个可迭代对象后会 迭代调用
              observer.on_next，内部是 for x in iterable
        - 如果 subscribe() 接收一个 Subscriber 对象，则 on_next 接收到的 value 则是一个可迭代对象 FromIteratorObservable()，
              内部有一个 star_loop() 方法，每次 on_next 接收到的 value 是一个 range(batch_size)

    - 不带 batch_size
        - 内部会把它封装成一个可迭代对象 FromSingleElementFlowable()
        - 如果 subscribe() 中没有接收一个 Subscriber 对象，则会在内部 on_next 中 迭代调用 observer.on_next，即 for x in iterable
        - 如果 subscribe() 接收一个 Subscriber 对象，则 on_next 接收到的 value 则是一个可迭代对象

- from_list: 其内部也是生成 FromIteratorObservable() 或者 FromSingleElementFlowable()

"""
import time
from threading import Thread

import rxbp
from rxbp.acknowledgement.acksubject import AckSubject
from rxbp.acknowledgement.continueack import continue_ack
from rxbp.observer import Observer
from rxbp.schedulers.threadpoolscheduler import ThreadPoolScheduler
from rxbp.testing.tobserver import TObserver


def just():
    shoot = rxbp.just('Hello')
    shoot.subscribe(
        on_next=lambda v: print('Received: {}'.format(v)),
        on_completed=lambda: print('Done!')
    )


class TASubscribe(Observer):
    def __init__(self):
        self.ack = None

    def on_next(self, val):
        """
        :return: 如果返回 AckSubject 则会向 Observable 反压，即不会再发送数据
        """
        for v in val:
            print('val: ', v)
        return continue_ack

    def on_completed(self):
        print('Done!')

    def on_error(self, exc):
        print('Exception: ', exc)


class TBSubscribe(Observer):
    def on_next(self, val):
        """
        :return: 如果返回 AckSubject 则会向 Observable 反压，即不会再发送数据
        """
        if val == [8]:
            return AckSubject()

        print("Received: ", val)
        return continue_ack

    def on_completed(self):
        print('Done!')

    def on_error(self, exc):
        print('Exception: ', exc)


def from_range():
    # rxbp.from_range(100000, batch_size=1).pipe(
    #     # rxbp.op.filter(lambda i: i > 990),
    #     rxbp.op.last()
    # ).subscribe(print)

    # rxbp.from_range(100000).subscribe(print)

    def closer(subscription):
        subscription.dispose()
        print("dispose...")

    sink = TASubscribe()
    publisher = rxbp.from_range(1_000_000, batch_size=1)
    # publisher = publisher.pipe(
    #     rxbp.op.subscribe_on(ThreadPoolScheduler("publisher")),
    # )
    # subscription = publisher.subscribe(observer=TASubscribe(), subscribe_scheduler=ThreadPoolScheduler("publisher"))
    subscription = publisher.subscribe(observer=sink)

    t2 = Thread(target=closer, args=(subscription,))
    t2.start()
    t2.join()

    # sink.ack.on_next(continue_ack)

    time.sleep(1000)


if __name__ == '__main__':
    # just()

    from_range()
