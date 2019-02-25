from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
import sys

DB_SETTING = 'sqlite:///memo.db'

engine = create_engine(DB_SETTING)

Session = sessionmaker(bind=engine)

def init_db():
    import Models
    import ModelServices

@contextmanager
def session_scope(session=None):

    if session:
        yield session
    else:
        session = Session()
        try:
            yield session
            session.commit()
        except BaseException as e:
            session.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            while exc_tb.tb_next:
                exc_tb = exc_tb.tb_next
            print(exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno, e)
            raise
        finally:
            session.close()

Base = declarative_base()