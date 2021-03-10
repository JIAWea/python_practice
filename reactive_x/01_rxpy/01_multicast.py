"""
生产者：Observable 即可观察对象
消费者：Observer 即观察者

操作符：
op.multicast:
    - 接受一个 Subject() 对象，将所有的 消费者 维护到一个 observers 列表，在调用 on_next 时一起发送数据
    - 使用了 multicast 操作符后会将生产者变为 connectable
        - connectable 是一个发布者，但是它一开始不会发送数据，即使有订阅者订阅，只有调用了 connect() 后才会发送所有数据
            可以控制何时发送数据的

"""

import rx
from rx import operators as op
from rx.subject import Subject


def multicast():
    source = rx.of(1, 2, 3, 4, 5).pipe(
        op.multicast(subject=Subject())
    )

    source.subscribe(
        on_next=lambda v: print('Subscriber-1: received %s' % v),
        on_completed=lambda: print('Subscriber-1: Done')
    )
    source.subscribe(
        on_next=lambda v: print('Subscriber-2: received %s' % v),
        on_completed=lambda: print('Subscriber-2: Done')
    )

    source.connect()


if __name__ == '__main__':
    multicast()
