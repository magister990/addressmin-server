#from functools import classmethod
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class BaseBase:
    __name__: str

    @declared_attr
    def __tablename__(model) -> str:
        return model.__name__.lower()

class Base(BaseBase):
    __abstract__ = True

    @classmethod
    def get_column_names(model) -> [str]:
        return [p.key for p in model.__table__.columns]

    def to_dict(self):
        columns = self.get_column_names()
        result = {}
        for col in columns:
            result[col]=getattr(self, col)
        return result
