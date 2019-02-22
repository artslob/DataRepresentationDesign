from lab1.tables import Table, Column
from lab1.types import IntType, StringType, FloatType


def test_select():
    table = Table(columns=(Column('id', IntType), Column('name', StringType), Column('age', FloatType),))
    table.insert(dict(id=1, name='George', age=35.5))
    table.insert(dict(id=2, name='Fred', age=25.))
    assert len(table.rows) == 2
    assert table.select(['id'], ) == [[1], [2]]
    assert table.select(['id', 'age'], table.fields['age'] > 30.) == [[1, 35.5]]
    assert table.select(['name'], table.fields['name'] > 'G') == [['George']]
    assert table.select(['id'], table.fields['id'] >= 2) == [[2]]
    assert table.select(['id'], 2 <= table.fields['id']) == [[2]]
    assert table.select(['id'], 0 < table.fields['id']) == [[1], [2]]
    assert table.select(['id'], (0 < table.fields['id']) & (table.fields['id'] < 2)) == [[1]]
