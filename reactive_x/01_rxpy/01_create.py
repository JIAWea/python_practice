"""
生产者：Observable 即可观察者对象
消费者：Observer 即观察者

create: 一次性创建单一数据流，没有队列
defer: 工厂模式，接受一个函数，返回一个 Observable 或者 future。 Union[Observable, Future]

"""
import threading
import time

import rx
from rx.core import Observer
from rx.disposable import BooleanDisposable
from rx.scheduler import CurrentThreadScheduler, NewThreadScheduler
from rx.scheduler.eventloop import AsyncIOScheduler
from rx.scheduler.scheduler import Scheduler


class Subscriber(Observer):
    def on_next(self, value):
        print("value: {}, thread: {}".format(value, threading.current_thread().name))

    def on_completed(self) -> None:
        print("Done")

    def on_error(self, error: Exception) -> None:
        print("error: ", error)


def handler(observer, scheduler: Scheduler):
    for i in range(100):
        time.sleep(0.5)
        observer.on_next("index: {}".format(str(i)))
    observer.on_completed()

    # def action(_scheduler, states):
    #     for i in range(10):
    #         observer.on_next("index: " + str(i))
    #     observer.on_completed()
    #
    # return scheduler.schedule(action)


def rx_create(name):
    from rx import operators as op
    source = rx.create(handler).pipe(
        # op.do_action(on_next=lambda i: print("do_action, thread: {}".format(threading.current_thread().name))),
        # op.subscribe_on(NewThreadScheduler()),
    )

    # subscription = source.subscribe(
    #     on_next=lambda i: print("Received-{0}: {1}".format(name, i)),
    #     on_error=lambda e: print("Error Occurred: {0}".format(e)),
    #     on_completed=lambda: print("Done!"),
    #     scheduler=CurrentThreadScheduler.singleton()
    # )
    subscription = source.subscribe(Subscriber(), scheduler=NewThreadScheduler())
    time.sleep(3)
    subscription.dispose()
    print("dispose!")

    time.sleep(20)


def factory(states):
    # return rx.of(1, 3, 5, 7, 9)
    # return rx.return_value(10)
    return rx.range(5)


def rx_defer():
    defer = rx.defer(factory=factory)
    subscription = defer.subscribe(
        on_next=lambda i: print("Received {0}".format(i)),
        on_error=lambda e: print("Error Occurred: {0}".format(e)),
        on_completed=lambda: print("Done!"),
    )
    subscription.dispose()


if __name__ == '__main__':
    rx_create('Ray')

    # rx_defer()
