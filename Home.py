import mysql.connector
import os
import sys
import time
from Models.CustomerData import Customer
from Models.TransactionData import Transaction
from Models.BeneficiaryData import Beneficiary
from Utilities.Util import *
from database.dbconnector import DbConnector


def dashboard(customer, db):
    """
    Displays the Dashboard to the user after login.

    Parameters:
    customer(Customer): customer object
    """
    choosing = True
    os.system('clear')

    # input choice
    while choosing:
        print("")
        decorate_heading(f"Hello {customer.userName}. Welcome to this Bank")
        customer.print_details()
        print("")
        print("1. Update Info")
        print("2. Transfer Fund")
        print("3. Change MPin")
        print("4. Add Cards")
        print("5. Add Beneficiaries")

        int_choice = 6
        while int_choice not in [i for i in range(1, 6)]:
            choice = input("Enter choice from above options: ")
            if choice.isdigit():
                int_choice = int(choice)

        if int_choice == 1:
            customer.update_info(db)
        elif int_choice == 2:
            transaction = Transaction()
            transaction.add_transaction(customer, Customer(), db)
        elif int_choice == 3:
            customer.change_mpin(db)
        elif int_choice == 4:
            customer.add_cards(db)
        elif int_choice == 5:
            beneficiary = Beneficiary()
            beneficiary.set_beneficiary()
            customer.beneficiaries.append(beneficiary)
            db.add_beneficiary(customer.cust_id, beneficiary)


# Main Program Starts here
if __name__ == "__main__":
    try:
        # get database handle
        db = DbConnector()

        # instantiate a customer
        customer = Customer()

        # input choice
        print("1. Login")
        print("2. Register")
        print("Press Any Other key to Exit......")
        choice = int(input("Enter choice: "))

        if choice == 1:
            os.system('clear')
            # redirect to login page
            customer.login(db)

            # redirect to dashboard
            dashboard(customer, db)

        elif choice == 2:
            os.system('clear')
            # initialize customer instance
            customer.register(db)

            # add customer to db
            db.add_customer_to_db(customer)

            customer = Customer()
            os.system('clear')
            # redirect to login page
            customer.login(db)

            # redirect to dashboard
            dashboard(customer, db)

    except mysql.connector.Error as se:
        db.my_db.rollback()
        # print("Something went wrong: {}".format(se))
    except ValueError as ve:
        pass
        # print("Something went wrong: {}".format(ve))
    except Exception as e:
        #pass
        print("exception handled: {}".format(e))
    else:
        os.system('clear')

    decorate_heading("Thank You for Using This Bank")
    time.sleep(2)
    sys.exit()
