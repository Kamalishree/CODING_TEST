from dao.ILoanRepository import ILoanRepository
from exception.InvalidLoanException import InvalidLoanException
from util.DBConnUtil import DBConnUtil
from entity.customer import Customer
from entity.homeloan import HomeLoan
from entity.carloan import CarLoan
import math

class LoanRepositoryImpl(ILoanRepository):

    def __init__(self):
        self.conn = DBConnUtil.get_connection()

    def apply_loan(self, loan):
        try:
            confirm = input("Do you want to apply for the loan? (Yes/No): ").strip().lower()
            if confirm != "yes":
                print("Loan application cancelled by user.")
                return

            cursor = self.conn.cursor()

            # Insert Customer if not exists
            cursor.execute("SELECT * FROM Customer WHERE customer_id = ?", loan.customer.customer_id)
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO Customer (customer_id, name, email, phone, address, credit_score) VALUES (?, ?, ?, ?, ?, ?)",
                    (loan.customer.customer_id, loan.customer.name, loan.customer.email,
                     loan.customer.phone, loan.customer.address, loan.customer.credit_score)
                )

            # Insert into Loan table
            cursor.execute("""
                INSERT INTO Loan (loan_id, customer_id, principal_amount, interest_rate, loan_term, loan_type, loan_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (loan.loan_id, loan.customer.customer_id, loan.principal_amount, loan.interest_rate,
                  loan.loan_term, loan.loan_type, loan.loan_status))

            # Insert into sub-type table
            if isinstance(loan, HomeLoan):
                cursor.execute("""
                    INSERT INTO HomeLoan (loan_id, property_address, property_value)
                    VALUES (?, ?, ?)
                """, (loan.loan_id, loan.property_address, loan.property_value))

            elif isinstance(loan, CarLoan):
                cursor.execute("""
                    INSERT INTO CarLoan (loan_id, car_model, car_value)
                    VALUES (?, ?, ?)
                """, (loan.loan_id, loan.car_model, loan.car_value))

            self.conn.commit()
            print("Loan successfully applied and stored in database.")

        except Exception as e:
            print("Error applying loan:", e)

    def calculate_interest(self, loan_id=None, principal_amount=None, rate=None, term=None):
        try:
            if loan_id:
                cursor = self.conn.cursor()
                cursor.execute("SELECT principal_amount, interest_rate, loan_term FROM Loan WHERE loan_id = ?", loan_id)
                row = cursor.fetchone()
                if not row:
                    raise InvalidLoanException(f"No loan found with ID {loan_id}")
                principal_amount, rate, term = row

            #  Convert Decimal or string to float before math
            principal = float(principal_amount)
            r = float(rate)
            t = float(term)

            interest = (principal * r * t) / 1200  # annual interest rate divided by 12*100
            return round(interest, 2)

        except InvalidLoanException as e:
            print(e)
        except Exception as e:
            print("Error calculating interest:", e)
            return None


    def loan_status(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT C.credit_score, L.loan_status
                FROM Customer C JOIN Loan L ON C.customer_id = L.customer_id
                WHERE L.loan_id = ?
            """, loan_id)

            row = cursor.fetchone()
            if not row:
                raise InvalidLoanException(f"Loan ID {loan_id} not found.")
            credit_score, current_status = row

            if current_status != "Pending":
                print(f"Loan already {current_status}")
                return

            new_status = "Approved" if credit_score > 650 else "Rejected"
            cursor.execute("UPDATE Loan SET loan_status = ? WHERE loan_id = ?", new_status, loan_id)
            self.conn.commit()
            print(f"Loan {loan_id} has been {new_status}.")

        except InvalidLoanException as e:
            print(e)
        except Exception as e:
            print("Error updating loan status:", e)

    def calculate_emi(self, loan_id=None, principal_amount=None, rate=None, term=None):
        try:
            if loan_id:
                cursor = self.conn.cursor()
                cursor.execute("SELECT principal_amount, interest_rate, loan_term FROM Loan WHERE loan_id = ?", loan_id)
                row = cursor.fetchone()
                if not row:
                    raise InvalidLoanException(f"Loan ID {loan_id} not found.")
                principal_amount, rate, term = row

            # Safe conversions from Decimal or string to float
            principal = float(principal_amount)
            r = float(rate) / 12 / 100  # monthly interest rate
            n = float(term)  # total number of months

            # Protect against division by zero or invalid math
            if r == 0 or n == 0:
                print("Invalid rate or term. Cannot calculate EMI.")
                return None

            # EMI formula
            emi = (principal * r * math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1)
            return round(emi, 2)

        except InvalidLoanException as e:
            print(e)
        except Exception as e:
            print("Error calculating EMI:", e)
            return None


    def loan_repayment(self, loan_id, amount):
        try:
            emi = self.calculate_emi(loan_id=loan_id)
            if not emi:
                return

            if amount < emi:
                print(f"Payment rejected. Minimum EMI amount is {emi}")
                return

            num_emis = int(amount // emi)
            print(f"Payment accepted. {num_emis} EMIs paid for loan {loan_id}.")

            # You can insert into Repayment table if implemented

        except Exception as e:
            print("Error during repayment:", e)

    def get_all_loans(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT L.loan_id, C.name, L.principal_amount, L.interest_rate, L.loan_term, L.loan_type, L.loan_status
                FROM Loan L JOIN Customer C ON L.customer_id = C.customer_id
            """)
            rows = cursor.fetchall()

            if not rows:
                print("No loans found.")
                return

            for row in rows:
                print(f"LoanID: {row[0]}, Customer: {row[1]}, Amount: {row[2]}, Rate: {row[3]}%, Term: {row[4]} months, Type: {row[5]}, Status: {row[6]}")

        except Exception as e:
            print("Error fetching loan data:", e)

    def get_loan_by_id(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT L.loan_id, C.name, L.principal_amount, L.interest_rate, L.loan_term, L.loan_type, L.loan_status
                FROM Loan L JOIN Customer C ON L.customer_id = C.customer_id
                WHERE L.loan_id = ?
            """, loan_id)

            row = cursor.fetchone()
            if not row:
                raise InvalidLoanException(f"Loan ID {loan_id} not found.")

            print(f"LoanID: {row[0]}, Customer: {row[1]}, Amount: {row[2]}, Rate: {row[3]}%, Term: {row[4]} months, Type: {row[5]}, Status: {row[6]}")

        except InvalidLoanException as e:
            print(e)
        except Exception as e:
            print("Error fetching loan by ID:", e)
