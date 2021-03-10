import time
from threading import Thread

import rx
import rxbp
from rxbp.schedulers.timeoutscheduler import TimeoutScheduler
from rxbp.testing.tobserver import TObserver


# 必须指定 scheduler
def from_rx_interval():
    # from_rx 将 Observable 转为 FromRxBufferingFlowable， 其中使用到了 BufferObserver, 不适用与 request_n
    # prev_meas_state = self.state.get_measured_state(bool(len_queue))
    # 当 queue 的长度为 0 时，即使有背压也会被认为是 WaitingState，继续发送数据
    interval = rxbp.from_rx(rx.interval(1))
    sink = TObserver(immediate_continue=5)
    interval.subscribe(observer=sink, subscribe_scheduler=TimeoutScheduler())

    def counter(sink):
        while True:
            time.sleep(1)
            print(f"immediate: {sink.immediate_continue}, received: ", sink.received)

    t1 = Thread(target=counter, args=(sink,))
    t1.start()
    time.sleep(100)
