from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://ojeleachwbmhjs:209bed0e76ee57c5f7fb93978fc0d9a0693e94ded6e38acedf50a703e05b8fe0@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/d3c6fpta682ap2"
#SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://ojeleachwbmhjs:209bed0e76ee57c5f7fb93978fc0d9a0693e94ded6e38acedf50a703e05b8fe0@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/d3c6fpta682ap2"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()