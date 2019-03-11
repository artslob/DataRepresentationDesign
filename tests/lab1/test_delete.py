import pytest

from lab1.tables import Table, Column
from lab1.types import IntType, StringType, FloatType


@pytest.fixture
def table_factory():
    def create_table():
        table = Table(columns=(Column('id', IntType), Column('name', StringType), Column('age', FloatType),))
        table.insert(dict(id=1, name='George', age=35.5))
        table.insert(dict(id=2, name='Fred', age=25.))
        return table

    return create_table


@pytest.fixture
def table(table_factory):
    return table_factory()


def test_delete(table):
    assert len(table.rows) == 2
    table.delete()
    assert len(table.rows) == 0
    table.delete()
    assert len(table.rows) == 0


def test_delete_condition(table):
    assert len(table.rows) == 2
    table.delete(table.fields['name'] == 'Fred')
    assert len(table.rows) == 1
    assert table.rows == [dict(id=1, name='George', age=35.5)]
