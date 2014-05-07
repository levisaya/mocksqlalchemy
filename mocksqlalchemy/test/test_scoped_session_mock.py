import unittest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from unittest.mock import patch
from mocksqlalchemy import ScopedSessionmakerMock


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class TestScopedSessionMock(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql://postgres:postgresroot@127.0.0.1:5432/test')
        Base.metadata.create_all(self.engine)
        from sqlalchemy.orm import sessionmaker
        sm = sessionmaker(bind=self.engine)
        session = sm()
        session.query(User).delete()
        session.commit()
        session.close()

    def tearDown(self):
        from sqlalchemy.orm import sessionmaker
        sm = sessionmaker(bind=self.engine)
        session = sm()
        self.assertEqual(session.query(User).count(), 0)
        session.close()

    @patch('sqlalchemy.orm.sessionmaker', ScopedSessionmakerMock)
    def test_rollback(self):
        from sqlalchemy.orm import sessionmaker
        sm = sessionmaker(bind=self.engine)
        session = sm()
        session.add(User(name='derp'))
        session.commit()
        session.close()
