from datetime import datetime

import pytest

from lab1.exceptions import TableInsertError
from lab1.tables import Table, Column
from lab1.types import IntType, StringType, FloatType, DatetimeType, BinaryType


def test_insert():
    table = Table(columns=(Column('id', IntType), Column('name', StringType), Column('weight', FloatType),))
    assert len(table.rows) == 0
    first_arg = dict(id=1, name='John', weight=70.)
    second_arg = dict(id=2, name='Steven', weight=75.)
    table.insert(first_arg)
    table.insert(second_arg)
    assert len(table.rows) == 2
    assert table.rows[0] == first_arg
    assert table.rows[1] == second_arg


def test_insert_mutability():
    table = Table(columns=(Column('id', IntType),))
    value = dict(id=3)
    table.insert(value)
    assert table.rows[0] == value
    value['id'] = 5
    value['name'] = 'Test name'
    assert table.rows[0]['id'] == 3
    assert 'name' not in table.rows[0]
    assert len(table.rows) == 1


@pytest.mark.parametrize('value', [dict, str, list, 12, 'string', tuple(), []])
def test_insert_not_dict(value):
    table = Table(columns=(Column('id', IntType),))
    with pytest.raises(TableInsertError, match='should be dictionary'):
        # noinspection PyTypeChecker
        table.insert(value)


@pytest.mark.parametrize('value', [{}, dict(id=2), dict(id=2, name=3, weight=7.)])
def test_insert_wrong_number_of_args(value):
    table = Table(columns=(Column('id', IntType), Column('name', StringType),))
    with pytest.raises(TableInsertError, match='number .* not equal to'):
        table.insert(value)


def test_insert_missing_field_name():
    table = Table(columns=(Column('id', IntType), Column('name', StringType),))
    with pytest.raises(TableInsertError, match='missing field name'):
        table.insert(dict(id=1, test='str'))


@pytest.mark.parametrize('value', [7.0, datetime(2019, 1, 2), 'str', b'bytes'])
def test_insert_wrong_type_int(value):
    table = Table(columns=(Column('id', IntType),))
    with pytest.raises(TableInsertError, match='invalid value for field'):
        table.insert(dict(id=value))


@pytest.mark.parametrize('value', [42, datetime(2019, 1, 2), 'str', b'bytes'])
def test_insert_wrong_type_float(value):
    table = Table(columns=(Column('temperature', FloatType),))
    with pytest.raises(TableInsertError, match='invalid value for field'):
        table.insert(dict(temperature=value))


@pytest.mark.parametrize('value', [42, 42.0, 'str', b'bytes'])
def test_insert_wrong_type_datetime(value):
    table = Table(columns=(Column('birthday', DatetimeType),))
    with pytest.raises(TableInsertError, match='invalid value for field'):
        table.insert(dict(birthday=value))


@pytest.mark.parametrize('value', [42, 7.0, datetime(2019, 1, 2), b'bytes'])
def test_insert_wrong_type_str(value):
    table = Table(columns=(Column('name', StringType),))
    with pytest.raises(TableInsertError, match='invalid value for field'):
        table.insert(dict(name=value))


@pytest.mark.parametrize('value', [42, 7.0, datetime(2019, 1, 2), 'str'])
def test_insert_wrong_type_binary(value):
    table = Table(columns=(Column('file', BinaryType),))
    with pytest.raises(TableInsertError, match='invalid value for field'):
        table.insert(dict(file=value))
