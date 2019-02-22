class Lab1BaseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TableCreationError(Lab1BaseError):
    pass


class TableInsertError(Lab1BaseError):
    pass


class TableSelectError(Lab1BaseError):
    pass


class ConditionError(Lab1BaseError):
    pass
