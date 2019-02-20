from typing import NamedTuple, Type

from lab1.types import FieldType


class Column(NamedTuple):
    """
    Should be used as argument when creating tables.
    """
    name: str
    type: Type[FieldType]


class Field(NamedTuple):
    """
    Inner representation of field used by table. Not public API.
    """
    index: int
    name: str
    type: Type[FieldType]


# TODO: create custom exceptions for table operations
class Table:
    def __init__(self, columns):
        self.fields = {}
        self.index_to_name = []

        if not len(columns):
            raise ValueError('empty list of columns')

        for i, column in enumerate(columns):
            if not isinstance(column, Column):
                raise ValueError(f'{column!r} is not column')
            if column.type is FieldType or type(column.type) != type or not issubclass(column.type, FieldType):
                raise ValueError('type should be subclass of base field type')

            field = Field(index=i, name=column.name, type=column.type)
            if field.name in self.fields:
                raise ValueError(f'name {field.name!r} already exist')

            self.fields[field.name] = field
            self.index_to_name.append(field)

        self.index_to_name = tuple(self.index_to_name)
