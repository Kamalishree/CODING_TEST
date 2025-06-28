class Customer:
    def __init__(self, customer_id=None, name=None, email=None, phone=None, address=None, credit_score=None):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.credit_score = credit_score

    # Getters and Setters
    def get_customer_id(self):
        return self.customer_id

    def set_customer_id(self, customer_id):
        self.customer_id = customer_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_phone(self):
        return self.phone

    def set_phone(self, phone):
        self.phone = phone

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_credit_score(self):
        return self.credit_score

    def set_credit_score(self, credit_score):
        self.credit_score = credit_score

    def __str__(self):
        return f"Customer[ID={self.customer_id}, Name={self.name}, Email={self.email}, Phone={self.phone}, Address={self.address}, CreditScore={self.credit_score}]"
