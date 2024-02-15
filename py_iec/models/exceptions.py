class IECError(Exception):
    """Exception raised for errors in the IEC API.

    Attributes:
        code -- input salary which caused the error.
        error -- description of the error
    """

    def __init__(self, code, error):
        self.code = code
        self.error = error
        super().__init__(f"(Code {self.code}): {self.error}")


class IECLoginError(IECError):
    """Exception raised for errors in the IEC Login.

    Attributes:
        code -- input salary which caused the error.
        error -- description of the error
    """

    def __init__(self, code, error):
        IECError.__init__(self, code, error)
