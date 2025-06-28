from entity.loan import Loan

class CarLoan(Loan):
    def __init__(self, loan_id=None, customer=None, principal_amount=0.0, interest_rate=0.0, loan_term=0,
                 car_model=None, car_value=0.0, loan_type="CarLoan", loan_status="Pending"):
        super().__init__(loan_id, customer, principal_amount, interest_rate, loan_term, loan_type, loan_status)
        self.car_model = car_model
        self.car_value = car_value

    def get_car_model(self):
        return self.car_model

    def set_car_model(self, car_model):
        self.car_model = car_model

    def get_car_value(self):
        return self.car_value

    def set_car_value(self, car_value):
        self.car_value = car_value

    def __str__(self):
        return super().__str__() + f", CarModel={self.car_model}, CarValue={self.car_value}"
