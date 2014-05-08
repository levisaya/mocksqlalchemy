import unittest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from mocksqlalchemy import ScopedSessionmakerMock
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class TestScopedSessionMock(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql://postgres:postgresroot@127.0.0.1:5432/test')
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)()
        session.query(User).delete()
        session.commit()
        session.close()

    def tearDown(self):
        pass

    def test_rollback(self):
        sm = ScopedSessionmakerMock(bind=self.engine)
        session = sm()
        session.add(User(name='derp'))
        session.commit()
        results = session.query(User)
        self.assertEqual(results.count(), 1)
        session.close()

        real_session = sessionmaker(bind=self.engine)()
        results = real_session.query(User)
        self.assertEqual(results.count(), 0)



if __name__ == '__main__':
    unittest.main()