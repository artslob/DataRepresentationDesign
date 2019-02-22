from abc import ABC, abstractmethod

from lab1 import tables
from lab1.exceptions import ConditionError


class Condition(ABC):
    @abstractmethod
    def evaluate(self, table: 'tables.Table', row: dict):
        pass


class BinaryCondition(Condition):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

        if op not in ('&', '|', '<', '<=', '==', '!=', '>', '>='):
            raise ConditionError(f'unknown operator: {op!r}')

        if op in ('&', '|') and (not isinstance(left, Condition) or not isinstance(right, Condition)):
            raise ConditionError(f"operators 'and' and 'or' support only binary arguments")

        if op in ('<', '<=', '==', '!=', '>', '>=') and (isinstance(left, Condition) or isinstance(right, Condition)):
            raise ConditionError(f'comparision does not support conditions')

    def evaluate(self, table: 'tables.Table', row: dict):
        # TODO move duplicate code to function
        if isinstance(self.left, tables.Field):
            if self.left.name not in table.fields:
                raise ConditionError(f'field {self.left!r} not in table {table!r}')

            left_result = row[self.left.name]
        elif isinstance(self.left, Condition):
            left_result = self.left.evaluate(table, row)
        else:
            left_result = self.left

        if isinstance(self.right, tables.Field):
            if self.right.name not in table.fields:
                raise ConditionError(f'field {self.right!r} not in table {table!r}')

            right_result = row[self.right.name]
        elif isinstance(self.right, Condition):
            right_result = self.right.evaluate(table, row)
        else:
            right_result = self.right

        op = self.op

        if op == '&':
            return left_result and right_result
        elif op == '|':
            return left_result or right_result
        elif op == '<':
            return left_result < right_result
        elif op == '<=':
            return left_result <= right_result
        elif op == '==':
            return left_result == right_result
        elif op == '!=':
            return left_result != right_result
        elif op == '>':
            return left_result > right_result
        elif op == '>=':
            return left_result >= right_result

    def __and__(self, other):
        return BinaryCondition(self, '&', other)

    def __or__(self, other):
        return BinaryCondition(self, '|', other)
