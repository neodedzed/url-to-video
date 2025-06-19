from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL='sqlite:///products.db'

engine = create_engine(url=DATABASE_URL)

session = sessionmaker(
    bind=engine,
)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    except Exception as e:
        print(f"Error while creating DB Session: {e}") 
    finally:
        db.close()