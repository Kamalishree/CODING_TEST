class InvalidLoanException(Exception):
    def __init__(self, message="Loan with the specified ID was not found."):
        super().__init__(message)
