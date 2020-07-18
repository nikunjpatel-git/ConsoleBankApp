from Utilities.Util import *


class CardDetails:
    def __init__(self):
        self.CardNumber = ''
        self.CardType = ''
        self.Cvv = ''
        self.Mpin = ''

    def add_card(self, card_type, db):
        """
        Add data to cards instance attributes.

        Parameters:
            card_type(string): Type of card to add
            db(DbConnector): Database Connector instance
        """
        # auto generate unique card number
        got_card_num = False
        card_num = 0
        while not got_card_num:
            self.CardNumber = random_num_gen(16)
            got_card_num = db.validate_number("carddetails", "card_number", self.CardNumber)

        # auto generate cvv number
        self.Cvv = random_num_gen(3)

        # input mpin for th auto generated card
        while len(self.Mpin) != 4 or not self.Mpin.isdigit():
            print("Note :- mpin should be 4 digits long and must contain only digits ")
            self.Mpin = input(f"Enter MPin for the {card_type} card: ")
