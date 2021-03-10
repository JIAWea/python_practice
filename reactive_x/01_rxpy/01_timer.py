"""

timer: 每隔一定的频率发出数据，通常会使用 map 将数据转换成想要发出的数据

"""

import rx
from rx import operators as op


def interval():
    # rx.of(1, 3, 5, 7).subscribe(
    #     on_next=lambda value: print('received: {}'.format(value)),
    #     on_completed=lambda: print('Done!')
    # )

    t = rx.interval(1).pipe(
        op.map(lambda v: 'new value'),
        # op.take(10)
    )
    t.subscribe(
        on_next=lambda value: print('received: {}'.format(value)),
        on_completed=lambda: print('Done!')
    )


def timer():
    t = rx.timer(0, 1)
    t.pipe(op.take(5)).subscribe(
        on_next=lambda value: print('received: {}'.format(value)),
        on_completed=lambda: print('Done!')
    )
    t.run()


if __name__ == '__main__':
    interval()

    # timer()
