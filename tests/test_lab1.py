from lab1.tables import Table, Column
from lab1.types import IntType, StringType, FloatType


def test_table_creation():
    table = Table(columns=(Column('id', IntType), Column('name', StringType), Column('weight', FloatType),))
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
