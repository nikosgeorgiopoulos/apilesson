from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time



#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-adress/hostname>/<database_name>'


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine )

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# for connecting with raw sql with the postgres driver psycopg2
#  while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', port='5433', database='fastapi', 
#                                 user='postgres', password= 'Ea.palini.2007', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print ("Database connection was succesful.")
#         break
#     except Exception as error:
#         print ("Connection to batabasse failed.")
#         print ("Error:", error)
#         time.sleep(2)
