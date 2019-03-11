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
    table.delete(table.fields['age'] <= 40.)
    assert len(table.rows) == 0
    assert table.rows == []
