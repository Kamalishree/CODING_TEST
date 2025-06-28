class Loan:
    def __init__(self, loan_id=None, customer=None, principal_amount=0.0, interest_rate=0.0, loan_term=0, loan_type=None, loan_status="Pending"):
        self.loan_id = loan_id
        self.customer = customer  # This is a Customer object
        self.principal_amount = principal_amount
        self.interest_rate = interest_rate
        self.loan_term = loan_term
        self.loan_type = loan_type
        self.loan_status = loan_status

    # Getters and Setters
    def get_loan_id(self):
        return self.loan_id

    def set_loan_id(self, loan_id):
        self.loan_id = loan_id

    def get_customer(self):
        return self.customer

    def set_customer(self, customer):
        self.customer = customer

    def get_principal_amount(self):
        return self.principal_amount

    def set_principal_amount(self, principal_amount):
        self.principal_amount = principal_amount

    def get_interest_rate(self):
        return self.interest_rate

    def set_interest_rate(self, interest_rate):
        self.interest_rate = interest_rate

    def get_loan_term(self):
        return self.loan_term

    def set_loan_term(self, loan_term):
        self.loan_term = loan_term

    def get_loan_type(self):
        return self.loan_type

    def set_loan_type(self, loan_type):
        self.loan_type = loan_type

    def get_loan_status(self):
        return self.loan_status

    def set_loan_status(self, loan_status):
        self.loan_status = loan_status

    def __str__(self):
        return f"Loan[ID={self.loan_id}, Customer={self.customer}, Amount={self.principal_amount}, Interest={self.interest_rate}, Term={self.loan_term}, Type={self.loan_type}, Status={self.loan_status}]"
