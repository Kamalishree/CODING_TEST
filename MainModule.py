import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entity.customer import Customer
from entity.homeloan import HomeLoan
from entity.carloan import CarLoan
from dao.LoanRepositoryImpl import LoanRepositoryImpl

def main():
    repo = LoanRepositoryImpl()

    while True:
        print("\n======= Loan Management System =======")
        print("1. Apply Loan")
        print("2. Get Loan by ID")
        print("3. Get All Loans")
        print("4. Calculate Interest")
        print("5. Calculate EMI")
        print("6. Update Loan Status")
        print("7. Loan Repayment")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Apply Loan
            print("\n-- Enter Customer Details --")
            customer_id = int(input("Customer ID: "))
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            address = input("Address: ")
            credit_score = int(input("Credit Score: "))

            customer = Customer(customer_id, name, email, phone, address, credit_score)

            print("\n-- Enter Loan Details --")
            loan_id = int(input("Loan ID: "))
            principal = float(input("Principal Amount: "))
            rate = float(input("Interest Rate (%): "))
            term = int(input("Loan Term (months): "))
            loan_type = input("Loan Type (HomeLoan/CarLoan): ")

            if loan_type.lower() == "homeloan":
                property_address = input("Property Address: ")
                property_value = float(input("Property Value: "))
                loan = HomeLoan(loan_id, customer, principal, rate, term, property_address, property_value)
            elif loan_type.lower() == "carloan":
                car_model = input("Car Model: ")
                car_value = float(input("Car Value: "))
                loan = CarLoan(loan_id, customer, principal, rate, term, car_model, car_value)
            else:
                print("Invalid loan type. Try again.")
                continue

            repo.apply_loan(loan)

        elif choice == '2':
            loan_id = int(input("Enter Loan ID: "))
            repo.get_loan_by_id(loan_id)

        elif choice == '3':
            repo.get_all_loans()

        elif choice == '4':
            loan_id = int(input("Enter Loan ID to calculate interest: "))
            interest = repo.calculate_interest(loan_id=loan_id)
            if interest is not None:
                print(f"Interest Amount: ₹{interest}")

        elif choice == '5':
            loan_id = int(input("Enter Loan ID to calculate EMI: "))
            emi = repo.calculate_emi(loan_id=loan_id)
            if emi is not None:
                print(f"Monthly EMI: ₹{emi}")

        elif choice == '6':
            loan_id = int(input("Enter Loan ID to update status: "))
            repo.loan_status(loan_id)

        elif choice == '7':
            loan_id = int(input("Enter Loan ID: "))
            amount = float(input("Enter repayment amount: "))
            repo.loan_repayment(loan_id, amount)

        elif choice == '8':
            print("Exiting Loan Management System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
