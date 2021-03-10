"""
生产者：Observable 即可观察对象
消费者：Observer 即观察者

基础使用：of, range, from

- range: 内部一直通过 scheduler 迭代调度 action() --> next(gen)，直到迭代器发生 StopIteration

- from_iterable:
    - 与 range 不同的是，range 是不断地迭代调用 action()，action 中调用 next()
    - from_iterable 是调用一次 action()，action 中一次性迭代 “可迭代对象”，使用 for x in iterable

- from_, from_list: 底层都是调用 from_iterable

"""

import rx
from rx import operators as op


def func1():
    # op.share 影响第二次订阅
    o = rx.range(4).pipe(
        op.share(),
        op.subscribe_on()
    )

    o.subscribe(print)
    o.subscribe(print)  # the second time no elements are sent


# 通过 scheduler 迭代执行 action
def base_of():
    source = rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")
    source.pipe(
        op.map(lambda s: len(s)),
        op.filter(lambda i: i >= 5)
    ).subscribe(
        lambda value: print("Received {0}".format(value)),
        lambda e: print("Error: {0}".format(e)),
        lambda: print("Done!")
    )


def lowercase():
    def _lowercase(source):
        def subscribe(observer, scheduler=None):
            def on_next(value):
                observer.on_next(value.lower())

            return source.subscribe(
                on_next,
                observer.on_error,
                observer.on_completed,
                scheduler)

        return rx.create(subscribe)

    return _lowercase


def lowercase_func():
    rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon").pipe(
        lowercase()
    ).subscribe(
        lambda value: print("Received {0}".format(value)),
        lambda e: print("Error {0}".format(e)),
        lambda: print("Done"),
    )


# 根据时间段合并
def op_merge():
    xs = rx.range(1, 5).pipe()
    ys = rx.from_("abcde")  # [a, b, c, d, e]
    xs.pipe(
        op.merge(ys)
    ).subscribe(print)


# from_ 与 from_list 与 from_iterable 都一样，底层都是调用 from_iterable
def from_():
    rx.from_(range(1, 6)).subscribe(print)

    rx.from_iterable(range(1, 6)).subscribe(print)

    rx.from_list([1, 2, 3, 4, 5]).subscribe(print)


def rx_range():
    rx.range(10).subscribe(print)


if __name__ == '__main__':
    # func1()

    # base_of()

    # lowercase_func()

    # op_merge()

    from_()

    # rx_range()
