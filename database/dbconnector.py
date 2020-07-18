import mysql.connector
import re
import os
from datetime import datetime
from Models.BeneficiaryData import Beneficiary
from Models.CardData import CardDetails


class DbConnector:
    my_db = None
    cursor = None

    def __init__(self):
        """
        Initializes DbConnector instance.

        """
        # create a db handle
        self.my_db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123456@abc",
            database="testdb"
        )
        self.cursor = self.my_db.cursor(buffered=True)

    def save(self):
        # commit database operation
        self.my_db.commit()

    def add_customer_to_db(self, customer):
        """
        Saves customer to database for the first time.

        Parameters:
            customer(Customer): Customer instance.
        """
        insert_query = f"INSERT INTO customer (username, address, aadhar_number, mobile_number,bal, account_number)\
         Values ('{customer.userName}','{customer.address}','{customer.aadharNumber}',\
                '{customer.mobileNumber}',{customer.bal},'{customer.accountNumber}')"

        self.cursor.execute(insert_query)
        self.save()

        # get customer id of the newly added record
        select_query = "SELECT id from customer where username = '{}'".format(customer.userName)
        self.cursor.execute(select_query)
        result = self.cursor.fetchone()
        cust_id = result[0]

        # add card to db
        for each_card in customer.cards:
            insert_query = "INSERT INTO carddetails (card_number, cvv, mpin, type, cust_id) Values (%s,%s,%s,%s,%s)"
            data = [(each_card.CardNumber, each_card.Cvv, each_card.Mpin, each_card.CardType, cust_id)]
            self.cursor.executemany(insert_query, data)
        self.save()

    def validate_number(self, table, where_col, col_value):
        """
        Checks if the given number is unique in the database.

        Parameters:
            table(string): Table name
            where_col(string): Column name
            col_value(string): number to verify

        Returns:
            bool: False if number is duplicate else True
        """
        sql_query = f"SELECT * FROM {table} WHERE {where_col} = '{col_value}'"
        self.cursor.execute(sql_query)
        result = self.cursor.fetchone()
        if result is not None:
            return False
        else:
            return True

    def add_beneficiary(self, cust_id, beneficiary):
        """
        Saves beneficiary to database.

        Parameters:
            cust_id(int): Customers' id
            beneficiary(Beneficiary): Beneficiary instance
        """
        sql_query = f"INSERT INTO beneficiary (b_name, ifsc_code, account_number, cust_id)\
         Values ('{beneficiary.name}','{beneficiary.ifsc_code}','{beneficiary.account_number}', '{cust_id}')"

        self.cursor.execute(sql_query)
        self.save()

    def add_card_to_db(self, card, cust_id):
        """
        Saves card to database.

        Parameters:
            cust_id(int): Customers' id
            card(CardDetails): CardDetails instance.
        """
        insert_query = "INSERT INTO carddetails (card_number, cvv, mpin, type, cust_id) Values (%s,%s,%s,%s,%s)"
        data = [(card.CardNumber, card.Cvv, card.Mpin, card.CardType, cust_id)]

        self.cursor.executemany(insert_query, data)
        self.save()

    def get_all(self, table, where_col, col_value):
        """
        Selects all the records for the given table, column and value

        Parameters:
            table(string): Table name
            where_col(string): Column name
            col_value(string/int):  This is the column value to add

        Returns:
            list(tuple): The fetched records.
        """
        if isinstance(col_value, int):
            select_query = f"SELECT * from {table} where {where_col} = {col_value}"
        else:
            select_query = f"SELECT * from {table} where {where_col} = '{col_value}'"
        self.cursor.execute(select_query)
        result = self.cursor.fetchall()
        return result

    def get_transaction_details(self, cust_id):
        """
        Get transaction details of a customer.

        Parameters:
              cust_id(int): Customer id

        Returns:
              list(tuple): The fetched transactions for the given customer id.
        """
        select_query = f"SELECT amount, date, account_number, to_account FROM \
        transactions as t JOIN customer as c on t.to_account = c.id  where from_account = {cust_id}"
        self.cursor.execute(select_query)
        result = list(self.cursor.fetchall())
        return result

    def update_mpin(self, card):
        """
        Updates MPin in the database.

        Parameters:
            card(CardDetails): CardDetails instance
        """
        update_query = f"UPDATE carddetails SET mpin = '{card.Mpin}' WHERE card_number = '{card.CardNumber}'"
        self.cursor.execute(update_query)
        self.save()

    def update_customer_details(self, customer):
        """
        Updates the customer information in database.

        Parameters:
            customer(Customer): Customer instance.
        """
        update_query = f"UPDATE customer SET address = '{customer.address}', mobile_number = '{customer.mobileNumber}'\
        WHERE id = '{customer.cust_id}'"
        self.cursor.execute(update_query)
        self.save()

    def check_receiver(self, receiver):
        """
        Validates if there is any customer with the given account number.

        Parameters:
            receiver(string): Account Number of the receiver.
        """
        sql_query = f"SELECT * FROM customer WHERE account_number = '{receiver}'"
        self.cursor.execute(sql_query)
        result = self.cursor.fetchone()
        return result

    def add_transaction_to_db(self, transaction):
        """
        Saves transaction to database.

        Parameters:
            transaction(Transaction): Transaction instance
        """
        update_query = f"UPDATE customer SET bal = {transaction.sender.bal}\
                WHERE id = {transaction.sender.cust_id}"
        self.cursor.execute(update_query)

        update_query = f"UPDATE customer SET bal = {transaction.receiver.bal}\
                        WHERE id = {transaction.receiver.cust_id}"
        self.cursor.execute(update_query)

        insert_query = f"INSERT INTO transactions (from_account, to_account, amount, date) \
        Values({transaction.sender.cust_id},{transaction.receiver.cust_id}, {transaction.amount}, '{datetime.now()}')"
        self.cursor.execute(insert_query)
        self.save()





