class Lab1BaseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TableCreationError(Lab1BaseError):
    pass
