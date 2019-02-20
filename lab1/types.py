from datetime import datetime


class FieldType:
    _type = None

    @classmethod
    def is_valid(cls, value):
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
