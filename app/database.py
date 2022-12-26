from sqlmodel import SQLModel, create_engine

url = f'postgresql://user:pass@localhost:5432/fastapi_dev'
engine = create_engine(url, echo=True)


def create_db_and_tables():
    print('Creating tables...')
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
