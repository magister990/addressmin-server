from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
