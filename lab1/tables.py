from typing import NamedTuple, Type

from lab1.exceptions import TableCreationError
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


class Table:
    def __init__(self, columns):
        self.rows = []
        self.fields = {}
        self.index_to_name = []

        if not len(columns):
            raise TableCreationError('empty list of columns')

        for i, column in enumerate(columns):
            if not isinstance(column, Column):
                raise TableCreationError(f'{column!r} is not column')
            if not isinstance(column.name, str):
                raise TableCreationError(f'column name should be string: {column.name!r}')
            if column.type is FieldType or type(column.type) != type or not issubclass(column.type, FieldType):
                raise TableCreationError('type should be subclass of base field type')

            field = Field(index=i, name=column.name, type=column.type)
            if field.name in self.fields:
                raise TableCreationError(f'name {field.name!r} already exist')

            self.fields[field.name] = field
            self.index_to_name.append(field)

        self.index_to_name = tuple(self.index_to_name)

    def insert(self, values: dict):
        """
        :param values: dict that contains names of fields as keys and values for fields as values.
        example: dict(id=12, name='John Williams')
        """
        if not isinstance(values, dict):
            raise ValueError('values should be dictionary')

        if len(values) != len(self.fields):
            raise ValueError('number of values in insert is not equal to fields of the table')

        if not all(field.name in values and field.type.is_valid(values[field.name]) for field in self.fields.values()):
            raise ValueError()

        for field in self.fields.values():
            if field.name not in values:
                raise ValueError('missing field name')

            if not field.type.is_valid(values[field.name]):
                raise ValueError('invalid value for field')

        # TODO: copy dict
        self.rows.append(values)
