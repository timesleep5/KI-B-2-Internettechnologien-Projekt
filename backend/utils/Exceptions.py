class NoKeywordFoundException(Exception):
    """
    Exception raised when no keyword is found in the input.

    This exception is typically raised when a required keyword is expected in the input,
    but none is found or recognized.

    Attributes:
        message (str): Optional error message describing the exception.
    """

    def __init__(self, message="No keyword found in input"):
        self.message = message
        super().__init__(self.message)


class NoMatchingStateException(Exception):
    """
    Exception raised when no matching state is found.

    This exception is typically raised when attempting to retrieve or set a state that
    does not match any predefined state in the application.

    Attributes:
        message (str): Optional error message describing the exception.
    """

    def __init__(self, message="No matching state found"):
        self.message = message
        super().__init__(self.message)
