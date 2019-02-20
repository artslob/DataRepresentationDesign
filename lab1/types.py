from datetime import datetime


class FieldType:
    _type = None

    @classmethod
    def validate_value(cls, value):
        if not cls._is_valid(value):
            raise ValueError(f'value {value!r} is not valid')

        return value

    @classmethod
    def _is_valid(cls, value):
        return isinstance(value, cls._type)


class IntType(FieldType):
    _type = int


class FloatType(FieldType):
    _type = float


class DatetimeType(FieldType):
    _type = datetime


class StringType(FieldType):
    _type = str


class BinaryType(FieldType):
    _type = bytes
