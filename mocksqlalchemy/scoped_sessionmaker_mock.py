__author__ = 'Andy'

from sqlalchemy.orm.session import Session


class ScopedSessionmakerMock(object):
    def __init__(self, *args, bind=None, **kwargs):
        self.engine = bind
        self.args = args
        self.kwargs = kwargs
        self.connection = None
        self.transaction = None
        self.nested_transaction = None

    def __call__(self):
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        self.nested_transaction = self.connection.begin_nested()
        return Session(self.connection)

    def __del__(self):
        if self.nested_transaction is not None:
            self.nested_transaction.rollback()
        if self.connection is not None:
            self.connection.close()

