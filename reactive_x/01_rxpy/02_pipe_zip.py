import rx
from rx import operators as op


def op_zip():
    source = rx.range(1, 10)
    source.pipe(
        op.zip(
            source,
            source.pipe(op.skip(1)),
            source.pipe(op.skip(2)),
        )
    ).subscribe(
        on_next=lambda v: print('Received: {}'.format(v))
    )


if __name__ == '__main__':
    op_zip()
