def test_update(table):
    assert len(table.rows) == 2
    table.update(dict(name='Test'))
    assert table.rows == [dict(id=1, name='Test', age=35.5), dict(id=2, name='Test', age=25.)]
    assert table.select(['name']) == [['Test'], ['Test']]
    table.update(dict(id=1000), table.fields['id'] == 1)
    assert table.select(['id']) == [[1000], [2]]


def test_update_conditions(table):
    table.update(dict(name='Test'), table.fields['id'] < 0)
    assert table.select(['name']) == [['George'], ['Fred']]
    table.update(dict(name='Test'), (1 < table.fields['id']) & (table.fields['age'] > 20.))
    assert table.select(['name']) == [['George'], ['Test']]
    table.update(dict(name='2'), (1 < table.fields['id']) | (30. < table.fields['age']))
    assert table.select(['name']) == [['2'], ['2']]
