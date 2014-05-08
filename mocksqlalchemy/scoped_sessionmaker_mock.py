from sqlalchemy.orm.session import Session


class ScopedSessionmakerMock(object):
    def __init__(self, *args, **kwargs):
        self.engine = kwargs['bind']
        self.args = args
        self.kwargs = {k: v for k, v in kwargs.items() if k != 'bind'}
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        self.nested_transaction = None

    def __call__(self):
        self.nested_transaction = self.connection.begin_nested()
        return Session(self.connection, *self.args, **self.kwargs)

    def __del__(self):
        if self.nested_transaction is not None:
            self.nested_transaction.rollback()
        self.connection.close()
        self.transaction.rollback()
        self.engine.dispose()

