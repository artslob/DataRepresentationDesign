import copy
from typing import NamedTuple, Type

import lab1.conditions as conditions
from lab1.exceptions import TableCreationError, TableInsertError, ConditionError, TableSelectError
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

    def __lt__(self, other):
        self.check_operands(other)
        return conditions.BinaryCondition(self, '<', other)

    def __le__(self, other):
        self.check_operands(other)
        return conditions.BinaryCondition(self, '<=', other)

    def __eq__(self, other):
        self.check_operands(other)
        return conditions.BinaryCondition(self, '==', other)

    def __ne__(self, other):
        self.check_operands(other)
        return conditions.BinaryCondition(self, '!=', other)

    def __gt__(self, other):
        self.check_operands(other)
        return conditions.BinaryCondition(self, '>', other)

    def __ge__(self, other):
        self.check_operands(other)
        return conditions.BinaryCondition(self, '>=', other)

    def check_operands(self, other):
        if not self.type.is_valid(other) and not isinstance(other, Field):
            raise ConditionError(f'cannot compare {self!r} and {other!r}: different types')

        if isinstance(other, Field) and self.type != other.type:
            raise ConditionError(f'cannot compare {self!r} and {other!r}: different types')


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
                raise TableCreationError(f'type should be subclass of base field type: {column.type!r}')

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
            raise TableInsertError('values should be dictionary')

        if len(values) != len(self.fields):
            raise TableInsertError('number of values in insert is not equal to fields of the table')

        for field in self.fields.values():
            if field.name not in values:
                raise TableInsertError(f'missing field name: {field.name!r}')

            value = values[field.name]
            if not field.type.is_valid(value):
                raise TableInsertError(f'invalid value for field: {value!r}')

        self.rows.append(copy.deepcopy(values))

    def select(self, fields, condition: conditions.Condition = None):
        for field in fields:
            if field not in self.fields:
                raise TableSelectError(f'field name {field!r} not exist in table {self!r}')

        result = []
        for row in self.rows:
            if condition and not condition.evaluate(self, row):
                continue

            result.append([row[field] for field in fields])

        return result
