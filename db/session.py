import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

pwd = os.path.dirname(os.path.abspath(__file__))
engine = create_engine("sqlite:///" + os.path.join(pwd, "db.sqlite"))
Base = declarative_base()
Session = sessionmaker(bind=engine)

