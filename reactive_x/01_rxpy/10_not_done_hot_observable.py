import sys
import time
from typing import Any, List

from rx.core import Observable, typing
from rx.disposable import Disposable
from rx.internal.basic import default_comparer
from rx.scheduler import CurrentThreadScheduler, VirtualTimeScheduler
from rx.scheduler.scheduler import Scheduler


class Subscription(object):
    def __init__(self, start, end=None):
        self.subscribe = start
        self.unsubscribe = end or sys.maxsize

    def equals(self, other):
        return self.subscribe == other.subscribe and self.unsubscribe == other.unsubscribe

    def __eq__(self, other):
        return self.equals(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        unsubscribe = "Infinite" if self.unsubscribe == sys.maxsize else self.unsubscribe
        return "(%s, %s)" % (self.subscribe, unsubscribe)


class Recorded:
    def __init__(self, time: int, value: Any, comparer=None):
        self.time = time
        self.value = value
        self.comparer = comparer or default_comparer

    def __eq__(self, other):
        """Returns true if a recorded value matches another recorded value"""

        time_match = self.time == other.time
        return time_match and self.comparer(self.value, other.value)

    equals = __eq__

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "%s@%s" % (self.value, self.time)


# class HotObservable(Observable):
#     def __init__(self, messages: List[Recorded], scheduler: Scheduler = None) -> None:
#         super().__init__()
#
#         self.scheduler: Scheduler = scheduler or CurrentThreadScheduler.singleton()
#         self.messages = messages
#         self.subscriptions: List[Subscription] = []
#         self.observers: List[typing.Observer] = []
#
#     def _work(self):
#         parent = self
#
#         def get_action(notification):
#             def action(scheduler, state):
#                 for observer in parent.observers[:]:
#                     observer.on_next(notification)
#                 return Disposable()
#
#             return action
#
#         while self.messages:
#             message = self.messages.pop(0)
#             notification = message.value
#
#             # Warning: Don't make closures within a loop
#             action = get_action(notification)
#             self.scheduler.schedule(action)
#
#     def _subscribe_core(self, observer=None, scheduler=None) -> typing.Disposable:
#         self.observers.append(observer)
#
#         self._work()
#
#         def dispose_action():
#             self.observers.remove(observer)
#             # start = self.subscriptions[index].subscribe
#             # end = self.scheduler.clock
#             # self.subscriptions[index] = Subscription(start, end)
#
#         return Disposable(dispose_action)

class HotObservable(Observable):
    def __init__(self, messages: List[Recorded], scheduler: Scheduler = None) -> None:
        super().__init__()

        self.scheduler = scheduler or CurrentThreadScheduler.singleton()
        self.messages = messages
        self.subscriptions: List[Subscription] = []
        self.observers: List[typing.Observer] = []

        out_self = self

        def get_action(notification):
            def action(scheduler, state):
                for observer in out_self.observers[:]:
                    # notification.accept(observer)
                    observer.on_next("received: ", notification)
                return Disposable()
            return action

        for message in self.messages:
            notification = message.value

            # Warning: Don't make closures within a loop
            action = get_action(notification)
            self.scheduler.schedule(action)

    def _subscribe_core(self, observer=None, scheduler=None) -> typing.Disposable:
        self.observers.append(observer)
        # self.subscriptions.append(Subscription(self.scheduler.clock))
        # index = len(self.subscriptions) - 1

        def dispose_action():
            self.observers.remove(observer)
            # start = self.subscriptions[index].subscribe
            # end = self.scheduler.clock
            # self.subscriptions[index] = Subscription(start, end)

        return Disposable(dispose_action)


if __name__ == '__main__':
    import time
    hot = HotObservable([Recorded(i, i) for i in range(int(1e6))])

    hot.subscribe(
        on_next=lambda v: print('received: {}'.format(v))
    )

    time.sleep(1)

