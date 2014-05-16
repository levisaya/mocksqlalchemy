from sqlalchemy.orm.session import Session


class ScopedSessionmakerMock(object):
    def __init__(self, *args, **kwargs):
        self.engine = kwargs['bind']
        self.args = args
        self.kwargs = {k: v for k, v in kwargs.items() if k != 'bind'}
        self.nested_transaction = None
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()

    def __call__(self, **kwargs):
        self.nested_transaction = self.connection.begin_nested()
        self.kwargs.update(kwargs)
        return Session(self.connection, *self.args, **self.kwargs)

    def __del__(self):
        if self.nested_transaction is not None:
            self.nested_transaction.rollback()
        self.connection.close()
        self.transaction.rollback()
        self.engine.dispose()

