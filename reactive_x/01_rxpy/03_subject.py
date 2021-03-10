"""
生产者：Observable 即可观察对象
消费者：Observer 即观察者

Subject()

Subject 可以看成是一个代理，可以充当生产者和消费者。
- 因为它是观察者，所以可以订阅消费一个或多个生产者；
- 因为它是被观察者，所以可以发布数据到所以的消费者；

"""

from rx.subject import Subject, ReplaySubject, BehaviorSubject, AsyncSubject


# 即使没有订阅者也可以发布数据，但是不会被接收到
# 订阅只能接受后面的数据
# 支持多播
def subject():
    subject = Subject()

    for i in range(40, 45):
        subject.on_next(i)

    d1 = subject.subscribe(
        on_next=lambda x: print("subscriber-1 got: %s" % x),
        on_completed=lambda: print("completed!"))

    d2 = subject.subscribe(
        on_next=lambda x: print("subscriber-2 got: %s" % x),
        on_completed=lambda: print("subscriber-2 completed!"))

    for i in range(50, 52):
        subject.on_next(i)

    d1.dispose()

    for i in range(52, 55):
        subject.on_next(i)

    subject.on_completed()


# 缓存数据，并会重新推送缓存的数据
def replay_subject():
    # replay = ReplaySubject(buffer_size=2)
    replay = ReplaySubject()

    replay.on_next(1)
    replay.on_next(2)
    replay.on_next(3)

    replay.on_completed()
    replay.subscribe(
        on_next=lambda x: print("subscriber-1 got: %s" % x),
        on_completed=lambda: print("completed!"))

    replay.dispose()

    try:
        replay.on_next(4)
    except Exception:
        print("has been disposed")


# 直接推送 100，如果发布其他数据，则 100 会被替换成最后一个发布的数据
def behavior_subject():
    behavior = BehaviorSubject(100)
    behavior.subscribe(
        on_next=lambda x: print("subscriber-1 got: %s" % x),
        on_completed=lambda: print("completed!"))
    behavior.on_next(200)
    behavior.on_next(300)

    # 300
    behavior.subscribe(
        on_next=lambda x: print("subscriber-2 got: %s" % x),
        on_completed=lambda: print("completed!"))
    behavior.on_completed()


# 缓存所有数据，直到 on_completed 被调用，则返回最后一个数据
def async_subject():
    ayn = AsyncSubject()
    ayn.on_next(100)
    ayn.on_next(200)

    # 500
    ayn.subscribe(
        on_next=lambda x: print("subscriber-1 got: %s" % x),
        on_completed=lambda: print("completed!"))

    ayn.on_next(400)
    ayn.on_next(500)

    # 500
    ayn.subscribe(
        on_next=lambda x: print("subscriber-2 got: %s" % x),
        on_completed=lambda: print("completed!"))

    ayn.on_completed()


if __name__ == '__main__':
    subject()

    # replay_subject()

    # behavior_subject()

    # async_subject()
