from datetime import datetime


class Transaction:
    def __init__(self):
        """
        Initializes Transaction instance.

        """
        self.sender = None
        self.receiver = None
        self.amount = 0
        self.date = None

    def add_transaction(self, sender, receiver, db):
        """
        Adds transaction for a customer.

        Parameters:
              sender(Customer): Customer instance
              receiver(Customer): Customer instance
              db(DbConnector): Database Connector instance
        """
        got_receiver = False
        self.sender = sender
        result = None

        # input receiver account number and check if it exists in database
        while not got_receiver:
            acc_num = validate_account_number(sender.accountNumber)
            result = db.check_receiver(acc_num)
            if result is not None:
                got_receiver = True

        # populate transaction.receiver attribute
        self.receiver = receiver
        self.receiver.cust_id = result[0]
        self.receiver.bal = result[5]
        self.receiver.accountNumber = result[6]
        self.receiver.userName = result[1]
        self.amount = sender.bal + 1

        # input amount
        while self.amount > sender.bal or self.amount < 0:
            self.amount = int(input("Enter transaction amount: "))
            if self.amount > sender.bal:
                print("Insufficient balance")

        # perform transaction
        self.sender.bal -= self.amount
        self.receiver.bal += self.amount

        # add transaction in db
        db.add_transaction_to_db(self)
        self.date = datetime.now()

        # add transaction to customer instance
        self.sender.transactions.append(self)


def validate_account_number(sender_acc_num):
    """
    validates and check the syntax of the given account number.

    Parameters:
        sender_acc_num(string): sender account number.

    Returns:
        string: syntactically valid receiver account number
    """
    acc_num = ''
    while not acc_num.isdigit() or len(acc_num) != 12 or acc_num == sender_acc_num:
        acc_num = input("Enter the recipient account number: ")
    return acc_num
