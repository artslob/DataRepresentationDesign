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
    with pytest.raises(TableCreationError):
        Table(columns=[])


@pytest.mark.parametrize('wrong_value',
                         [Column, int, 1, 'test', ('id', 123), Column('id', IntType()), Column('id', int)])
def test_create_table_with_wrong_column_type(wrong_value):
    with pytest.raises(TableCreationError):
        Table(columns=[wrong_value])

    with pytest.raises(TableCreationError):
        Table(columns=[Column('name', StringType), wrong_value])


def test_create_table_duplicate_fields():
    with pytest.raises(TableCreationError):
        Table(columns=[Column('id', IntType), Column('name', StringType), Column('id', FloatType)])
