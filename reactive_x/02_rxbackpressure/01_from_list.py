import rxbp
from rxbp.acknowledgement.continueack import continue_ack
from rxbp.testing.tobserver import TObserver


def demo1():
    # batch_size 批量
    publisher = rxbp.from_list([2, 4, 6, 8, 10, 12, 14, 16, 18, 20], batch_size=1)
    sink = TObserver(immediate_continue=5)
    # publisher.subscribe(observer=sink, subscribe_scheduler=ThreadPoolScheduler("publisher"))
    publisher.subscribe(observer=sink)
    print("sink: ", sink.received)

    if sink.immediate_continue > 0 and sink.ack:
        sink.ack.on_next(continue_ack)

    print("sink: ", sink.received)

    sink.immediate_continue = 3
    if sink.immediate_continue > 0 and sink.ack:
        sink.ack.on_next(continue_ack)

    print("sink: ", sink.received)


def demo2():
    publisher = rxbp.from_list([2, 4, 6, 8, 10, 12, 14, 16, 18, 20], batch_size=1)
    sink = TObserver(immediate_continue=2)
    publisher.subscribe(observer=sink)
    assert sink.received == [2, 4, 6]

    sink.immediate_continue = 3
    if sink.immediate_continue > 0 and sink.ack:
        sink.ack.on_next(continue_ack)
    assert sink.received == [2, 4, 6, 8, 10, 12, 14]

    sink.immediate_continue = 2
    if sink.immediate_continue > 0 and sink.ack:
        sink.ack.on_next(continue_ack)
    assert sink.received == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]


if __name__ == '__main__':
    demo1()

    demo2()
