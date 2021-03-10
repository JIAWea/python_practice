"""
生产者：Observable 即可观察对象
消费者：Observer 即观察者

操作符：
op.publish:
    - 使用了 publish 操作符后会将生产者变为 connectable
        - connectable 也是一个发布者，但是它一开始不会发送数据，即使有订阅者订阅，只有调用了 connect() 后才会发送所有数据
            可以控制何时发送数据的
        - 支持多播，其底层使用了 multicast 操作符
"""

import rx
from rx import operators as op


def op_connectable():
    # 可以消费
    unshared = rx.range(1, 4)
    unshared.subscribe(
        on_next=lambda value: print('base received-0: {}'.format(value))
    )

    # connectable 调用 connect 后才会消费
    # 支持可以多播
    # 实现机制：返回一个多播嵌套Subject()
    share = unshared.pipe(
        op.publish()
    )
    share.subscribe(
        on_next=lambda value: print('Connect received-1: {}'.format(value))
    )
    share.subscribe(
        on_next=lambda value: print('Connect received-2: {}'.format(value))
    )

    share.connect()


# publisher 可以运用于 RSocket-py
def create_and_publish():
    publisher = rx.defer(lambda _: rx.of(1, 3, 5, 8, 10)).pipe(
        op.publish()
    )
    publisher.connect()

    subscription = publisher.subscribe(
        on_next=lambda value: print('Connect received-1: {}'.format(value)),
        on_completed=lambda: print("Done!")
    )
    subscription.dispose()


if __name__ == '__main__':
    # op_connectable()

    create_and_publish()
