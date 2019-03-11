import pytest

from lab1.exceptions import ConditionError
from lab1.tables import Table, Column
from lab1.types import IntType, StringType, FloatType


@pytest.fixture
def table():
    table = Table(columns=(Column('id', IntType), Column('name', StringType), Column('age', FloatType),))
    table.insert(dict(id=1, name='George', age=35.5))
    table.insert(dict(id=2, name='Fred', age=25.))
    return table


def test_select(table):
    assert len(table.rows) == 2
    assert table.select(['id'], ) == [[1], [2]]
    assert table.select(['id', 'age'], table.fields['age'] > 30.) == [[1, 35.5]]
    assert table.select(['name'], table.fields['name'] > 'G') == [['George']]
    assert table.select(['id'], table.fields['id'] >= 2) == [[2]]
    assert table.select(['id'], 2 <= table.fields['id']) == [[2]]
    assert table.select(['id'], 0 < table.fields['id']) == [[1], [2]]


def test_select_equal(table):
    assert table.select(['id'], table.fields['name'] == 'fred') == []
    assert table.select(['id'], table.fields['name'] == 'Fred') == [[2]]
    assert table.select(['id', 'name', 'age'], table.fields['age'] == 35.5) == [[1, 'George', 35.5]]
    match = r"cannot compare Field\(index=2, name='age', type=<class 'lab1.types.FloatType'>\) and 36: different types"
    with pytest.raises(ConditionError, match=match):
        table.select(['id'], table.fields['age'] == 36)


def test_complex_condition(table):
    assert table.select(['id'], (0 < table.fields['id']) & (table.fields['id'] < 2)) == [[1]]
    assert table.select(['id'], (0 < table.fields['id']) | (table.fields['id'] < 2)) == [[1], [2]]

    with pytest.raises(TypeError, match=r"unsupported operand type\(s\) for &: 'Field' and 'BinaryCondition'"):
        assert table.select(['id'], 0 < table.fields['id'] & (table.fields['id'] < 2)) == [[1]]
    with pytest.raises(TypeError, match=r"unsupported operand type\(s\) for &: 'Field' and 'Field'"):
        assert table.select(['id'], 0 < table.fields['id'] & table.fields['id'] < 2) == [[1]]
    with pytest.raises(ConditionError, match=r"operators 'and' and 'or' support only binary arguments"):
        assert table.select(['id'], (0 < table.fields['id']) & table.fields['id'] < 2) == [[1]]
    with pytest.raises(TypeError,
                       match=r"'<' not supported between instances of 'BinaryCondition' and 'BinaryCondition'"):
        assert table.select(['id'], (0 < table.fields['id']) < (table.fields['id'] < 2)) == [[1], [2]]


# noinspection PyTypeChecker
def test_select_compare_fields():
    table = Table(columns=(Column('id', IntType), Column('planned', IntType), Column('factually', IntType),))
    table.insert(dict(id=1, planned=5, factually=10))
    table.insert(dict(id=2, planned=5, factually=5))
    table.insert(dict(id=3, planned=5, factually=4))
    assert table.select(['id'], table.fields['planned'] < table.fields['factually']) == [[1]]
    assert table.select(['id'], table.fields['planned'] > table.fields['factually']) == [[3]]
    assert table.select(['id'], table.fields['planned'] == table.fields['factually']) == [[2]]
    assert table.select(['id'], table.fields['planned'] >= table.fields['factually']) == [[2], [3]]
    assert table.select(['id'], table.fields['planned'] != table.fields['factually']) == [[1], [3]]
