"""
生产者：Observable 即可观察对象
消费者：Observer 即观察者

RxPy 没有 blocking
    - 将发出的数据最终转换为 list, dict, iterable, set...

"""

import rx
from rx import operators as op


def block():
    source = rx.timer(0.5, 1).pipe(
        op.take(3),
        # op.to_list()
        # op.to_dict(lambda v: v*2, lambda v: v*4)
        # op.to_iterable()
        op.to_set()
    )
    source.subscribe(
        on_next=lambda v: print('Received: {}'.format(v)),
        on_completed=lambda: print('Done!')
    )

    source.run()


if __name__ == '__main__':
    block()
