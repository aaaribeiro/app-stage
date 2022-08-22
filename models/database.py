##### piece of code to connect postgres database on heroku cloud #####
# import os
# DATABASE_URL = os.environ['DATABASE_URL']
# if DATABASE_URL.startswith("postgres://"):
#     DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
#######################################################################

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# local database
DATABASE_URL = "postgresql+psycopg2://postgres_dw:!Netcondwproject$#2022!@tstage-dw-project.c1n70u3mmeqb.us-east-1.rds.amazonaws.com:5432/stage-dw-project"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()