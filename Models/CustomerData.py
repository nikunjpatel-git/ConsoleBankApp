from .CardData import CardDetails
from .BeneficiaryData import Beneficiary
from Utilities.Util import *
from .TransactionData import Transaction
import os
import re


class Customer:
    def __init__(self):
        """
        Initializes Customer instance.

        """
        self.cust_id = 0
        self.userName = ''
        self.address = ''
        self.aadharNumber = ''
        self.mobileNumber = ''
        self.accountNumber = ''
        self.cards = []
        self.beneficiaries = []
        self.transactions = []
        self.bal = 500

    def register(self, db):
        """
        Registers the customer.

        Parameters:
            db(DbConnector): Database Connector object
        """
        print("")
        decorate_heading(f"Registration Module")

        # input username
        got_username = False
        while not got_username:
            self.userName = input("Enter UserName: ")
            got_username = db.validate_number("customer", "username", self.userName)
            if not got_username:
                print(f"Username: {self.userName} is already taken. Try another one.")

        # input address
        self.address = input("Enter Address: ")

        # input aadhar number
        while len(self.aadharNumber) != 12 or not self.aadharNumber.isdigit():
            print("Note :- Aadhar number should be 12 digits long ")
            self.aadharNumber = input("Enter Aadhar Number: ")

        # input mobile number
        while len(self.mobileNumber) != 10 or not self.mobileNumber.isdigit():
            print("Note :- Mobile number should be 10 digits long ")
            self.mobileNumber = input("Enter Mobile Number: ")

        # input cards
        self.cards = []
        while len(self.cards) < 2:
            card = CardDetails()
            if len(self.cards) == 0:
                card.add_card("Credit", db)
                card.CardType = 'C'
            else:
                card.add_card("Debit", db)
                card.CardType = 'D'

            self.cards.append(card)

        # auto generate unique account number
        got_acc_num = False
        while not got_acc_num:
            self.accountNumber = random_num_gen(12)
            got_acc_num = db.validate_number("customer", "account_number", self.accountNumber)

    def print_details(self):
        """
        Displays the customer data on dashboard.

        """
        # display customers' personal info
        print("")
        print("UserName: " + self.userName)
        print("Account Number: "+self.accountNumber)
        print("Address: " + self.address)
        print("Aadhar Number: " + self.aadharNumber)
        print("Mobile Number: " + self.mobileNumber)
        print("Account Balance: " + str(self.bal))
        print("")

        # display details of all cards
        print("Your CardDetails: ")
        for each_card in self.cards:
            print("Card Type: " + each_card.CardType)
            print("Card Number: " + each_card.CardNumber)
            print("Card CVV Number: " + each_card.Cvv)

        # display all beneficiaries
        if len(self.beneficiaries) == 0:
            print("\nThere are no beneficiaries added yet.")
        else:
            print("\nYour Beneficiaries:")
            for each in self.beneficiaries:
                print("Name: "+each.name)
                print("IFSC Code: " + each.ifsc_code)
                print("Account Number: " + each.account_number)
                print("")

        # display all transactions
        if len(self.transactions) == 0:
            print("There are no transactions yet.")
        else:
            print("\nYour Transactions:")
            for each in self.transactions:
                print("Recipient: "+each.receiver.accountNumber)
                print("Amount: " + str(each.amount))
                print("Date: " + each.date.strftime("%d-%m-%Y %H:%M:%S"))
                print("")

    def login(self, db):
        """
        Login the customer.

        Parameters:
        db(DbConnector): Database Connector object
        """
        print("")
        decorate_heading(f"Login Module")

        # login loop
        logged_in = False
        result = None
        while not logged_in:
            username = input("Enter UserName: ")
            result = db.get_all("customer", "username", username)
            if len(result) != 0:
                logged_in = True
            else:
                print("Incorrect Username, Please try again.......")

        # initialize customer attributes using db
        user = result[0]
        self.cust_id, self.userName, self.address, self.aadharNumber, \
            self.mobileNumber, self.bal, self.accountNumber = user

        # initialize card details of the customer using db
        result = db.get_all("carddetails", "cust_id", self.cust_id)
        for each_card in get_organized(result):
            card = CardDetails()
            id, card.CardNumber, card.Cvv, card.Mpin,card.CardType, cust_id = each_card
            self.cards.append(card)

        # initialize beneficiary details of the customer using db
        result = db.get_all("beneficiary", "cust_id", self.cust_id)
        for each_ben in get_organized(result):
            beneficiary = Beneficiary()
            id, beneficiary.name, beneficiary.ifsc_code, beneficiary.account_number, cust_id = each_ben
            self.beneficiaries.append(beneficiary)

        # initialize transaction details of the customer using db
        result = db.get_transaction_details(self.cust_id)
        for each_tran in get_organized(result):
            transaction = Transaction()
            transaction.sender = self
            receiver = Customer()
            transaction.amount, transaction.date, receiver.accountNumber, receiver.cust_id = each_tran
            transaction.receiver = receiver
            self.transactions.append(transaction)

        os.system('clear')

    def change_mpin(self, db):
        """
        Changes Mpin of a card.

        Parameters:
            db(DbConnector): Database Connector instance
        """
        # display choice of cards
        for each_card in self.cards:
            print(f"{(self.cards.index(each_card))+1}. {each_card.CardType} card: {each_card.CardNumber}")

        # input user choice
        length = len(self.cards) + 1
        while length > len(self.cards):
            choice = input("Enter choice from above options: ")
            if choice.isdigit():
                length = int(choice)

        card_to_change = self.cards[length-1]

        # verify old mpin
        mpin = ''
        while (len(mpin) != 4) or (not mpin.isdigit()) or (mpin != card_to_change.Mpin):
            mpin = input(f"Enter your old MPin for the card number {card_to_change.CardNumber} :")

        # input new mpin
        mpin = ''
        while len(mpin) != 4 or not mpin.isdigit():
            mpin = input(f"Enter your new MPin for the card number {card_to_change.CardNumber} :")

        card_to_change.Mpin = mpin

        # update mpin in db
        db.update_mpin(card_to_change)

    def update_info(self, db):
        """
        Updates customer information.

        Parameters:
            db(DbConnector): Database Connector instance
        """
        # display choice
        print("Select the information to update.")
        print("1. Address")
        print("2. Mobile no.")
        print("3. Both")

        # input choice
        int_choice = 4
        while int_choice not in [i for i in range(1, 4)]:
            choice = input("Enter choice from above options: ")
            if choice.isdigit():
                int_choice = int(choice)

        # update address
        if int_choice in [1, 3]:
            self.address = input("Enter updated address: ")

        # update mobile number
        if int_choice in [2, 3]:
            self.mobileNumber = ''
            while len(self.mobileNumber) != 10 or not self.mobileNumber.isdigit():
                print("Note :- Mobile number should be 10 digits long ")
                self.mobileNumber = input("Enter Updated Mobile Number: ")

        # update information in database
        db.update_customer_details(self)

    def add_cards(self, db):
        os.system('clear')
        card = CardDetails()
        card_type = ''

        # input card type to add
        exp = re.compile('[CDcd]')
        while exp.match(card_type) is None:
            card_type = input("Enter the card type to add [C/D]:")

        if card_type.upper() == 'C':
            card.CardType = 'C'
            card_type = 'Credit'
        else:
            card.CardType = 'D'
            card_type = 'Debit'

        # add card
        card.add_card(card_type, db)
        self.cards.append(card)

        # add card in database
        db.add_card_to_db(card, self.cust_id)


def get_organized(result):
    for each_record in result:
        yield tuple(each_record)



