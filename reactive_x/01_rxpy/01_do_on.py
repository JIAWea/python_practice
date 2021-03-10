"""
生产者：Observable 即可观察对象
消费者：Observer 即观察者

操作符
op.do_xx, op.xx_action:
- 一般在 可观察对象 中使用，用于记录发送的数据，或者在发送特定的数据后执行某些操作，或者记录日志等

"""
import rx
from rx import operators as op


def do_on():
    source = rx.of(1, 3, 5, 7)
    source.pipe(
        op.do_action(on_next=lambda v: print('do_action_on_next: {}'.format(v))),
        op.finally_action(lambda: print('finally_action: Done!'))
    ).subscribe(
        on_next=lambda v: print('subscriber: got {}'.format(v)),
        on_completed=lambda: print('subscriber Done!')
    )


if __name__ == '__main__':
    do_on()
