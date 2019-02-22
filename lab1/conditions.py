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

    @staticmethod
    def _evaluate_arg(arg, table: 'tables.Table', row: dict):
        if isinstance(arg, tables.Field):
            if arg.name not in table.fields:
                raise ConditionError(f'field {arg!r} not in table {table!r}')
            return row[arg.name]

        elif isinstance(arg, Condition):
            return arg.evaluate(table, row)

        # means its basic type
        return arg

    def evaluate(self, table: 'tables.Table', row: dict):
        left_result = self._evaluate_arg(self.left, table, row)
        right_result = self._evaluate_arg(self.right, table, row)

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
