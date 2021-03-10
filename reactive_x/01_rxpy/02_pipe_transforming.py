"""

操作符使用

"""


import rx
import operator
from rx import operators as ops


# 组合, 映射
def ops_zip_map():
    b = rx.of(2, 2, 4, 4)

    source.pipe(
        ops.zip(b),  # returns a tuple with the items of a and b
        ops.map(lambda z: operator.mul(z[0], z[1]))
    ).subscribe(print)

    source.pipe(
        ops.zip(b),
        ops.starmap(operator.mul)
    ).subscribe(print)


# 合并
def ops_merge():
    obs1 = rx.from_([1, 2, 3, 4])
    obs2 = rx.from_([5, 6, 7, 8])

    res = rx.merge(obs1, obs2)
    res.subscribe(print)


# 缓冲池，在一个时间段中一起发送缓冲池的数据
def ops_buffer():
    source.pipe(
        ops.buffer(rx.interval(0.000001))
    ).subscribe(print)

    source.pipe(
        ops.buffer_when(lambda: rx.timer(0.5))
    ).subscribe(print)


# 映射
def ops_flat_map():
    # 将一个源序列映射到另一个源序列，并将结果合并为一个 observable
    source.pipe(
        ops.flat_map(lambda v: rx.range(0, v))
    ).subscribe(print)


# 按每个元素分组
def ops_group():
    rx.of(1, 2, 2, 3, 3).pipe(
        ops.group_by(lambda x: x),
    ).subscribe(print)


# 最大值
def ops_max():
    rx.of(1, 2, 5, 6, 3).pipe(
        ops.max(),
    ).subscribe(print)


# 扫描
def ops_scan():
    # 每次打印都计算前面元素的和
    rx.of(1, 2, 5, 6, 3).pipe(
        ops.scan(lambda acc, x: acc + x),
        ops.sequence_equal(rx.from_list([1, 3, 8, 14, 17]))
    ).subscribe(print)


# 共享, 阻塞其他订阅者
def ops_share():
    s = source.pipe(
        ops.share()
    )

    s.subscribe(print)
    s.subscribe(print)


# 获取单个
def ops_single():
    source.pipe(
        ops.single(lambda x: x == 4)
    ).subscribe(print)


def ops_replay():
    s = source.pipe(
        ops.retry(4)
        # ops.replay(lambda x: x, buffer_size=20, window=20)
    )
    s.subscribe(print)


def ops_take():
    source.pipe(
        ops.take(3)
    ).subscribe(print)


if __name__ == '__main__':
    source = rx.of(1, 2, 3, 4)

    ops_buffer()

    # ops_flat_map()

    # ops_group()

    # ops_max()

    # ops_scan()

    # ops_share()

    # ops_single()

    # ops_replay()

    # ops_take()
