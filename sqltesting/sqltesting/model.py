# /// script
# dependencies = [
#   "sqlmodel"
# ]
# ///
import logging
from sqlalchemy.schema import CreateSchema
from sqlmodel import SQLModel, Field, create_engine, Session, select, text

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TestModel(SQLModel, table=True):
    __table_args__ = {'schema': 'per_user'}

    id: int | None = Field(default=None, primary_key=True)


if __name__ == '__main__':
    engine = create_engine('sqlite://', echo=True)
    with engine.connect() as connect:
        if connect.dialect.has_schema(connect, 'per_user'):
            connect.execute(CreateSchema('per_user'))
        else:
            connect.execute(text("ATTACH DATABASE ':memory:' AS  per_user"))
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([TestModel(), TestModel(), TestModel()])
        session.commit()

    with Session(engine) as session:
        data = session.exec(select(TestModel.id))
        log.info(f'collected ids: {data.all()}')