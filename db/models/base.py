from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import select
from db.connection import session

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

    def validate_unique(
        self,
        field_name,
        value,
        message = "The '{field}' of '{value}' is aready in use."
    ):
        if not value:
            return value
        pk_column=inspect(self.__class__).primary_key[0]
        self_pk=inspect(self).identity
        query = select(self.__class__).where(
            getattr(self.__class__, field_name) == value
        ).where(
            pk_column != self_pk
        )
        result = session.execute(query).scalars().first()
        if result:
            raise ValueError(message.format(field = field_name, value = value))
        return value

    def validate_exists(
        self,
        field_name,
        value,
        message = "The '{field}' of '{value}' does not exist.",
        other_class = None,
        other_field = None
    ):
        if not value:
            return value
        select_class = other_class if other_class else self.__class__
        select_field = other_field if other_field else getattr(self.__class__, field_name)
        query = select(select_class).where(select_field == value)
        result = session.execute(query).scalars().first()
        if not result:
            raise ValueError(message.format(field = field_name, value = value))
        return value
