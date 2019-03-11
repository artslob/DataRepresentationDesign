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


def test_update(table):
    assert len(table.rows) == 2
    table.update(dict(name='Test'))
    assert table.rows == [dict(id=1, name='Test', age=35.5), dict(id=2, name='Test', age=25.)]
    assert table.select(['name']) == [['Test'], ['Test']]
    table.update(dict(id=1000), table.fields['id'] == 1)
    assert table.select(['id']) == [[1000], [2]]
