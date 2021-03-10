"""

操作符 op:


"""
import rxbp
from rxbp.acknowledgement.continueack import continue_ack
from rxbp.observer import Observer


class TSubscribe(Observer):
    def on_next(self, val):
        """
        :param val: generator()
        :return: ack
        """
        for v in val:
            print("Received: ", v)
        return continue_ack

    def on_completed(self):
        print('Done!')

    def on_error(self, exc):
        print('Exception: ', exc)


def op_filter():
    # batch_size 批量
    source = rxbp.from_list([2, 4, 6, 8, 10], batch_size=1)

    source.pipe(
        rxbp.op.filter(lambda v: v > 5),
    ).subscribe(observer=TSubscribe())


if __name__ == '__main__':
    op_filter()
