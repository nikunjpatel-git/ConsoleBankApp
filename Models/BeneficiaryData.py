import re


class Beneficiary:
    def __init__(self):
        """
        Initializes Beneficiary instance.

        """
        self.name = ''
        self.ifsc_code = ''
        self.account_number = ''

    def set_beneficiary(self):
        """
        Sets the beneficiary instance attributes.

        """
        # input beneficiary name
        self.name = input("Enter Beneficiary Name:")

        # Regex for IFSC Code
        exp = re.compile('[A-Za-z]{4}0[0-9]{6}')

        # input IFSC code
        while exp.match(self.ifsc_code) is None:
            print("Note :- IFSC Code should contain 11 alphanumeric characters and must follow normal guidelines. ")
            self.ifsc_code = input("Enter IFSC code: ")

        # input beneficiary account number
        while len(self.account_number) != 12 or not self.account_number.isdigit():
            print("Note :- Account number should be 12 digits long ")
            self.account_number = input("Enter Account Number: ")