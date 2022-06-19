from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from config.settings import Settings

SQLALCHEMY_DATABASE_URL = Settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)