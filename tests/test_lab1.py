import pytest

from lab1.exceptions import TableCreationError
from lab1.tables import Table, Column
from lab1.types import IntType, StringType, FloatType


def test_table_creation():
    table = Table(columns=(Column('id', IntType), Column('name', StringType), Column('weight', FloatType),))
    assert len(table.fields) == 3
    assert table.fields['id'].index == 0
    assert table.fields['id'].name == 'id'
    assert table.fields['id'].type == IntType
    assert table.fields['name'].index == 1
    assert table.fields['name'].name == 'name'
    assert table.fields['name'].type == StringType
    assert table.fields['weight'].index == 2
    assert table.fields['weight'].name == 'weight'
    assert table.fields['weight'].type == FloatType
    assert [i.name for i in table.index_to_name] == ['id', 'name', 'weight']


def test_create_empty_table():
    with pytest.raises(TableCreationError, match='empty'):
        Table(columns=[])


@pytest.mark.parametrize('wrong_value,expected_exc', [
    [Column, 'not column'],
    [int, 'not column'],
    [1, 'not column'],
    ['test', 'not column'],
    [('id', 123), 'not column'],
    [Column('id', IntType()), 'type should be subclass'],
    [Column('id', int), 'type should be subclass'],
    [Column(123, IntType), 'name should be string'],
])
def test_create_table_with_wrong_column_type(wrong_value, expected_exc):
    with pytest.raises(TableCreationError, match=expected_exc):
        Table(columns=[wrong_value])

    with pytest.raises(TableCreationError, match=expected_exc):
        Table(columns=[Column('name', StringType), wrong_value])


def test_create_table_duplicate_fields():
    with pytest.raises(TableCreationError, match='already exist'):
        Table(columns=[Column('id', IntType), Column('name', StringType), Column('id', FloatType)])
